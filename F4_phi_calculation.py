import numpy as np
import sys 


class creep_number:
    
    def __init__(self,t0,t,cross_section,material,cement_class,RH):
        #self.lambda_creep = self.calculate_creep_deflection()
        #self.lambda_shrink = self.calculate_shrink_deflection()
        self.h0 = self.calculate_h0(cross_section.Ac,cross_section.width,cross_section.height)
        self.beta_fcm = self.calculate_beta_fcm(material.fcm)
        self.phi_RH = self.calculate_phi_RH(self.h0,material.fcm,RH)
        self.t0_adjusted = self.calculate_t0_adjusted(t0,cement_class)
        self.beta_t0 = self.calculate_beta_t0(self.t0_adjusted)
        self.phi_0 = self.calculate_phi_0(self.phi_RH,self.beta_fcm,self.beta_t0)
        self.beta_c = self.calculate_beta_c(t0,t,RH,self.h0,material.fcm)
        self.phi = self.calcualte_phi(self.phi_0,self.beta_c)
        
    #def calculate_longtime_defletion(lambda_creep,lambda_shrink):
      #  deflection_total = lambda_creep + lambda_shrink
       # return deflection_total 


#------Deflection because of shrink-----   
   # def calculate_shrink_deflection():
         
#------Deflection because of creep-----   

   # def calculate_creep_deflection():


# Annex B: Creep and shrink: finding creepnumber after a given time
    def calcualte_phi(self,phi_0,beta_c): 
        phi = phi_0 * beta_c # B.1
        return phi
    
    def calculate_phi_0(self,phi_RH,beta_fcm,beta_t0): 
        phi_0 = phi_RH * beta_fcm * beta_t0 # B.2
        return phi_0
    
    def calculate_phi_RH(self,h0,fcm,RH): 
        alpha_1 = (35 / fcm) ** 0.7 # B.8c
        alpha_2 = (35 / fcm) ** 0.2 # B.8c
        if fcm <= 35:
            phi_RH = 1 + (1 - RH / 100) / (0.1 * h0 ** (1 / 3)) # B.3a
        else:
            phi_RH = (1 + (1 - RH / 100) / (0.1 * h0 ** (1 / 3)) * alpha_1) * alpha_2 # B.3b
        return phi_RH
    
    def calculate_beta_fcm(self,f_cm): 
        beta_fcm = 16.8 / f_cm**0.5 # B.4
        return beta_fcm
    
    def calculate_beta_t0(self,t0_adjusted): 
        beta_t0 = 1 / (0.1 + t0_adjusted **0.20) # B.5
        return beta_t0

    def calculate_h0(self,Ac,width,height): 
        h0 = (2 * Ac) / (2 * (width + height)) # B.6
        return h0
   
    def calculate_beta_c(self,t0,t,RH,h0,fcm): 
        alpha_3 = (35 / fcm) ** 0.5 # B.8c
        if fcm <= 35:
            beta_H = min(1.5 * (1 + (0.012 * RH) ** 18) * h0 + 250, 1500) # B.8a
        else:
            beta_H = min(1.5 * (1 + (0.012 * RH) ** 18) * h0 + 250 * alpha_3, 1500 * alpha_3) # B 8.b
        beta_c = ((t - t0) / (beta_H + t - t0)) ** 0.3 # B.7
        return beta_c

    def calculate_t0_adjusted(self,t0,cement_class):
        if cement_class == 'S':
            alpha_cement = -1
        elif cement_class == 'N':
            alpha_cement = 0
        elif cement_class == 'R':
            alpha_cement = 1
        else: 
            raise ValueError(f'cement_class={cement_class}, expected R, N or S')
        t0_adjusted = max(t0 * (9 / (2 + t0**1.2) + 1) ** alpha_cement, 0.5) # B.9, noe forenklet
        return t0_adjusted

