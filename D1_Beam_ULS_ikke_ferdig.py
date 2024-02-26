# import of libaries
import numpy as np

#---------------------------
 
# defining the class "Beam"
class capacity_beam_ULS:
    def __init__(self,cross_section,material,load):
        self.alpha_bal = self.get_alpha(material)
        self.M_Rd = self.calc_M_Rd(self.alpha_bal,material,cross_section) * 10 ** (-6)
        self.V_Rd = self.calc_V_Rd(cross_section,load,material) * 10 ** (-3)
        self.utilization_degree_M = self.get_utilization_degree_M(self.M_Rd,load)
        self.utilization_degree_V = self.get_utilization_degree_V(self.V_Rd,load)
        self.M_check = self.do_control_of_M_cap(self.M_Rd,load,self.utilization_degree_M)
        self.V_check = self.do_control_of_V_cap(self.V_Rd,load,self.utilization_degree_V)
    
    def get_alpha(self,material):
        alpha_bal = material.eps_cu1 / (material.eps_cu1 + material.eps_yd)
        #self.alpha_norm_reinforced = concrete.eps_cu1 / (concrete.eps_cu1 + 2 * steel.eps_yk)
        return alpha_bal
    
    def calc_M_Rd(self,alpha_bal,material,cross_section):
        M_Rd = 0.8 * alpha_bal * (1 - 0.4 * alpha_bal) * material.fcd * cross_section.width * cross_section.d ** 2
        return M_Rd
    
    # 6.2.2 
    def calc_V_Rd(self,cross_section,load,material):
        k = max(1 + np.sqrt(200/cross_section.d),2)
        ro_l = max(cross_section.As/(cross_section.width * cross_section.d),0.02)
        sigma_cp = max(load.N_Ed / cross_section.Ac, 0.2 * material.fcd)
        CRd_c = 0.18 / material.gamma_concrete
        k_1 = 0.15
        v_min = 0.035 * k ** (3/2) * material.fck ** (0.5)
        V_Rd = (CRd_c * k * (100 * ro_l * material.fck) ** (1/3) + k_1 * sigma_cp) * cross_section.width * cross_section.d
        V_Rd_min = (v_min + k_1 * sigma_cp) * cross_section.width * cross_section.d
        V_Rd = max(V_Rd,V_Rd_min)
        return V_Rd
    
    def get_utilization_degree_M(self,M_Rd,load):
        M_utilization = (M_Rd / load.M_Ed) * 100
        return M_utilization

    def get_utilization_degree_V(self,V_Rd,load):
        V_utilization = (V_Rd / load.V_Ed) * 100
        return V_utilization
    
    def do_control_of_M_cap(self,M_Rd,load,M_utilization):
        if M_Rd >= load.M_Ed:
            M_check = f'Moment capacity is suificcient, and the utilization degree is {M_utilization:.1f}%'
        else: 
            M_check = f'Moment capacity is not suificcient, and the utilization degree is {M_utilization:.1f}%'
        return M_check
    
    def do_control_of_V_cap(self,V_Rd,load,V_utilization):
        if V_Rd >= load.V_Ed:
            V_check = f'Shear capacity is suificcient, and the utilization degree is {V_utilization:.1f}%'
        else:
            V_check = f'Shear capacity is not suificcient, and the utilization degree is {V_utilization:.1f}%'
        return V_check
    
    def calc_shear_reinforcement(self,load,V_Rd,cross_section,material):
        if V_Rd >= load.V_Ed:
            As_shear = 0 
        else:
            V_Rd = load.V_Ed
            s = 100
            As_shear = V_Rd * s / 0.9 * cross_section.d * material.fyd 
        return self.As_shear 
