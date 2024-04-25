
import numpy as np

# for prestress: assumed stress - prestress 
# reinforcement in top will not affect crack control

class Crack_control_prestressed:
    ''' Class to contain crack control in Service limit state (SLS) for prestressed cross sectino
    All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the 
    book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2 by Svein Ivar Sørensen.
    '''
    def __init__(self, cross_section, load, material, exposure_class: str,
                  stress, bar_diameter: float):
        '''Args:
            cross_section(class):  class that contain all cross-section properties
            material(class):  class that contain all material properties
            load(class):  class that contain all load properties
            exposure_class(string):  exposure class to calculate nominal thickness, defined by user
            creep_number(class):  class that contain creep number phi for self- and liveload
            time_effect(class):  class that contain time effects because of creep, shrink and relaxation
            stress(class):  class that contain stress in cross section
            prestress_bar_diameter(float):  diameter of prestressed rebar, defined by user [mm]

        Returns: 
            k_c(float):  factor that take into consideration the ratio between cnom and cmin,dur
            crack_width(float):  limit value of crack width [mm]
            alpha(float):  factor for calculating reinforcment stress
            sigma(float):  reinforcement stress [N/mm2]
            max_bar_diameter(float):  maximum bar diameter to limit crack width [mm]
            control_bar_diameter(boolean):  control of bar diameter, return True or False
        '''
        self.k_c = self.calculate_kc(cross_section.cnom,cross_section.c_min_dur)
        self.crack_width = self.get_limit_value(exposure_class,self.k_c)
        self.sigma_p = material.fpk - stress.sigma_p_cracked
        self.max_bar_diameter  = self.calculate_maximal_bar_diameter(self.crack_width,self.sigma_p)
        self.control_bar_diameter = self.control_of_bar_diameter(bar_diameter,self.max_bar_diameter)
        self.utilization = self.get_utilization_degree(bar_diameter,self.max_bar_diameter)
        
        
    def calculate_kc(self, cnom: float,c_min_dur: float)-> float: 
        ''' Function that calculate the factor kc according to EC2 NA.7.3.1
        Args: 
            cnom(float):  nominal concrete cover from crosse section class [mm]
            c_min_dur(float):  smallest nominal cover because of environmental effects from section class [mm]
        Returns:
            k_c(float):  factor that take into consideration the ratio between cnom and cmin,dur
        '''
        kc = min(cnom / c_min_dur, 1.3)
        return kc

    def get_limit_value(self, exposure_class: str,k_c: float)-> float:
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
        
    def calculate_maximal_bar_diameter(self, w_max:float , sigma: float)-> float:
        ''' Function that calculates max bar diameter according to EC2 table 7.2N, using 
        interpolation in two directions. The bar diameters are implemented as a matrix Ø , the reinforcement 
        tension as vector a, and crack width as vector w.
        Args:
            w_max(float):  limit value of crack width [mm]
            sigma_pfloat):  reinforcement stress [N/mm2]
        Returns:
            max_bar_diameter(float):  maximum bar diameter to limit crack width [mm]
        '''

        if sigma > 450:
            sigma = None
            max_bar_diameter = None

        else:
            if sigma < 160:
                sigma = 160
            else:
                sigma = sigma
       
            Ø = ([[40, 32, 20, 16, 12, 10, 8, 6],[32, 25, 16, 12, 10, 8, 6, 5],[25, 16, 12, 8, 6, 5, 4, 0]])  #  Bar diameter matrix
            a = [160, 200, 240, 280, 320, 360, 400, 450]  #  Reinforcement tension vector
            w = [0.4, 0.3, 0.2]  #  Crack width vector
        
            for k in range(0,len(w)-1,1):
                if w[k] >= w_max > w[k+1]:
                    for i in range(len(a) - 1):
                        x1 = Ø[k][i] * (w[k+1]-w_max)/(w[k+1]-w[k]) + Ø[k+1][i]* (w_max-w[k])/(w[k+1]-w[k]) 
                        x2 = Ø[k][i+1] * (w[k+1]-w_max)/(w[k+1]-w[k]) + Ø[k+1][i+1]* (w_max-w[k])/(w[k+1]-w[k]) 
                        if a[i] <= sigma < a[i + 1]:
                            max_bar_diameter = x1 * (a[i+1]-sigma) / (a[i+1]-a[i]) + x2 * (sigma-a[i]) / (a[i+1] - a[i])
        return max_bar_diameter
    

    
    def control_of_bar_diameter(self, bar_diameter: float, max_bar_diameter: float)-> bool:
        ''' Control of max bar diameter compared to given bar_diameter
        Args:
            max_bar_diameter(float):  maximum bar diameter to limit crack width [mm]
            bar_diameter(float):  reinforcement diameter, given by user [mm]
        Returns:
            True if given reinforcement diameter is suifficent, or False if its not suifficent
        '''
        if max_bar_diameter == None:
            return (f'The stress is bigger that the maximum, and the crack control could not be executed')
        elif bar_diameter > max_bar_diameter:
            return False
        else: 
            return True
        
    def get_utilization_degree(self,bar_diameter,max_bar_diameter):
        '''
        '''
        if max_bar_diameter == None:
            return (f'The stress is bigger that the maximum, and the crack utilization could not be executed')
        else:
            utilization = (max_bar_diameter / bar_diameter) * 100
            return round(utilization,1)

