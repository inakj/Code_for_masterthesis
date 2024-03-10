
# Stress calculation for uncracked concrete, stage 1

class uncracked_concrete_prestress:

    def __init__(self,material,cross_section,load):
        self.P0 = self.calc_prestress_force(material.Fp01k,material.fpk,cross_section.Ap)
        self.netta = self.calc_netta(material.Ep,material.Ecm)
        self.At = self.calc_At(cross_section.Ac,self.netta,cross_section.Ap)
        self.yt = self.calc_yt(self.netta,cross_section.Ap,cross_section.e,self.At)
        self.It = self.calc_It(cross_section.width,cross_section.height,self.yt,self.netta,cross_section.Ap,cross_section.e)
        self.sigma_c = self.calc_concrete_stress(cross_section.height,self.P0,self.At,self.It,self.yt,cross_section.e,load.Mg_SLS)
        self.sigma_c_under = self.sigma_c[0]
        self.sigma_c_over = self.sigma_c[1]
        self.sigma_c_prestress = self.sigma_c[2]
        self.stress_reduction = self.calc_stress_reduction(self.sigma_c_prestress,material.Ecm,material.Es,material.fpk)
        self.control = self.control_concrete_stress(material.fck,material.fctm,self.sigma_c_over,self.sigma_c_under,self.sigma_c_prestress)

   
    def calc_prestress_force(self,Fp01k,fpk,Ap):
        fp01k = Fp01k / Ap 
        sigma_prestress_max = min(0.8 * fpk, 0.9 * fp01k)
        Pmax = sigma_prestress_max * Ap
        P0 = Pmax
        return P0
    
    def calc_netta(self,Ep,Ecm):
        netta = Ep / Ecm
        return netta
    
    #Transformed cross section
    def calc_At(self,Ac,netta,Ap):
        At = Ac + (netta - 1) * Ap
        return At
    
    # Distance between reinforced gravity axis and concrete gravity axis
    def calc_yt(self,netta,Ap,e,At):
        y_t = ((netta - 1) * Ap * e) / At
        return y_t
    
    # Moment of inertia
    def calc_It(self,width,height,y_t,netta,Ap,e):
        It = (width * height ** 3) / 12 + width * height * y_t ** 2 + (netta - 1) * Ap * (e - y_t) ** 2
        return It

    # Concrete stress in top, bottom and in line with prestressing
    def calc_concrete_stress(self,height,P0,At,It,yt,e,Mg_SLS):
        N = - P0
        Mt = - P0 * (e - yt) + Mg_SLS
        y = height / 2
        sigma_c_under = N / At + Mt / (It / (y-yt))
        y = - height / 2
        sigma_c_over = N / At + Mt / (It / (y-yt))
        y = e
        sigma_c_prestress = N / At + Mt / (It / (y-yt))
        sigma_c = [sigma_c_under,sigma_c_over,sigma_c_prestress]
        return sigma_c

    # Concrete stress reduction in prestress
    def calc_stress_reduction(self,sigma_c_prestress,Ecm,Es,fpk):
        delta_eps_p = abs(sigma_c_prestress / Ecm) 
        delta_sigma_p = delta_eps_p * Es 
        percentage_reduction = (delta_sigma_p / (0.8 * fpk)) * 100
        return percentage_reduction
    
    # Control of concrete stress. Control of biggest pressure in top/bottom and control of tension in prestress
    def control_concrete_stress(self,fck,fctm,sigma_c_over,sigma_c_under,sigma_c_prestress): # if returns True, then should be cracked
        allowed_pressure = - 0.6 * fck 
        allowed_tension = fctm
        if min(sigma_c_over,sigma_c_under) > allowed_pressure:
            return False
        elif sigma_c_prestress > allowed_tension:
            return False 
        else:
            return True
        
    
        
        
