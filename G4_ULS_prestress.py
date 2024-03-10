"""
Looking at the prestress force as a force within the material. 
Here there are only assumed prestressing in tension.
"""
import numpy as np

class capacity_prestress:

    def __init__(self,material,delta_sigma_pL,load,cross_section):
        self.sigma_p0 = min(0.8 * material.fpk, 0.9 * material.fp01k)
        self.eps_p0 = self.sigma_p0 / material.Ep
        self.eps_loss = self.eps_p0 * (abs(delta_sigma_pL) / self.sigma_p0)* 10 ** 2
        self.eps_diff = self.eps_p0 - self.eps_loss
        self.MRd = self.calc_moment_capacity(eps_cu,material.fpd,material.Epm,material.fcd,cross_section.width,cross_section.d,cross_section.Ap)
        self.control = self.control_moment(load.M_Ed)

        
    def calc_moment_capacity(self,eps_cu,fpd,Ep,fcd,width,d,Ap):
        alpha_b = eps_cu / (eps_cu + fpd / Ep - self.eps_diff)
        Apb = 0.8 * alpha_b * width * d * fcd / fpd 
        if Ap <= Apb: # Skal = være her??
            alpha = (fpd * Ap)/ (0.8 * fcd * width * d)
        elif Ap > Apb:
            a = 0.8 * fcd * width * d
            b = (eps_cu - self.eps_diff) * Ep * Ap
            c = - eps_cu * Ep * Ap
            alpha = max((- b + np.sqrt(b ** 2 - 4 * a * c)) / (2 * a), - b - np.sqrt(b ** 2 - 4 * a * c) / (2 * a))
        MRd = 0.8 * alpha * (1 - 0.4 * alpha) * fcd * width * d ** 2
        return MRd
    
    def control_moment(self,M_Ed):
        if M_Ed < self.MRd:
            return True
        else: #Må slakkarmeres
            #As_necessary = (M_Ed - MRd) / (fyd * d)
            #if As > As_necessary
            return False
        

    def calc_shear_capacity(self):
        


    

