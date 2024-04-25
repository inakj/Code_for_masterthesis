import numpy as np

class Uncracked_stress:

    '''Class to contain calculation of uncracked prestressed
    cross section. All calculations are done according to the standard
    NS-EN 1992-1-1:2004 (abbreviated to EC2).
    '''

    def __init__(self, material, cross_section, load):
        '''Args:
            cross_section(class):  class that contain all cross-section properties
            material(class):  class that contain all material properties
            load(class):  class that contain all load properties 
        Returns:    
            netta(float): factor for material relation
            At(float):  transformed cross section area [mm2]
            yt(float):  distance between reinforced gravity axis and concrete gravity axis [mm]
            It(float):  moment of inertia for tranforsmed cross section [mm4]
            sigma_c_uncracked(float):  concrete stress for uncracked cross section [N/mm2]

        '''
        self.netta = material.Ep / material.Ecm
        self.At = self.calculate_At(cross_section.Ac,self.netta,cross_section.Ap)
        self.yt = self.calculate_yt(self.netta,cross_section.Ap,cross_section.e,self.At)
        self.It = self.calculate_It(cross_section.width,cross_section.height,self.yt,self.netta,cross_section.Ap,cross_section.e)
        self.sigma_c_uncracked = self.calculate_concrete_stress_uncracked(cross_section.height,load.P0,self.At,self.It,self.yt,cross_section.e,load.M_SLS)
       
    def calculate_At(self, Ac: float, netta: float, Ap: float)-> float:
        ''' Function that calculates transformed cross section
        Args:
            Ac(float):  concrete area, from cross section class [mm2]
            netta(float):  factor 
            Ap(float):  area of prestress reinforcement, from cross section class [mm2]
        Returns:
            At(float):  transformed cross section area [mm2]
        '''
        At = Ac + (netta - 1) * Ap
        return At
    
    def calculate_yt(self, netta: float, Ap: float, e: float, At: float)-> float:
        ''' Function that calculates distance yt
        Args: 
            netta(float):  factor
            Ap(float):  area of prestress reinforcement, from cross section class [mm2] 
            e(float):  distance from bottom to prestressed reinforcement [mm]
            At(float):  transformed cross section area [mm2]
        Returns:
            yt(float):  distance between reinforced gravity axis and concrete gravity axis [mm]
        '''
        y_t = ((netta - 1) * Ap * e) / At
        return y_t
    
    def calculate_It(self, width: float, height: float, yt: float, netta: float, Ap: float, e: float)-> float:
        ''' Function that calculates moment of inertia 
        Args: 
            width(float):  width of cross section, from cross section class [mm]
            height(float):  height of cross section, from cross section class [mm]
            yt(float):  distance between reinforced gravity axis and concrete gravity axis [mm]
            netta(float):  factor
            Ap(float):  area of prestress reinforcement, from cross section class [mm2] 
            e(float):  distance from bottom to prestressed reinforcement [mm]
        Returns:
            It(float):  moment of inertia for tranforsmed cross section [mm4]
        '''
        It = (width * height ** 3) / 12 + width * height * yt ** 2 + (netta - 1) * Ap * (e - yt) ** 2
        return It

    def calculate_concrete_stress_uncracked(self, height: float, P0: float, At: float, It: float, yt: float,
                                  e: float, M_SLS: float)-> float:
        ''' Funtion that calculates concrete stress
        Args:
            height(float):  height of cross section, from cross section class [mm]
            P0(float):  prestress force [kN]
            At(float):  transformed cross section area [mm2]
            It(float):  moment of inertia for tranforsmed cross section [mm4]
            yt(float):  distance between reinforced gravity axis and concrete gravity axis [mm]
            e(float):  distance from bottom to prestressed reinforcement [mm]
            Mg_SLS(float):  total moment in SLS [kNm]
        Returns: 
            sigma_c_under:  concrete stress i top of beam [N/mm2]
            sigma_c_over:  concrete stress in bottom of beam [N/mm2]
            sigma_c_prestress:  concrete stress in line with prestress [N/mm2]
        '''
        N = - P0
        Mt =  - P0 * (e - yt) + M_SLS
        y = height / 2
        sigma_c_under = N / At + Mt / (It / (y-yt))
        y = - height / 2
        sigma_c_over = N / At + Mt / (It / (y-yt))
        y = e
        sigma_c_prestress = N / At + Mt / (It / (y-yt))
        sigma_c_uncracked = [sigma_c_under,sigma_c_over,sigma_c_prestress]
        return sigma_c_uncracked

    
