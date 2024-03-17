"""
Looking at the prestress force as a force within the material. 
Here there are only assumed prestressing in tension.
"""
import numpy as np

class capacity_prestress:

    def __init__(self,material,delta_sigma_pL,load,cross_section,losses):
        self.sigma_p0 = min(0.8 * material.fpk, 0.9 * material.fp01k)
        self.eps_p0 = self.sigma_p0 / material.Ep
        self.eps_loss = self.eps_p0 * (abs(delta_sigma_pL) / self.sigma_p0)* 10 ** 2
        self.eps_diff = self.eps_p0 - self.eps_loss
        self.MRd = self.calc_moment_capacity(eps_cu,material.fpd,material.Epm,material.fcd,cross_section.width,cross_section.d,cross_section.Ap)
        self.control_M = self.control_moment(load.M_Ed)
        self.NEd = self.calc_NEd(material.gamma_0_9,losses.total_loss,load.P0)
        self.V_Rd = self.calc_shear_capacity(cross_section.d,cross_section.As,cross_section.width,cross_section.Ac,material.fcd,material.gamma_concrete,material.fck)
        self.control_V = self.control_V(load.V_Ed)
     

    def get_lambda(self,fck)-> float:
        if fck <= 50:
            self.lambda_factor = 0.8
        elif 50 < fck <= 90:
            self.lambda_factor = 0.8 - (fck/50)/400
        return self.lambda_factor 
    
    def get_netta(self,fck)-> float:
        if fck <= 50:
            self.netta = 1.0
        elif 50 < fck <= 90:
            self.netta = 1.0 - (fck/50)/200
        return self.netta

    def calc_moment_capacity(self,eps_cu,fpd,Ep,fcd,width,d,Ap):
        alpha_b = eps_cu / (eps_cu + fpd / Ep - self.eps_diff)
        Apb = self.netta * self.lambda_factor * alpha_b * width * d * fcd / fpd 
        if Ap <= Apb: 
            alpha = (fpd * Ap)/ (self.netta * self.lambda_factor * fcd * width * d)
        elif Ap > Apb:
            a = self.netta * self.lambda_factor * fcd * width * d
            b = (eps_cu - self.eps_diff) * Ep * Ap
            c = - eps_cu * Ep * Ap
            alpha = max((- b + np.sqrt(b ** 2 - 4 * a * c)) / (2 * a), - b - np.sqrt(b ** 2 - 4 * a * c) / (2 * a))
        MRd = self.netta * self.lambda_factor * alpha * (1 - 0.5 * self.lambda_factor * alpha) * fcd * width * d ** 2
        return MRd
    
    def control_moment(self,M_Ed):
        if M_Ed < self.MRd:
            return True
        else: #Må slakkarmeres
            #As_necessary = (M_Ed - MRd) / (fyd * d)
            #if As > As_necessary
            return False
        
    def calc_NEd(self,gamma_p,loss,P0): 
        NEd = gamma_p * (1 - loss / 100) * P0
        return NEd

    def calc_shear_capacity(self,d,As,width,Ac,fcd,gamma_concrete,fck):
        k = max(1 + np.sqrt(200/d),2)
        ro_l = max(As/(width * d),0.02)
        sigma_cp = max(self.NEd / Ac, 0.2 * fcd)
        CRd_c = 0.18 / gamma_concrete
        k_1 = 0.15 #assumed compressive force 
        v_min = 0.035 * k ** (3/2) * fck ** (0.5)
        V_Rd_c = (CRd_c * k * (100 * ro_l * fck) ** (1/3) + k_1 * sigma_cp) * width * d
        V_Rd_min = (v_min + k_1 * sigma_cp) * width * d
        V_Rd_c = max(V_Rd_c,V_Rd_min)
        return V_Rd_c
        
    def do_control_of_V_cap(self,V_Ed):
        if self.V_Rd >= V_Ed:
            return True
        else:
            return False
    


    

