
import numpy as np

from F2_Deflection_with_creep import creep_deflection
from B1_Material_strength_properties import Material


class shrink_deflection:

    def __init__(self,cement_class,material,RH,load,creep,cross_section):
            self.eps_cd0 = self.calculate_eps_cd0(cement_class,material.fck,RH,material.fcm)
            self.eps_cd = self.calculate_eps_cd(self.eps_cd0,cross_section.Ac,cross_section.width,cross_section.height)
            self.eps_ca = self.calculate_eps_ca(material.fck)
            self.shrink_strain = self.calculate_strain(self.eps_cd,self.eps_ca)
            self.curvature = self.calculate_shrink_curvature(self.eps_cs,creep.netta,cross_section.As,cross_section.Ac,cross_section.height,cross_section.d,cross_section.width)
            self.deflection = deflection(self.curvature,load.length)

    def calculate_eps_cd0(cement_class,fck,RH,fcm):

        if cement_class == 'N':

            eps_cd_0_matrix = [[0.62,0.48,0.38,0.30,0.27],[0.58,0.46,0.36,0.28,0.25],[0.49,0.38,0.30,0.24,0.21],[0.30,0.24,0.19,0.15,0.13],[0.17,0.13,0.10,0.08,0.07],[0,0,0,0,0]] 
            fck_vector = [20,40,60,80,90] 
            RH_vector = [20,40,60,80,90,100] 

        for k in range(len(RH_vector)):
            if RH_vector[k+1] >= RH > RH_vector[k]:
                for i in range(len(fck_vector)):
                    x1 = (eps_cd_0_matrix[k+1][i]-eps_cd_0_matrix[k][i])/(RH_vector[k+1]-RH_vector[k])*(RH-RH_vector[k])+ eps_cd_0_matrix[k][i] 
                    x2 = (eps_cd_0_matrix[k+1][i+1]-eps_cd_0_matrix[k][i+1])/(RH_vector[k+1]-RH_vector[k])*(RH-RH_vector[k])+ eps_cd_0_matrix[k][i+1]
                    if fck_vector[i] <= fck < fck_vector[i + 1]:
                        eps_cd0 = (x2-x1)/(fck_vector[i+1]-fck_vector[i])*(fck-fck_vector[i]) + x1
                        return eps_cd0
        
        else:
            eps_cd0 = 0.85 * ((220 + 110 * alpha_ds1) * np.exp(- alpha_ds2 * fcm/fcm0)) * 10 ** -6 * beta_RH
            beta_RH = 1.55 (1 - (RH / RH0) ** 3)
            fcm0 = 10 
            RH0 = 100
            if cement_class == 'S':
                alpha_ds1 = 3
                alpha_ds2 = 0.13
            elif cement_class == 'R':
                alpha_ds1 = 6
                alpha_ds2 = 0.11
            return eps_cd0

    def calculate_eps_cd(self,eps_cd0,Ac,width,height):
        eps_cd = beta_ds * k_h * eps_cd0
        h_0 = 2 * Ac / (2 * width + 2 * height)
        h_0_vector = [100,200,300,500]
        k_h_vector = [1,0.85,0.75,0.7]
        for i in range(len(h_0_vector)-1):
            if h_0_vector[i+1] >= h_0 >= h_0_vector[i]:
                k_h = (k_h_vector[i+1] - k_h_vector[i]) / (h_0_vector[i+1] - h_0_vector[i]) * (h_0 - h_0_vector[i]) + k_h_vector[i]
        beta_ds = 1 # assumed t--> infitity / 18263
        return eps_cd
    
    def calculate_eps_ca(self,fck):
        eps_ca = beta_as * eps_ca_inf
        eps_ca_inf = 2.5 * (fck - 10) * 10 ** -6
        beta_as = 1 # assumed t --> infinity
        return eps_ca


    def calculate_strain(self,eps_cd,eps_ca):
        eps_cs = eps_cd + eps_ca # where this is strain for drying and autogenous
        return eps_cs
    
    def calculate_shrink_curvature(self,eps_cs,netta,As,Ac,height,d,width):
        K_s = eps_cs * netta * As * e / I 
        e = d - a
        a = (Ac * 0.5 * height  + netta * As * d) / (Ac + netta * As)
        I = (width * height ** 3) / 12 + width * height * (a - height / 2)**2 + netta * As * e**2
        return K_s
    
    #forenklet: K_s = eps_cs / d

    def deflection(self,K_s,length):
        deflection_shrink = (K_s * (length * 1000)**2)/8
        return deflection_shrink

