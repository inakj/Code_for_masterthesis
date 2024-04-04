
import numpy as np


class Crack_control:
    ''' Class to contain crack control in Service limit state (SLS) for ordinary reinforced cross section
    All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the 
    book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2 by Svein Ivar Sørensen.
    '''
    def __init__(self, cross_section, load, material, exposure_class: str, creep_number, bar_diameter: float):
        '''Args:
            cross_section(class):  class that contain all cross-section properties
            load(class):  class that contain all load properties
            material(class):  class that contain all material properties
            exposure_class(string):  exposure class to calculate nominal thickness, defined by user
            creep_number(class):  class that contain creep number phi for self- and liveload
            bar_diameter(float):  rebar diameter, defined by user [mm]

        Returns: 
            k_c(float):  factor that take into consideration the ratio between cnom and cmin,dur
            crack_width(float):  limit value of crack width [mm]
            alpha(float):  factor for calculating reinforcment stress
            sigma_s(float):  reinforcement stress [N/mm2]
            max_bar_diameter(float):  maximum bar diameter to limit crack width [mm]
            control_bar_diameter(boolean):  control of bar diameter, return True or False
        '''
        self.k_c = self.calculate_kc(cross_section.cnom,cross_section.c_min_dur)
        self.crack_width = self.get_limit_value(exposure_class,self.k_c)
        self.Ec_middle = self.calculate_E_middle(material.Ecm,creep_number.phi_selfload,creep_number.phi_liveload,load.M_SLS,load.Mg_SLS,load.Mp_SLS)
        self.alpha = self.calculate_alpha(material.Es,self.Ec_middle,cross_section.As,cross_section.width,cross_section.d)
        self.sigma_s = self.calculate_reinforcement_stress(self.alpha,cross_section.width,cross_section.d,load.M_SLS,self.Ec_middle,material.Es,cross_section.As)
        self.max_bar_diameter  = self.calculate_maximal_bar_diameter(self.crack_width,self.sigma_p)
        self.control_bar_diameter = self.control_of_bar_diameter(bar_diameter,self.max_bar_diameter)
        
    def calculate_kc(self, cnom: float, c_min_dur: float)-> float: 
        ''' Function that calculate the factor kc according to EC2 NA.7.3.1
        Args: 
            cnom(float):  nominal concrete cover, from cross section class [mm]
            c_min_dur(float):  smallest nominal cover, from cross section class [mm]
        Returns:
            k_c(float):  factor that take into consideration the ratio between cnom and cmin,dur
        '''
        kc = min(cnom / c_min_dur, 1.3)
        return kc

    def get_limit_value(self, exposure_class: str, k_c: float)-> float:
        ''' Function that get the limit value for crack width according to table NA.7.1. Assumed normal
        reinforcement or prestressed reinforcement without continous interaction. 
        Args:
            exposure_class(string):  exposure class to calculate nominal thickness, defined by user
            k_c(float):  factor that take into consideration the ratio between cnom and cmin,dur
        Returns:
            crack_width(float):  limit value of crack width [mm]
        Raises:
            ValueError: checks if the exposure class is either X0 or in the list list_of_exp_class
        '''
        list_of_exp_class = ['XC1', 'XC2', 'XC3', 'XC4', 'XD1', 'XD2', 'XD3', 'XS1', 'XS2', 'XS3']
        if exposure_class == 'X0':
            return 0.4
        if exposure_class in list_of_exp_class:
            return 0.3 * k_c
        else:
            raise ValueError(f"There is no exposure class called {exposure_class}")
        
    def calculate_E_middle(self, Ecm: int, phi_selfload: float, phi_liveload: float, M_SLS: float, 
                           Mg_SLS: float, Mp_SLS: float)-> float:
        ''' Function that calculates E_middle, based on effective elasticity modulus according to EC2 7.4.3(5)
        Args:
            Ecm(int):  elasticity modulus for concrete, from material class [N/mm2]
            phi_selfload(float):  creep number for selfload, from creep class
            phi_liveload(float):  creep number for liveload, from creep class
            Mg_SLS(float):  characteristic selfload moment, from load class[kNm]
            Mp_SLS(float):  characteristic liveload moment, from load class[kNm]
            M_SLS(float):  characteristic total load moment, from load class[kNm]
        Returns:
            Ec_middle(float):  middle elasticity modulus [N/mm2]
        '''
        Ec_eff_selfload = Ecm / (1 + phi_selfload)
        Ec_eff_liveload = Ecm / (1 + phi_liveload)
        Ec_middle = M_SLS / (Mg_SLS / Ec_eff_selfload + Mp_SLS / Ec_eff_liveload)
        return Ec_middle
    
        
    def calculate_alpha(self, Es: int, Ec_middle: float, As: float, width: float, d: float)-> float:
        ''' Function that calculates alpha 
        Args:
            Es(int):  elasiticity modulus for steel, from material class [N/mm2]
            Ec_middle(float):  middle elasticity modulus [N/mm2]
            As(float):  area of reinforcement, from cross section class [mm2]
            width(float):  width of cross-section, defined by user [mm]
            d(float):  effective height, from cross section class [mm]
        Returns:
            alpha(float):  factor for calculating reinforcment stress
        '''
        netta = Es / Ec_middle 
        ro = As / (width * d)
        alpha = np.sqrt((netta * ro) ** 2 + 2 * netta * ro) - netta * ro
        return alpha

    def calculate_reinforcement_stress(self, alpha: float, width: float, d: float, M_Ed: float, Ec_middle: float, 
                                        Es: int, As: float)-> float:
        ''' Function that calculates reinforcement stress
        The cross section is assumed cracked 
        Args: 
            alpha(float):  factor 
            width(float):  width of cross-section, defined by user [mm]
            d(float):  effective height, from cross section class[mm]
            M_Ed(float):  design moment, from load class [kNm]
            Es(int):  elasiticity modulus for steel, from material class [N/mm2]
            Ec_middle(float):  middle elasticity modulus, from longterm-effects class [N/mm2]
            As(float):  area of reinforcement, from cross section class[mm2]
        Returns:
            sigma_p(float):  reinforcement stress [N/mm2]
        '''
        Ic2 = (width * (alpha * d) ** 3) / 3 
        Is2 = As * ((1 - alpha) * d) ** 2
        Ei_2 = Ec_middle * Ic2 + Es * Is2
        sigma_p = Es * (M_Ed * 10 ** 6 * (1 - alpha) * d)/(Ei_2)
        return sigma_p

    def calculate_maximal_bar_diameter(self, w_max: float , sigma_p: float)-> float:
        ''' Function that calculates max bar diameter according to EC2 table 7.2N, using 
        interpolation in two directions. The bar diameters are implemented as a matrix Ø , the reinforcement 
        tension as vector a, and crack width as vector w.
        Args:
            w_max(float):  limit value of crack width [mm]
            sigma_p(float):  reinforcement stress [N/mm2]
        Returns:
            max_bar_diameter(float):  maximum bar diameter to limit crack width [mm]
        '''
        Ø = ([[40, 32, 20, 16, 12, 10, 8, 6],[32, 25, 16, 12, 10, 8, 6, 5],[25, 16, 12, 8, 6, 5, 4, 0]])  #  Bar diameter matrix
        a = [160, 200, 240, 280, 320, 360, 400, 450]  #  Reinforcement tension vector
        w = [0.4, 0.3, 0.2]  #  Crack width vector
        
        for k in range(0,len(w)-1,1):
            if w[k] >= w_max > w[k+1]:
                for i in range(len(a) - 1):
                    x1 = (Ø[k][i+1]-Ø[k][i])/(w[k]-w[k+1])*(w_max-w[k+1])+ Ø[k][i] 
                    x2 = (Ø[k+1][i+1]-Ø[k+1][i])/(w[k]-w[k+1])*(w_max-w[k+1])+ Ø[k+1][i]
                    if a[i] <= sigma_p < a[i + 1]:
                        max_bar_diameter = (x2-x1)/(a[i+1]-a[i])*(sigma_p-a[i]) + x1
                        return max_bar_diameter
            
    def control_of_bar_diameter(self, bar_diameter: float, max_bar_diameter: float)-> bool:
        ''' Control of max bar diameter compared to given bar_diameter
        Args:
            max_bar_diameter(float):  maximum bar diameter to limit crack width [mm]
            bar_diameter(float):  reinforcement diameter, given by user [mm]
        Returns:
            True if given reinforcement diameter is suifficent, or False if its not suifficent
        '''
        if bar_diameter > max_bar_diameter:
            return False
        else: 
            return True
        
    
