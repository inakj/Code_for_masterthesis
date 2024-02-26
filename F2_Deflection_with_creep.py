import numpy as np

from C1_Cross_section import cross_section_parameters

from C2_Design_values import design_values

from B1_Material_strength_properties import Material

from F4_phi_calculation import creep_number

class creep_deflection:

    def __init__(self,loading,cross_section,material,creep_t1_days,creep_t2_days,factor: float):
        self.Ec_eff = self.calculate_eff_long_E(material.Ecm,creep_t1_days.phi,creep_t2_days.phi)
        self.Ec_mid = self.calculate_middle_E(loading.M1,loading.M2,self.Ec_eff)
        self.netta = self.calculate_netta(material.Es,self.Ec_mid)
        self.ro = self.calculate_ro(cross_section.As,cross_section.width,cross_section.d)
        self.alpha = self.calculate_alpha(self.netta,self.ro)
        self.Ic = self.calculate_Ic(self.alpha,cross_section.width,cross_section.d)
        self.longterm_load = self.calculate_longterm_load(loading.g,loading.p,factor) 
        self.w = self.calculate_deflection_with_shrink(loading.length,self.longterm_load,self.Ec_mid,self.Ic)   
#------
    def calculate_eff_long_E(self,Ecm,phi_1,phi_2):
        Ec_eff_1 = Ecm / (1 + phi_1)
        Ec_eff_2 = Ecm / (1 + phi_2)
        Ec_eff = [Ec_eff_1,Ec_eff_2]
        return Ec_eff 

    def calculate_middle_E(self,M1,M2,Ec_eff):
        sum_M = M1 + M2 #Denne må gjøres generell
        Ec_eff_1 = Ec_eff[0]
        Ec_eff_2 = Ec_eff[1]
        Ec_mid = sum_M / (M1 / Ec_eff_1 + M2 / Ec_eff_2)
        return Ec_mid

    def calculate_netta(self,Es,Ec_mid):
        netta_ny = Es / Ec_mid
        return netta_ny

    def calculate_ro(self,As,width,d):
        ro_ny = As / (width * d)
        return ro_ny

    def calculate_alpha(self,netta_ny,ro_ny):
        alpha = np.sqrt((netta_ny * ro_ny)**2 + 2 * netta_ny * ro_ny) - netta_ny * ro_ny
        return alpha

    def calculate_Ic(self,alpha,width,d):
        Ic = 0.5 * alpha ** 2 * (1 - alpha/3) * width * d ** 3
        return Ic

    def calculate_longterm_load(self,g,p,factor):
        longterm_load = g + p * factor
        return longterm_load

    def calculate_deflection_with_shrink(self,length,longterm_load,Ec_mid,Ic):
        w = (5/384) * longterm_load * (length * 1000) ** 4 / (Ec_mid * Ic)
        return w
    

