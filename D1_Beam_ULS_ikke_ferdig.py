# import of libaries
import numpy as np

#---------------------------
 
# defining the class "Beam"
class capacity_beam_ULS:
    def __init__(self,cross_section,material,load):
        self.alpha_bal = self.get_alpha(material.eps_cu1,material.eps_yd)
        self.M_Rd = self.calc_M_Rd(self.alpha_bal,material.fcd,cross_section.width,cross_section.d) 
        self.V_Rd = self.calc_V_Rd(cross_section.d,cross_section.As,cross_section.width,load.N_Ed,cross_section.Ac,material.fcd,material.gamma_concrete,material.fck) 
        self.utilization_degree_M = self.get_utilization_degree_M(self.M_Rd,load.M_Ed)
        self.utilization_degree_V = self.get_utilization_degree_V(self.V_Rd,load.V_Ed)
        self.M_check = self.do_control_of_M_cap(self.M_Rd,load.M_Ed,self.utilization_degree_M)
        self.V_check = self.do_control_of_V_cap(self.V_Rd,load.V_Ed,self.utilization_degree_V)
        self.shear_rebar = self.calc_shear_reinforcement(self.V_Rd,load.V_Ed,cross_section.d,material.fyd)
        self.control = self.do_control_ULS(self.M_utilization,self.V_utilization)
    
    def get_alpha(self,eps_cu1,eps_yd):
        alpha_bal = eps_cu1 / (eps_cu1 + eps_yd)
        return alpha_bal
    
    def calc_M_Rd(self,alpha_bal,fcd,width,d):
        M_Rd = 0.8 * alpha_bal * (1 - 0.4 * alpha_bal) * fcd * width * d ** 2
        return M_Rd
    
    # 6.2.2 
    def calc_V_Rd(self,d,As,width,N_Ed,Ac,fcd,gamma_concrete,fck):
        k = max(1 + np.sqrt(200/d),2)
        ro_l = max(As/(width * d),0.02)
        sigma_cp = max(N_Ed / Ac, 0.2 * fcd)
        CRd_c = 0.18 / gamma_concrete
        k_1 = 0.15
        v_min = 0.035 * k ** (3/2) * fck ** (0.5)
        V_Rd = (CRd_c * k * (100 * ro_l * fck) ** (1/3) + k_1 * sigma_cp) * width * d
        V_Rd_min = (v_min + k_1 * sigma_cp) * width * d
        V_Rd = max(V_Rd,V_Rd_min)
        return V_Rd
    
    def get_utilization_degree_M(self,M_Rd,M_Ed):
        M_utilization = (M_Ed / M_Rd) * 100
        return M_utilization

    def get_utilization_degree_V(self,V_Rd,V_Ed):
        V_utilization = (V_Ed / V_Rd) * 100
        return V_utilization
    
    def do_control_of_M_cap(self,M_Rd,M_Ed,M_utilization):
        if M_Rd >= M_Ed:
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
    
    def calc_shear_reinforcement(self,V_Rd,V_Ed,d,fyd): #  DENNE ER UFERDiG
        if V_Rd >= V_Ed:
            As_shear = 0 
        else:
            V_Rd = V_Ed
            s = 100
            As_shear = V_Rd * s / 0.9 * d * fyd 
        return As_shear 
    

    def do_control_ULS(self,M_utilization,V_utilization):
        if M_utilization > 100:
            return False
        elif V_utilization > 100:
            return False 
        else:
            return True