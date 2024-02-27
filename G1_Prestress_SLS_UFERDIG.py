
# Stress calculation for uncracked concrete, stage 1

class prestress_SLS:

    def __init__(self):
           


    def calc_pretension_force









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