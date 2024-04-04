
import numpy as np

class ULS_prestressed:
    ''' Class to contain all relevant ultimate limit state (ULS) controls for prestressed cross section.
    All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2).
    '''

    def __init__(self, material, load, cross_section, time_effect):
        '''Args:
            material(class):  class that contain all material properties
            material(class):  class that contain all material properties
            load(class):  class that contain all load properties 
            time_effect(class):  class that contain time effects because of creep, shrink and relaxation
        Returns:
            eps_diff(float):  effective change differance beacuse of strain loss 
            alpha(float):  factor to decide if cross section is under-reinforced or over-reinforced
            M_Rd(float):  moment capacity [kNm]
            control_M(boolean):  return True if suifficent capacity, or False if not
            V_Rd(float):  shear capacity [kN]
            control_V(boolean):  return True if suifficent capacity, or False if not
        '''
        self.eps_diff = self.calculate_strain_diff(load.sigma_p_max,material.Ep,time_effect.loss_percentage)
        self.alpha = self.calculate_alpha(material.eps_cu3,cross_section.Ap,material.Ep,material.fcd,
                                self.eps_diff,cross_section.width,cross_section.d,material.fpd,material.lambda_factor,material.netta)
        self.M_Rd = self.calculate_moment_capacity(self.alpha,material.fcd,cross_section.width,cross_section.d,material.lambda_factor,material.netta)
        self.M_control = self.control_moment(load.M_ULS,load.M_prestress,self.M_Rd)
        self.V_Rd = self.calc_shear_capacity(cross_section.d,cross_section.As,cross_section.width,cross_section.Ac,material.fcd,material.gamma_concrete,
                                             material.fck,load.P0,material.gamma_0_9,time_effect.loss)
        self.V_control = self.control_V(self.V_Rd,load.V_ULS)
        self.M_utilization = self.control_utilization_M(self.M_Rd,load.M_ULS)
        self.V_utilization = self.control_utilization_V(self.V_Rd,load.V_ULS)
    
    def calculate_strain_diff(self, sigma_p: float, Ep: int, loss: float)-> float:
        ''' Function that calculates difference in strain because of losses
        Args:
            sigma_p(float):  design value of prestressing stress, from load class [N/mm2]
            Ep(int):  elasticity modulus for steel, from material class [N/mm2]
            loss(float):  loss in capacity because of time effects, from load class [%]
        Returns:
            eps_diff(float):  effective strain difference 
        '''
        eps_p0 = sigma_p / Ep 
        eps_loss = (loss / 100) * eps_p0
        eps_diff = eps_p0 - eps_loss
        return eps_diff

    def calculate_alpha(self, eps_cu3: float, Ap: float, Ep: float, fcd: float, eps_diff: float,
                        width: float, d: float, fpd: float, lambda_factor: float, netta: float)-> float:
        ''' Function that calculate factor alpha to decide if cross section is under-reinforced or 
        over-reinforced
        Args:
            eps_cu3(float):  concrete strain for bilinear/rectangular analysis, from material class
            Ap(float):  area of prestressed reinforcement, from cross section class[mm2]
            Ep(int):  elasticity moduls for prestressed reinforcement, from material class [N/mm2]
            fcd(float):  design compression strength in concrete, from material class [N/mm2]
            eps_diff(float):  effective strain difference 
            width(float):  width of beam [mm]
            d(float):  effective height, from cross section class [mm]
            fpd(float):  design prestressed strength in reinforcement [N/mm2]
            lambda_factor(float):  factor, from material class
            netta(float):  factor, from material class
        Returns:
            alpha(float):  Compression-zone-height factor for nonprestressed cross section
        '''
        alpha_b = eps_cu3 / (eps_cu3 + fpd / (Ep - eps_diff))
        Apb = netta * lambda_factor * alpha_b * width * d * fcd / fpd 
        if Ap <= Apb: 
            alpha = (fpd * Ap)/ (netta * lambda_factor * fcd * width * d)
        elif Ap > Apb:
            a = netta * lambda_factor * fcd * width * d
            b = (eps_cu3 - eps_diff) * Ep * Ap
            c = - eps_cu3 * Ep * Ap
            alpha = max((- b + np.sqrt(b ** 2 - 4 * a * c)) / (2 * a), - b - np.sqrt(b ** 2 - 4 * a * c) / (2 * a))
        return alpha

    def calculate_moment_capacity(self, alpha: float, fcd: float, width: float, d: float, lambda_factor: float,
                       netta: float)-> float:
        ''' Function that calculates M_Rd based on calculated alpha
        Args:
            alpha(float):  Compression-zone-height factor for nonprestressed cross section
            fcd(float):  design compression strength in concrete from material class [N/mm2]
            width(float):  width of beam [mm]
            d(float):  effective height from cross section class [mm]
            lambda_factor(float):  factor, from material class
            netta(float):  factor, from material class
        Returns: 
            M_Rd(float):  moment capacity [kNm]
        '''
        M_Rd = netta * lambda_factor * alpha * (1 - 0.5 * lambda_factor * alpha) * fcd * width * d ** 2
        return M_Rd
    
    def control_moment(self, M_ULS: float, M_p: float, M_Rd: float)-> bool:
        ''' Function that controls moment capacity 
        Args:   
            M_ULS(float):  design moment in ULS, from load class [kNm]
            M_p(float):  moment because of prestressing [kNm]
            M_Rd(float):  moment capacity [kNm]
        Returns:
            True or False(boolean):  True if capacity is suifficient, False if not
        '''
        M_Ed = M_ULS + M_p
        if M_Rd >= M_Ed:
            return True
        else: 
            return False
        

    def calc_shear_capacity(self,d:float, Ac: float, width: float, Ap: int, fcd: float, 
                            gamma_concrete: float, fck: int, P0: float, gamma_prestress: float, loss: float)-> float:
        ''' Function that calculate factor alpha to decide if cross section is under-reinforced or 
        over-reinforced
        Args:
            d(float):  effective height, from cross section class [mm]
            Ac(float):  area of concrete, from cross section class [mm2]
            width(float):  width of beam [mm]
            Ap(float):  area of prestressed reinforcement, from cross section class[mm2]
            fcd(float):  design compression strength in concrete, from material class [N/mm2]
            gamma_concrete(float):  materialfactor for concrete, from materal class
            fck(int):  cylinder compression strength [N/mm2]
            P0(float):   design value of prestressign force [N]
            gamma_prestresss(float):  loadfactor for prestressing
            loss(float): loss in capacity because of time effects [%]
        Returns:
            V_Rd(float):  shear capacity [kN]
        '''
        k = min(1 + np.sqrt(200/d),2)
        ro_l = min(Ap/(width * d),0.02)
        N_Ed = P0 * gamma_prestress * (1-loss/100)
        sigma_cp = min(N_Ed / Ac, 0.2 * fcd)
        CRd_c = 0.18 / gamma_concrete
        k_1 = 0.15 #assumed compressive force 
        v_min = 0.035 * k ** (3/2) * fck ** (0.5)
        V_Rd_c = (CRd_c * k * (100 * ro_l * fck) ** (1/3) + k_1 * sigma_cp) * width * d
        V_Rd_min = (v_min + k_1 * sigma_cp) * width * d
        V_Rd = max(V_Rd_c,V_Rd_min)
        return V_Rd * 10 ** -3
        
    def control_V(self, V_Rd: float, V_ULS: float)-> bool:
        ''' Function that controls moment capacity 
        Args:   
            M_ULS(float):  design moment in ULS, from load class [kNm]
            M_p(float):  moment because of prestressing [kNm]
            M_Rd(float):  moment capacity [kNm]
        Returns:
            True or False(boolean):  True if capacity is suifficient, False if not
        '''
        if V_Rd >= V_ULS:
            return True
        else:
            return False
    

    def control_utilization_M(self,M_Rd,M_Ed):
        '''
        '''
        utilization = (M_Ed / M_Rd) * 100
        return utilization
    
    def control_utilization_V(self,V_Rd,V_Ed):
        '''
        '''
        utilization = (V_Ed / V_Rd) * 100
        return utilization
    
    

