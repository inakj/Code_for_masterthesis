import numpy as np

from C1_Cross_section import cross_section_parameters


class deflection_shorttime:

    def __init__(self,loading,cross_section,material):
        self.netta = self.get_netta(material.Es,material.Ecm)
        self.ro = self.get_ro(cross_section.As,cross_section.width,cross_section.d)
        self.alpha_d = self.get_alfa_d(cross_section.Ac,cross_section.height,self.netta,cross_section.As,cross_section.d)
        self.Ic1 = self.get_Ic1(cross_section.width,cross_section.height,self.alpha_d)
        self.Is1 = self.get_Is1(cross_section.As,cross_section.d,self.alpha_d)
        self.EI_1 = self.get_bending_stiffness_uncracked_cross_section(material.Ecm,material.Es,self.Ic1,self.Is1)
        self.deflection_uncracked = self.get_deflection_cracked(loading.q,loading.length,self.EI_1)
        self.EI_2 = self.calc_bending_stiffness_cracked_cross_section(self.netta,self.ro,cross_section.width,cross_section.d,cross_section.As,material.Ecm,material.Es)
        self.deflection_cracked = self.get_deflection_cracked(loading.q,loading.length,self.EI_2)
        self.M_crack = self.get_M_cr(material.fctm,self.Ic1,self.netta,self.Is1,cross_section.height,self.alpha_d)
        self.q_cr = self.get_q_cr(self.M_crack,loading.length)
        self.total_deflection = self.calculate_deflection(self.M_crack,loading.M_SLS_tot,self.deflection_cracked,self.deflection_uncracked)
        self.max_deflection = self.get_max_deflection(loading.length)
        self.control = self.control_deflection(self.total_deflection,self.max_deflection)

    def get_netta(self,Es,Ecm):
        netta = Es / Ecm
        return netta
    
    def get_ro(self,As,b,d):
        ro = As / (b * d)
        return ro

    def get_alfa_d(self,Ac,h,netta,As,d):
        alpha_d = (Ac * 0.5 * h + netta * As * d)/(Ac + netta * As)
        return alpha_d
    
    def get_Ic1(self,b,h,alpha_d):
        Ic1 = b * h ** 3 / 12 + b * h * (alpha_d - h / 2) ** 2
        return Ic1
    
    def get_Is1(self,As,d,alpha_d):
        Is1 = As * (d - alpha_d) ** 2
        return Is1

    def get_bending_stiffness_uncracked_cross_section(self,Ecm,Es,Ic1,Is1):
        EI_1 = Ecm * Ic1 + Es * Is1 # Uncracked bending stiffness
        return EI_1

    def get_deflection_uncracked(self,load,length,EI_1):
        deflection_uncracked = 5/384 * load * (length * 1000) ** 4 / (EI_1)
        return deflection_uncracked
    
    def calc_bending_stiffness_cracked_cross_section(self,netta,ro,b,d,As,Ecm,Es):
        alpha_rel = np.sqrt((netta*ro) ** 2 + 2 * netta*ro) - netta*ro
        Ic2 = b * (alpha_rel * d) ** 3 / 3
        Is2 = As * ((1 - alpha_rel) * d) ** 2
        EI_2 = Ecm * Ic2 + Es * Is2
        return EI_2
    
    def get_deflection_cracked(self,load,length,EI_2):
        deflection_cracked = 5/384 * load * (length * 1000) ** 4 / (EI_2) 
        return deflection_cracked

    def get_M_cr(self,fctm,Ic1,netta,Is1,h,alpha_d):
        M_cr = fctm * (Ic1 + netta * Is1)/(h - alpha_d)
        return M_cr

    def get_q_cr(self,M_cr,length):
        q_cr = 8 * M_cr * 10 ** (-6) / length **2
        return q_cr

    def calculate_deflection(self,M_cr,M,deflection_cracked,deflection_uncracked): # 7.4.3, with tension stiffening
        beta = 0.5 # assumed long term load
        zeta = 1 - beta * (M_cr / (M * 10 ** 6)) ** 2 #Zeta: distribution coefficient, M_crack: crackmoment, M: SLS moment
        deflection  = zeta * deflection_cracked + (1 - zeta) * deflection_uncracked
        return deflection
    
    def get_max_deflection(self,length): # 7.4.1(4)
        max_deflection = (length * 1000) / 250
        return max_deflection

    def control_deflection(self,deflection,allowed_deflection):
        if allowed_deflection > deflection:
            return True
        else: 
            return False
    
