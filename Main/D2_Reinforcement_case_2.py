

import numpy as np


class Reinforcement_control_prestressed:
    ''' Class to contain all reinforcement controls for prestressed cross section
    All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the 
    book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2 by Svein Ivar Sørensen.
    '''
    def __init__(self, cross_section, material, load, ULS_prestressed, Asw: float):
        '''Args: 
            cross_section(class):  class that contain all cross-section properties
            material(class):  class that contain all material properties
            load(class):  class that contain all load properties
            ULS_control(class):  class that contain all ULS controls
            Asw(float):  shear reinforcement area, defined by user [mm2/mm]
        Returns: 
            As(float):  Minimum reinforcement [mm2]
            Asw_control(boolean):  Control of shear reinforcement, return True or False
            Ap_necessary(float):  area of prestress reinforcement necessary [mm2]
            A_control(boolean):  Control of prestress reinforcement area, return True or False
        '''
        #self.As = self.calculate_As_min(material.fctm,material.fyk,cross_section.width,cross_section.d)
        self.Asw_control = self.control_reinforcement_shear(material.fck,material.fyk,cross_section.width,Asw)
        self.Ap_necessary= self.calculate_prestress_reinforcement(load.M_ULS,cross_section.d,material.fpd,material.lambda_factor,ULS_prestressed.alpha)
        self.control = self.control_prestress_reinforcement(self.Ap_necessary,cross_section.Ap)

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
    
    def control_reinforcement_shear(self, fck: float, fyk: float, width: float, Asw: float)-> bool:
        ''' Control of shear reinforcement area according to EC2 9.2.2(5)
        Args:
            fck(int):  cylinder compression strength, from material class [N/mm2]
            fyk(int):  steel tensions characteristic strength, from material class [N/mm2]
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
        
    def calculate_prestress_reinforcement(self, M_Ed: float, d: float, fpd: float, lambda_factor: float, alpha: float)-> float:
        ''' Function that calculates necessary prestress reinforcement
        Args: 
            M_Ed(float):  design moment, from load class [kNm]
            d(float):  effective height, from cross section class [mm]
            fpd(float):  pretension strength, from material class [N/mm2]
            lambda_factor(float):  factor which defines the effective height for compression zone in concrete
            alpha(float):  compression-zone-height factor for cross section, from ULS control class
        Returns:
            Ap_necessary(float):  Necessary prestress reinforcement [mm2]
        '''
        z = (1- 0.5 * lambda_factor * alpha) * d
        Ap_necessary = (M_Ed * 10  ** 6) / ( z * fpd)
        return Ap_necessary
    
    def control_prestress_reinforcement(self, Ap_necessary: float, Ap: float)-> bool:
        ''' Control of prestress reinforcement
        Args:
            Ap_necessary(float):  Necessary prestress reinforcement [mm2]
            Ap(float):  Area of prestress reinforcement [mm2]
        Returns:
            Ap_control(boolean):  Control of prestress reinforcement area, return True or False
        '''
        if Ap >= Ap_necessary:
            return True
        else:
            return False

