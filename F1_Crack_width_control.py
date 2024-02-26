# EC2 7.3.3

import numpy as np

class crack_control:

    def __init__(self,cross_section,loading,material):
        self.k_c = self.get_factor_k_c(cross_section.cnom,cross_section.c_min_dur)
        self.crack_width = self.get_limit_value(cross_section.exposure_class,self.k_c)
        self.As_min = self.calc_minimum_reinforcement(material.fyk,material.fctm,cross_section.Ac,cross_section.height,loading.N_Ed,loading.q)
        self.control_As = self.check_minimum_reinforcement(self.As_min,cross_section.As)
        self.alpha = self.get_alpha(material.Es,material.Ecm,cross_section.As,cross_section.width,cross_section.d)
        self.sigma = self.calc_reinforcement_stress(self.alpha,cross_section.width,cross_section.d,loading.M_Ed,material.Ecm,material.Es,cross_section.As)
        self.max_bar_diameter  = self.get_maximal_bar_diameter(self.crack_width,self.sigma)
        self.control_bar_diameter = self.control_of_bar_diameter(cross_section.bar_diameter,self.max_bar_diameter)
        
        
    def get_factor_k_c(self,cnom,c_min_dur): 
        k_c = min(cnom / c_min_dur, 1.3)
        return k_c

    # table NA.7.1N for only reinforced cross sections with no prestressing
    def get_limit_value(self,exposure_class,k_c): 
        list_of_exp_class = ['XC1','XC2','XC3','XC4','XD1','XD2','XD3','XS1','XS2','XS3']
        if exposure_class == 'X0':
            return 0.4
        if exposure_class in list_of_exp_class:
            return 0.3 * k_c
        else:
            raise ValueError(f"There is no exposure class called {exposure_class}")
        

    # EC2 7.3.2(2)
    def calc_minimum_reinforcement(self,fyk,fctm,Ac,height,N_Ed,q):
        sigma_s = fyk
        fct_eff = fctm 
        A_ct = Ac #MÅ ENDRES 
        k = 1 # DENNE MÅ ENDRES
        h_new = min(1000, height)
        sigma_c = N_Ed / Ac
        if N_Ed > 0:
            k1 = 2.5
        else:
            k1 = 2 * h_new / 3 * height 
        k_c = max(0.4 * (1-sigma_c / (k1 * fct_eff * (height / h_new))),1)
        As_min = (k_c * k * fct_eff * A_ct) / sigma_s
        return As_min
    
    def check_minimum_reinforcement(self,As_min,As):
        if As_min > As:
            return f'Reinforcment area is too small!'
        else: 
            return f'Reinforcment area is OK!'
        
    def get_alpha(self,Es,Ecm,As,width,d):
        netta = Es / Ecm 
        ro = As / (width * d)
        alpha = np.sqrt((netta * ro) ** 2 + 2 * netta * ro) - netta * ro
        return alpha

    def calc_reinforcement_stress(self,alpha,width,d,M_Ed,Ecm,Es,As):
        Ic2 = width * (alpha * d) ** 3 / 3 ## opprisset
        Is2 = As * ((1 - alpha) * d) ** 2
        Ei_2 = Ecm * Ic2 + Es * Is2
        sigma = Es * (M_Ed * 10 ** 6 * (1 - alpha) * d)/(Ei_2)
        return sigma

# doing a linear interpolation

    def get_maximal_bar_diameter(self,w_max,a_max):
        Ø = ([[40,32,20,16,12,10,8,6],[32,25,16,12,10,8,6,5],[25,16,12,8,6,5,4,0]]) # Bar diameter matrix
        a = [160,200,240,280,320,360,400,450] # Reinforcement tenson vector
        w = [0.4,0.3,0.2] # Crack width vector
        
        for k in range(0,len(w)-1,1):
            if w[k] >= w_max > w[k+1]:
                for i in range(len(a) - 1):
                    x1 = (Ø[k][i+1]-Ø[k][i])/(w[k]-w[k+1])*(w_max-w[k+1])+ Ø[k][i] 
                    x2 = (Ø[k+1][i+1]-Ø[k+1][i])/(w[k]-w[k+1])*(w_max-w[k+1])+ Ø[k+1][i]
                    if a[i] <= a_max < a[i + 1]:
                        max_bar_diameter = (x2-x1)/(a[i+1]-a[i])*(a_max-a[i]) + x1
                        return max_bar_diameter
                    else:
                        return None
                        print(f'There is no max diameter for sigma ={self.sigma}')
                    

    def control_of_bar_diameter(self,bar_diameter,max_bar_diameter):
        if max_bar_diameter == None:
            return None
        elif bar_diameter > max_bar_diameter:
            return f'Bar diameter are too big!'
        else: 
            return f'Bar diameter are suifficient!'
        
    
#-----------INPUT-------------------
input_concrete_class:str = 'C20' #must be given with 'C + number'
input_steel_class:str = 'B500NC' #must be given with in this exact way
input_width: int = 200 
input_height: int = 500
input_nr_bars: int = 6
input_bar_diameter: int = 20
input_stirrup_diameter: int = 10
input_distributed_load: int = 20 #kN/m
input_beam_length: int = 8 
input_exposure_class:str = 'XC1'
input_axial_force = 0
#-------------------------------------

# import relevant scripts

from C2_Design_values import design_values
from B1_Material_strength_properties import Material
from C1_Cross_section import cross_section_parameters
from D1_Beam_ULS_ikke_ferdig import capacity_beam_ULS
from D2_Beam_SLS_ikke_ferdig import capacity_beam_SLS
from F1_Crack_width_control import crack_control
from E1_As_control import reinforcement


#Material object
materials_instance = Material(input_concrete_class,float(input_steel_class[1:4]))

#Cross section object
cross_section_instance = cross_section_parameters(input_width,input_height,input_nr_bars,input_bar_diameter,input_stirrup_diameter,input_exposure_class)

#Loading object 
tall:int = 4
loading_instance = design_values(input_distributed_load,input_beam_length,tall) 

crack = crack_control(cross_section_instance,loading_instance,materials_instance)


print(crack.max_bar_diameter)
