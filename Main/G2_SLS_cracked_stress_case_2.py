import numpy as np

class Stress_cracked:

    '''Class to contain calculation of cracked prestressed cross section. 
    All calculations are done according to the standard
    NS-EN 1992-1-1:2004 (abbreviated to EC2).
    '''

    def __init__(self, material, cross_section, load, deflection, time_effect, creep_number):
        '''Args:
            cross_section(class):  class that contain all cross-section properties
            material(class):  class that contain all material properties
            load(class):  class that contain all load properties 
            deflection(class):  class that contain deflection control 
            time_effect(class):  class that contain time effects because of shrink, creep and relaxation
            creep_number(class):  class that contain creep number calculations
        Returns:    
            E_middle(float):  Middle elasticity modulus [N/mm2]
            netta(float): factor for material relation
            ro(float):  factor for reinforcemeent relation
            Ns(float):  axial force because of free shrink [kN]
            a(float):  factor for calculating alpha
            alpha(float):  factor for calculating stresses
            sigma_c(float):  stress in concrete top [N/mm2]
        '''
        self.E_middle = self.calculate_E_middle(material.Ecm,creep_number.phi_selfload,creep_number.phi_liveload,load.Mg_SLS,load.Mp_SLS,load.M_prestress,time_effect.loss_percentage)
        self.netta = material.Ep / self.E_middle
        self.ro = cross_section.Ap / (cross_section.width * cross_section.d)
        self.Ns = self.calculate_axial_force(deflection.eps_cs,material.Ep,cross_section.Ap)
        self.a = self.calculate_a(load.Mg_SLS,load.Mp_SLS,load.P0,load.M_prestress,time_effect.loss_percentage,cross_section.e)
        self.alpha = self.calculate_alpha(cross_section.d,cross_section.e,self.a)
        self.sigma_c_cracked = self.calculate_concrete_stress_cracked(cross_section.d,cross_section.width,self.alpha)
       
    def calculate_E_middle(self, Ecm: int, phi_1: float, phi_2: float, Mg_SLS: float, Mp_SLS: float,
                           M_p: float, loss: float)-> float:
        ''' Function that calculates E_middle, based on effective elasticity modulus according to EC2 7.4.3(5)
        Args:
            Ecm(int):  elasticity modulus for concrete [N/mm2]
            phi_1(float):  creep number for selfload from creep class
            phi_2(float):  creep number for liveload from creep class
            Mg_SLS(float):  characteristic selfload moment from load class[kNm]
            Mp_SLS(float):  characteristic liveload moment from load class[kNm]
            M_prestress(float):  moment because of prestressing [kNm]
            loss(float):  loss of prestress because of time effects [%]

        Returns:
            E_middle(float):  middle elasticity modulus [N/mm2]
        '''
        EcL_1 = Ecm / (1 + phi_1)
        EcL_2 = Ecm / (1 + phi_2)
        M1 = Mg_SLS
        M2 = Mp_SLS
        M_prestress = M_p * (1 - loss/100)
        E_middle = (abs(M_prestress) + M1 + M2) / ((abs(M_prestress) + M1)/ EcL_1 + M2 / EcL_2)
        return E_middle
        

    def calculate_axial_force(self, eps_cs: float, Ep: int, Ap: float)-> float:
        ''' Function that calculates acial force in prestress because of free shrink
        Args:
            eps_cs(float):  total shrinkage strain, from deflection class
            Ep(int):  elasticity moduls for prestressed reinforcement
            Ap(float):  area of prestressed reinforcement 
        Returns:
            Ns(float):  axial force in prestress [kN]
        '''
        Ns = eps_cs * Ep * Ap * 10 ** -3
        return Ns
    
    def calculate_a(self, Mg_SLS: float, Mp_SLS: float, P0: float, M_p: float, loss: float,e: float)-> float:
        ''' Function that calculates distance a equal to relation M/N 
        Args:
            Mg_SLS(float):  selfload moment in SLS, from load class [kNm]
            Mp_SLS(float):  liveload moment in SLS, from load class [kNm]
            P0(float):   design value of prestressign force [N]
            M_p(float):   moment because of prestressing included losses [kNm]
            loss(float):  loss of prestress because of time effects [%]
            e(float):  distance from bottom to prestressed reinforcement [mm]
        Returns:
            a(float):  factor for calculating alpha
        '''
        self.N = P0 * 10 ** -3 - self.Ns 
        self.M_prestress = M_p * (1 - loss/100)
        self.M = Mg_SLS + Mp_SLS + self.M_prestress + (self.Ns * e * 10**-3) 
        a = self.M/self.N 
        return a * 10 ** 3
    
    def calculate_alpha(self, d: float, e: float, a: float)-> float:
        ''' Function that calculates factor alpha, using abc formula for a third degree 
        equation
        Args:
            d(float):  effective height, from cross section class[mm]
            e(float):  distance to reinforcement, from cross section class [mm]
            a(float):  factor
        Returns:
            alpha(float):  factor
        '''
        coefficients = [d / (6 * (e + a)), 0.5 * (1 - d / (e + a)), self.netta * self.ro, - self.netta * self.ro] 
        roots = np.roots(coefficients)
        for num in roots:
            if 0 < num < 1:
                alpha = float(num)
        return alpha
    
    def calculate_concrete_stress_cracked(self, d: float, width: float,alpha: float)-> float:
        ''' Function that calculates concrete stress in top of cross section
        Args:
            d(float):  effective height, from cross section class[mm]
            width(float):  width of cross section, defined by user [mm]
        Returns:
            sigma_c(float):  concrete stress in top [N/mm2]
        '''
        sigma_c_cracked = (self.N * 10 ** 3) / (width * d * (0.5 * alpha - self.netta * self.ro * (1 - alpha)/alpha))
        return sigma_c_cracked
    
   
   
