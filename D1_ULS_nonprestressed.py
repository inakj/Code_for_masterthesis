
import numpy as np

class ULS_nonprestressed:
    ''' Class to contain all relevant ultimate limit state (ULS) controls. 
    Calculations are based on following assumptions from EC2 6.1(2)P:
    - Full bond between concrete and reinforcement
    - Naviers hypothesis
    - Stress-strain properties from EC 3.1.7, figure 3.5
    - Ignore concrete tension strength 
    Assumed that the ultimate failure criterion is compression failure in concrete. 
    All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the 
    book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2"
    '''
    def __init__(self,cross_section,material,load,width,Asw):
        '''Args:
            cross_section(class):  class that contain all cross-section properties
            material(class):  class that contain all material properties
            load(class):  class that contain all load properties
            Asw(float):  area of shear reinforcement per meter, defined by user [mm2/mm] 
        Returns:
            alpha_nonprestressed(float):  Compression-zone-height factor for nonprestressed cross section
            M_Rd(float):  Moment capacity of beam [kNm]
            V_Rd(float):  Shear force capacity of beam [kNm]
            M_control(boolean):  Control of moment capacity 
            V_control(boolean):  Control of shear force capacity
            M_utilization(float):  Utilization degree for moment [%]
            V_utilization(float):  Utilization degree for shear force [%]
        '''
        self.alpha_nonprestressed = self.calculate_alpha(material.eps_cu3,material.eps_yd,cross_section.As,
            material.Es,material.fcd,width,cross_section.d,material.fyd,material.lambda_factor,material.netta)
        self.M_Rd = self.calculate_M_Rd(self.alpha_nonprestressed,material.fcd,width,cross_section.d,material.lambda_factor,material.netta) 
        self.V_Rd = self.calculate_V_Rd(cross_section.d,cross_section.As,width,material.fcd,material.gamma_concrete,material.fck) 
        self.M_control = self.control_of_M_cap(self.M_Rd,load.M_ULS)
        self.V_control = self.control_of_V_cap(self.V_Rd,load.V_ULS,Asw,cross_section.d,material.fyd)
    
    def calculate_alpha(self,eps_cu3: float, eps_yd: float, As: float, Es: float, fcd: float,
                        width: float, d: float, fyd: float, lambda_factor: float, netta: float)-> float:
        ''' Function that calculate factor alpha to decide if cross section is under-reinforced or 
        over-reinforced
        Args:
            eps_cu3(float):  concrete strain for bilinear/rectangular analysis from material class
            eps_yd(float):  design yeild strain for reinforcement from material class
            As(float):  area of reinforcement from cross section class[mm2]
            fcd(float):  design compression strength in concrete from material class [N/mm2]
            width(float):  width of beam [mm]
            d(float):  effective height from cross section class [mm]
            fyd(float):  design tension strength in reinforcement [N/mm2]
            lambda(float):  factor which defines the effective height for 
                compression zone in concrete from material class
            netta(float):  factor which defines the effective strength from material class
        Returns:
            alpha(float):  Compression-zone-height factor for nonprestressed cross section
        '''
        alpha_bal = eps_cu3 / (eps_cu3 + eps_yd)
        Ap_balanced = lambda_factor * netta * alpha_bal * width * d * fcd / fyd 
        if As <= Ap_balanced: # --> Under-reinforced
            alpha = (fyd * As)/ (lambda_factor * netta * fcd * width * d)
        elif As > Ap_balanced: # --> Over-reinforced
            # Using abc-formula
            a = lambda_factor * netta * fcd * width * d
            b = eps_cu3 * Es * As
            c = - eps_cu3 * Es * As
            alpha = max((- b + np.sqrt(b ** 2 - 4 * a * c)) / (2 * a),
                        - b - np.sqrt(b ** 2 - 4 * a * c) / (2 * a))
        return alpha

    def calculate_M_Rd(self,alpha: float, fcd: float, width: float, d: float, lambda_factor: float,
                       netta: float)-> float:
        ''' Function that calculates M_Rd based on calculated alpha
        Args:
            alpha(float):  Compression-zone-height factor for nonprestressed cross section
            fcd(float):  design compression strength in concrete from material class [N/mm2]
            width(float):  width of beam [mm]
            d(float):  effective height from cross section class [mm]
        Returns: 
            M_Rd(float):  moment capacity [kNm]
        '''
        M_Rd = lambda_factor * netta * alpha * (1 - 0.5 * lambda_factor * alpha) * fcd * width * d ** 2
        return M_Rd
    
    
    def calculate_V_Rd(self,d: float, As: float, width: float, fcd: float, gamma_concrete: float, 
                       fck: int)-> float:
        ''' Function that calculate V_Rd according to EC2 6.2.2(1), when there is assumed no 
        calculation based need for shear reinforcement.
        Args:
            d(float):  effective height from cross section class [mm]
            As(float):  area of reinforcement from cross section class[mm2]
            width(float):  width of beam [mm]
            fcd(float):  design compression strength in concrete from material class [N/mm2]
            gamma_concrete(float):  materialfactor for concrete from material class
            fck(int):  cylinder compression strength from material class [N/mm2]
        Returns:
            V_Rd(float):  Shear force capacity [kN]
        '''
        k = max(1 + np.sqrt(200 / d), 2)
        ro_l = max(As / (width * d), 0.02)
        sigma_cp = 0.2 * fcd 
        CRd_c = 0.18 / gamma_concrete
        k_1 = 0.15
        v_min = 0.035 * k ** (3/2) * fck ** (0.5)
        V_Rd_c = (CRd_c * k * (100 * ro_l * fck) ** (1/3) + k_1 * sigma_cp) * width * d
        V_Rd_min = (v_min + k_1 * sigma_cp) * width * d
        V_Rd = max(V_Rd_c, V_Rd_min)
        return V_Rd * 10 ** 3
    
    def control_of_M_cap(self,M_Rd:float , M_Ed: float)-> bool:
        ''' Function that control moment capacity compared with design moment
        Args:
            M_Rd(float):  Moment capacity [kNm]
            M_Ed(float):  Design moment [kNm]
        Returns:
            The function returns "True" if the moment capacity is suifficent and 
            "False" if its not suifficent
        '''
        if M_Rd >= M_Ed:
            return True
        else: 
            return False
    
    def control_of_V_cap(self,V_Rd: float, V_Ed: float, Asw: float, d: float, fyd: float)-> bool:
        ''' Function that control shear capacity compared with design shear force. Also, if the 
        capacity is not suifficent, the function checks if the shear capacity is good enough according 
        to EC2 6.2.3(3) where there is calculation-based need for shear reinforcement. 
        Args:
            V_Rd(float):  Shear capacity [kNm]
            V_Ed(float):  Design shear force [kNm]
            Asw(float):  area of shear reinforcement per meter, defined by user [mm2/mm] 
            d(float):  effective height from cross section class [mm]
            fyd(float): design tension strength in reinforcement [N/mm2]
        Returns:
            The function returns "True" if the shear capacity is good enough and 
            "False" if its not good enough
        '''
        if V_Rd >= V_Ed:
            return True
        else:
            VRd_s = Asw * 0.9 * d * fyd * 10 ** -3
            if VRd_s >= V_Ed:
                return True
            else:
                return False
        
    
   