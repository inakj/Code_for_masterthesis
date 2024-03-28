

import numpy as np

# Called ordinary reinforcement not normal! 

class Reinforcement_control:
    ''' Class to contain all reinforcement controls for ordinary reinforced cross section
    All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the 
    book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2 by Svein Ivar Sørensen.
    '''
    def __init__(self, cross_section, material, load, ULS_control, Asw: float):
        '''Args: 
            cross_section(class):  class that contain all cross-section properties
            material(class):  class that contain all material properties
            load(class):  class that contain all load properties
            ULS_control(class):  class that contain all ULS controls
            Asw(float):  shear reinforcement area, defined by user [mm2/mm]

        Returns: 
            As_necessary(float):  Necessary reinforcement [mm2]
            As_min(float):  Minimum reinforcement [mm2]
            As_max(float): Maximum reinforcement [mm2]
            A_control(boolean):  Control of reinforcement, return True or False
            Asw_control(boolean):  Control of shear reinforcement, return True or False
        '''
        self.As_necessary = self.calculate_necessary_reinforcement(load.M_ULS,cross_section.d,material.fyd,material.lambda_factor,ULS_control.alpha)
        self.As_min = self.calculate_As_min(material.fctm,material.fyk,cross_section.width,cross_section.d)
        self.As_max = self.calculate_As_max(cross_section.Ac)
        self.control = self.control_reinforcement(cross_section.As,self.As_max,self.As_min,self.As_necessary)
        self.Asw_control = self.control_reinforcement_shear(material.fck,material.fyk,cross_section.width,Asw)
        
    
    def calculate_necessary_reinforcement(self, M_Ed: float, d: float, fyd: float, lambda_factor: float, 
                                          alpha: float)-> float:
        ''' Function that calculates necessary reinforcement, based on formula (4.26) in book by Sørensen
        Args: 
            M_Ed(float):  design moment, from load class [kNm]
            d(float):  effective height, from cross section class [mm]
            fyd(float):  design tension strength in reinforcement, from material class [N/mm2]
            lambda_factor(float):  factor which defines the effective height for compression zone
            alpha(float):  compression-zone-height factor for cross section, from ULS control class
        Returns:
            As_necessary(float):  Necessary reinforcement [mm2]
        '''
        z = (1 - 0.5 * lambda_factor * alpha) * d
        As_necessary = (M_Ed * 10  ** 6) / ( z * fyd)
        return As_necessary

    def calculate_As_min(self, fctm: float, fyk: int, width: float, d: float)-> float:
        ''' Function that calculates As minimum according to EC2 9.2.1.1(1)
        Args:
            fctm(float):  middlevalue of concrete axial tension strength, from material class [N/mm2]
            fyk(int):  steel tensions characteristic strength, from material class[N/mm2]
            width(float):  width of beam, defined by user [mm]
            d(float):  effective height from cross section class, from cross section class [mm]
        Returns:
            As_min(float):  Minimum reinforcement [mm2]
        '''
        As_min = min(0.26 * (fctm / fyk) * width * d, 0.0013 * width * d)
        return As_min
    
    def calculate_As_max(self, Ac: float)-> float:
        '''Function that calculates As maximum according EC2 9.2.1.1(3)
        Args:
            Ac(float):  concrete area from cross section class [mm2]
        Returns:
            As_max(float):  Maximum reinforcement [mm2]
        '''
        As_max = 0.04 * Ac
        return As_max
    
    def control_reinforcement(self, As: float, As_necessary: float, As_max: float, As_min: float)-> bool:
        ''' Control of reinforcement area. The area As must be smaller than the maximum, larger than the minimum 
        and larger than the necessary area to satisfy for the design moment. 
        Args:
            As(float):  reinforcement area from cross section class [mm2]
            As_necessary(float):  necessary reinforcement [mm2]
            As_min(float):  minimum reinforcement [mm2]
            As_max(float): maximum reinforcement [mm2]
        Returns:
            As_control(boolean):  Return True if area is suifficent or False 
            if its not suifficent
        '''
        if As > As_max:
            return False
        elif As < As_min or As < As_necessary:
            return False
        else: 
            return True
        
    def control_reinforcement_shear(self, fck: float, fyk: float, width: float, Asw: float)-> bool:
        ''' Control of shear reinforcement area according to EC2 9.2.2(5)
        Args:
            fck(int):  cylinder compression strength from material class [N/mm2]
            fyk(int):  steel tensions characteristic strength from material class [N/mm2]
            width(float):  width of beam, defined by user [mm]
            Asw(float):  area of shear reinforcement per meter, defined by user [mm2/mm] 
        Returns:
            Asw_control(boolean):  Control of shear reinforcement, return True or False
        '''
        ro_w_min = 0.1  * np.sqrt(fck) / fyk
        alpha = 90
        b_w = width
        Asw_min = ro_w_min * b_w * np.sin(alpha) 
        if Asw_min < Asw:
            return True
        else:
            return False
        


