import numpy as np

class cracked_concrete_prestress:

    def __init__(self,material,cross_section,load,phi_1,phi_2,eps_cs):
        self.P0 = self.calc_prestress_force(material.Fp01k,material.fpk,cross_section.Ap)
        self.E_middle = self.calc_E_middle(material.Ecm,phi_1,phi_2,self.P0,cross_section.e,load.Mg_SLS,load.Mp_SLS)
        self.netta = material.Ep / self.E_middle
        self.ro = cross_section.Ap / (cross_section.width * cross_section.d)
        self.h0 = (2 * cross_section.Ac) / (2 * cross_section.height + 2 * cross_section.width)
        self.Ns = self.calc_axial_force(eps_cs,material.Ep,cross_section.Ap)
        self.a = self.calc_a(self.P0,self.Ns,load.Mg_SLS,load.Mp_SLS,cross_section.e)
        self.alpha = self.calc_alpha(cross_section.d,cross_section.e,self.a)
        self.sigma_c = self.calc_sigma_c(cross_section.d,cross_section.width,self.alpha)
        self.sigma_p = self.calc_sigma_p(self.sigma_c,self.E_middle,self.alpha,eps_cs,material.Ep)



    # Initial prestressing force 
    def calc_prestress_force(self,Fp01k,fpk,Ap,delta_sigma_pr):
        fp01k = Fp01k / Ap 
        self.sigma_pi= min(0.8 * fpk, 0.9 * fp01k) - delta_sigma_pr # sigma_delta_pr is loss because of relaxation
        Pmax = self.sigma_pi * Ap 
        P0 = Pmax * 10 ** -3
        return P0        
    
    # E-middle width selfload, liveload and prestress moment
    def calc_E_middle(self,Ecm,phi_1,phi_2,P0,e,Mg_SLS,Mp_SLS):
        EcL_1 = Ecm / (1 + phi_1)
        EcL_2 = Ecm / (1 + phi_2)
        self.Mp = - P0 * e * 10 ** -3
        M1 = Mg_SLS
        M2 = Mp_SLS
        E_middle = (abs(self.Mp) + M1 + M2) / ((abs(self.Mp) + M1)/ EcL_1 + M2 / EcL_2)
        return E_middle

    # After free shrink in concrete there is a applied a pressure force in prestress reinforcement
    # which is applied as tension in the cross section calculation
    def calc_axial_force(self,eps_cs,Ep,Ap):
        Ns = eps_cs * Ep * Ap * 10 ** -3
        return Ns
    
    # Calculate a from the equivalnt outher force situation after figure 6.8 in Sørensen
    def calc_a(self,P0,Ns,Mg_SLS,Mp_SLS,e):
        self.N = P0 - Ns #kN
        M = Mg_SLS + Mp_SLS + self.Mp + (Ns * e) * 10 ** -6
        a = M/self.N
        return a
    
    # equation 6.24
    def calc_alpha(self,d,e,a):
        # Coefficients of the cubic equation ax^3 + bx^2 + cx + d = 0
        coefficients = [d / 6 * (e + a), 0.5 * (1 - d / (e + a)), self.netta * self.ro, - self.netta * self.ro] 
        roots = np.roots(coefficients)
        for num in roots:
            if 0 < num < 1:
                alpha = float(num)
        return alpha
    
    # equation 6.22
    def calc_sigma_c(self,d,width,alpha):
        sigma_c = (self.N * 10 ** 3) / (width * d * (0.5 * alpha - self.netta * self.ro * (1 - alpha)/alpha))
        return sigma_c # Compression in concrete at top
    
    def calc_sigma_p(self,sigma_c,E_middle,alpha,eps_cs,Ep):
        eps_c = sigma_c / E_middle # concrete strain top 
        self.delta_eps_p = eps_c * (1 - alpha) / alpha # strain at prestressing
        delta_sigma_p = (self.delta_eps_p - eps_cs) * Ep # stress change in prestressing
        sigma_p = 0.95 * self.sigma_pi + delta_sigma_p #stress in prestressing
        return sigma_p
    




        #eps_ck = (1 - alpha) / alpha * (sigma_c / Ecm) #Short time strain in concrete near pretension
        #delta_eps_pL = self.delta_eps_p - eps_ck + eps_cs # change in strain because of creep and shrink
        #delta_sigma_pL = delta_eps_pL * Ep - delta_sigma_pr



       

    

    








