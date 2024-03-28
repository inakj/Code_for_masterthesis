
import numpy as np 

class time_effects:
    ''' Class to contain losses that is caused by time, including shrink, creep and relaxation. 
    All calculations are done according to the standard
    NS-EN 1992-1-1:2004 (abbreviated to EC2).
    '''
    def __init__(self, material, cross_section, creep_number, uncracked, deflection, load):
        '''Args:
            material(class):  class that contain all material properties
            cross_section(class):  class that contain all cross-section properties
            creep_number(class):  class that contain creep number calculation
            uncracked_concrete(class): class that contain control of prestressed uncracked cross section
            deflection(class):  class that contain all calculations for deflection
            load(class):  class that contain all load properties 
        '''
        self.delta_relaxation = self.calculate_delta_sigma_pr(material.fpk,material.fp01k,cross_section.e)
        self.loss = self.calculate_stress_reduction(deflection.eps_cs,material.Ep,material.Ecm,self.delta_relaxation,creep_number.phi_selfload,uncracked.sigma_c_uncracked[2],
                                               cross_section.Ap,cross_section.Ac,cross_section.Ic,cross_section.e) 
        self.loss_percentage = self.calculate_loss_percentage(self.loss,load.sigma_p_max)
    

    def calculate_delta_sigma_pr(self, fpk: float, fp01k: float, t = 500000) -> float:
        """
        Calculation of loss in stress because of relaxation, where the steel is exposed to constant
        strain for long time, accroding to EC2 3.3.2. Assumed class 2: low relaxation
        Args:
            fpk(float):  characteristic strength for prestress, from material class [N/mm2]
            fp01k(float):  0.1% limit of strength for prestress, from material class [N/mm2]
            t(int):  time after stress-application, assumed t = 500 000 [hours]
           
        Returns:
            delta_sigma_pr(float):  Absolute value of relaxation loss [N/mm2]
        """
        self.sigma_pi = abs(min(0.75 * fpk, 0.85 * fp01k))
        self.ro_1000 = 2.5
        self.my = self.sigma_pi / fpk 
        delta_sigma_pr = self.sigma_pi * (0.66 * self.ro_1000 * np.e ** (9.1 * self.my) * ((t/1000) ** (0.75 * (1 - self.my))) * 10 ** (-5)) 
        return delta_sigma_pr

    def calculate_stress_reduction(self, eps_cs: float, Ep: float, Ecm: float, delta_sigma_pr: float, phi_selfload: float,
                              sigma_c_QP: float, Ap: float, Ac: float, Ic: float, zcp: float) -> float:
        """
        Total time dependant stress reduction in prestress, simplfied from EC2 5.10.6(2)
        Args:
            eps_cs(float):  total shrinkage strain, from deflection class
            Ep(int):  elasticity modulus for prestress [N/mm2]
            Ecm(int):  elasticity modulus for concrete [N/mm2]
            delta_sigma_pr(float):  stressloss because of relaxation [N/mm2]
            phi_selfload(float):  creep number for selfload, from creep number class 
            sigma_c_QP(float):  concrete stress in line with prestress, from uncracked class [N/mm2]
            Ap(float):  area of prestress, from cross section class [mm2]
            Ac(float):  area of concrete, from cross section class [mm2]
            Ic(float):  moment of inertia, from cross section class [mm4]
            zcp(float): eccentricity of prestress, same as e, from cross section class [mm2]
        Return:
            delta_sigma_p(float):  loss in prestress because of shrink, creep and relaxation [N/mm2]
        """
        delta_sigma_p = (eps_cs * Ep + 0.8 * delta_sigma_pr + (Ep / Ecm) * phi_selfload * sigma_c_QP) / \
                (1 + (Ep / Ecm) * (Ap / Ac) * (1 + (Ac / Ic) * zcp ** 2) * (1 + 0.8 * phi_selfload))
        return delta_sigma_p
    
    def calculate_loss_percentage(self, delta_sigma_p: float, sigma_p_max: float)-> float:
        ''' Function that calculate percentage loss because of time effects
        Args: 
            delta_sigma_p(float): reduction in stress [N/mm2]
            sigma_p_max(float):  design value of prestressing stress [N/mm2]
        Returns:
            loss(float):  precentage loss because of shrink, creep and relaxation
        '''
        loss_percentage = (delta_sigma_p * 100) / sigma_p_max
        return loss_percentage