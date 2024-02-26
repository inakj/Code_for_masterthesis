
# EC2 7.3.3
import sys
import numpy as np


class capacity_beam_SLS:
    def __init__(self,cross_section,loading,material):
        self.k_c = self.get_factor_k_c(cross_section.cnom,cross_section.c_min_dur)
        self.limit_value = self.get_limit_value(cross_section.exposure_class,self.k_c)
        self.crack_width = self.find_design_crack_width(self.limit_value)
        self.As_min = self.calc_minimum_reinforcement(material.fyk,material.fctm,cross_section.Ac,cross_section.height,loading.N_Ed,loading.q)
        self.control_As = self.check_minimum_reinforcement(self.As_min,cross_section.As)
        self.alpha = self.get_alpha(material.Es,material.Ecm,cross_section.As,cross_section.width,cross_section.d)
        self.sigma_s = self.calc_reinforcement_stress(self.alpha,cross_section.width,cross_section.d,loading.M_Ed,material.Ecm,material.Es)
        self.max_bar_diameter  = self.get_maximal_bar_diameter(self.crack_width,self.sigma_s)
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
                print("There is no exposure class called", exposure_class)
                sys.exit("Script terminated due to an error.")
        
    def find_design_crack_width(self,limit_value):
        round_values = [0.2, 0.3, 0.4]
        crack_width = min(round_values, key=lambda x: abs(x - limit_value))
        return crack_width

    # EC2 7.3.2(2)
    def calc_minimum_reinforcement(self,fyk,fctm,Ac,height,N_Ed,load):
        sigma_s = fyk
        fct_eff = fctm 
        A_ct = Ac #MÅ SJEKKES OPP
        k = 1 # DENNE MÅ ENDRES
        h_new = min(1000, height)
        sigma_c = N_Ed / Ac
        if load > 0:
            k = 0
            if N_Ed > 0:
                k1 = 2.5
            else:
                k1 = 2 * h_new / 3 * height 
        k_c = max(0.4 * (1-sigma_c / (k1 * fct_eff * height / h_new)),1)
        As_min = (k_c * k * fct_eff * A_ct) / sigma_s
        return As_min
    
    def check_minimum_reinforcement(self,As_min,As):
        if As_min < As:
            return f'Reinforcment area is too small!'
        else: 
            return f'Reinforcment area is OK!'
        
    def get_alpha(self,Es,Ecm,As,width,d):
        netta = Es / Ecm # Should probably not use this
        ro = As / (width * d)
        alpha = np.sqrt((netta * ro) ** 2 + 2 * netta * ro) - netta * ro
        return alpha

    def calc_reinforcement_stress(self,alpha,width,d,M_Ed,Ecm,Es):
        I_c = 0.5 * alpha ** 2 * (1 - alpha / 3) * width * d ** 3 ## SE PÅ DENNE
        eps_s = (M_Ed * 10 ** 6 * (1 - alpha) * d) / (Ecm * I_c) 
        sigma_s = Es * eps_s 
        return sigma_s

    def get_maximal_bar_diameter(self,crack_width,sigma_s):
        stress = [160,200,240,280,320,360]
        if crack_width == 0.4:
            k = [40,32,20,16,12,10]
            for i in range(len(stress) - 1):
                if stress[i] <=sigma_s < stress[i + 1]:
                    max_bar_diameter = (k[i + 1] - k[i]) / (stress[i + 1] - stress[i]) * (sigma_s - stress[i]) + k[i]
            return max_bar_diameter 
        elif crack_width == 0.3:
            k = [32,25,16,12,10,8]
            for i in range(len(stress) - 1):
                if stress[i] <= sigma_s < stress[i + 1]:
                    max_bar_diameter  = (k[i + 1] - k[i]) / (stress[i + 1] - stress[i]) * (sigma_s - stress[i]) + k[i]
            return max_bar_diameter 
        elif crack_width == 0.2:
            k = [25,16,12,8,6,5]
            for i in range(len(stress) - 1):
                if stress[i] <= sigma_s < stress[i + 1]:
                    max_bar_diameter  = (k[i + 1] - k[i]) / (stress[i + 1] - stress[i]) * (sigma_s - stress[i]) + k[i]
            return max_bar_diameter 
    
    def control_of_bar_diameter(self,bar_diameter,max_bar_diameter):
        if bar_diameter > max_bar_diameter:
            return f'Bar diameter are too big!'
        else: 
            return f'Bar diameter are suifficient!'






    


    
  
 