import numpy as np

class Deflection_prestressed:
    '''Class to contain deformation for prestressed cross section.
    All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the 
    book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2 by Svein Ivar Sørensen.
    '''

    def __init__(self, cross_section, material, load, creep_number, factor: float, length: float, 
                 RH: int, cement_class: str, time_effect):
        '''Args:
            cross_section(class):  class that contain all cross-section properties
            material(class):  class that contain all material properties
            load(class):  class that contain all load properties
            creep_number(class):  class that contain creep number phi for self- and liveload
            factor(float):  percentage of live load that is long lasting [%]
            length(float):  length of beam, defined by user [m]
            RH(int):  relative humidity, defined by user [%]
            cement_class(string):  cement class 'N','S' or 'R', defined by user
            time_effect(class):  class that contain time effects because of creep, shrink and relaxation

        Returns:
            Ec_middle(float):  middle elasticity modulus [N/mm2]
            netta(float): factor to calculate alpha
            ro(float): factor to calculate alpha
            alpha_uncracked(float):  factor for uncracked cross section
            EI_1(float):  bending stiffness for uncracked cross section [Nmm2]
            deflection_uncracked(float):  deflection including creep for cracked cross section [mm]
            alpha_cracked(float):  factor for cracked cross section
            EI_2(float):  bending stiffnes for cracked cross section [Nmm2]
            deflection_cracked(float):  deflection including creep for cracked cross section [mm]
            M_cr(float):  crack moment [kNm]
            control_Mcr(float)  True if cracked cross section. False if uncracked cross section
            eps_cd(float):  shrinkage strain due to drying over time
            eps_ca(float):  autogenous shrinkage strain
            eps_cs(float):  total shrinkage strain
            K_s(float):  curvature because of shrinkage [mm-1]
            deflection_shrinkage(float):  delfection only because of shrinkage [mm]
            total_deflection(float):  deflection including both shrinkage and creep, with tension stiffening [mm]
            control_deflection(boolean):  Return true if the deflection is within the limit, and False
            if the deflection is to big
        
        '''
        self.Ec_middle = self.calculate_E_middle(material.Ecm,creep_number.phi_selfload,creep_number.phi_liveload,load.Mg_SLS,load.Mp_SLS,load.M_prestress,time_effect.loss_percentage)
        self.netta = self.calculate_netta(material.Es,self.Ec_middle)
        self.ro = self.calculate_ro(cross_section.As,cross_section.width,cross_section.d)
        self.alpha_uncracked = self.calculate_alpha_uncracked(self.netta,cross_section.Ac,cross_section.height,cross_section.As,cross_section.d)
        self.EI_1 = self.calculate_EI_uncracked(cross_section.width,cross_section.height,self.alpha_uncracked,cross_section.As,cross_section.d,self.Ec_middle,material.Es)
        self.deflection_uncracked = self.calculate_deflection_uncracked(length, load.g_k,load.p_k, factor, self.EI_1)
        self.alpha_cracked = self.calculate_alpha_cracked(self.netta,self.ro)
        self.EI_2 = self.calculate_EI_cracked(self.alpha_cracked,cross_section.width,cross_section.d,self.Ec_middle,cross_section.As,material.Es)
        self.deflection_cracked = self.calculate_deflection_cracked(length,load.g_k,load.p_k,factor,self.EI_2)
        self.M_cr = self.calculate_M_cr(material.fctm,self.Ic1,self.netta,self.Ip1,cross_section.height,self.alpha_cracked,cross_section.d)
        self.control_Mcr = self.control_of_Mcr(self.M_cr,load.M_ULS)
        self.eps_cd0 = self.calculate_eps_cd_0(cement_class,RH,material.fcm)
        self.eps_cd = self.calculate_eps_cd(self.eps_cd0,cross_section.Ac,cross_section.width,cross_section.height)
        self.eps_ca = self.calculate_eps_ca(material.fck)
        self.eps_cs = self.calculate_eps_cs(self.eps_cd,self.eps_ca)
        self.K_s = self.calculate_curvature(self.eps_cs,self.netta,cross_section.As,cross_section.Ac,cross_section.height,cross_section.d,cross_section.width)
        self.deflection_shrinkage = self.calculate_deflection_shrinkage(self.K_s,length)
        self.total_deflection = self.calculate_deflection_tension_stiffening(self.M_cr,load.M_SLS,self.control_Mcr,self.deflection_shrinkage,self.deflection_cracked,self.deflection_uncracked)
        self.control = self.control_deflection(length,self.total_deflection)

    def calculate_E_middle(self, Ecm: int, phi_1: float, phi_2: float,
                           Mg_SLS: float, Mp_SLS: float, M_p: float, loss: float)-> float:
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

    def calculate_netta(self, Ep: int, Ec_middle: float)-> float:
        ''' Function that calculates factor netta
        Args:
            Ep(int):  elasiticity modulus for prestresses reinforcement [N/mm2]
            Ec_middle(float):  middle elasticity modulus [N/mm2]
        Returns:
            netta(float): factor for material relation
        '''
        netta = Ep / Ec_middle 
        return netta
    
    def calculate_ro(self, Ap: float, width: float, d: float)-> float:
        ''' Function that calculates factor ro
        Args:
            Ap(float):  prestress reinforcement area from cross section class[mm2]
            width(float): width from cross section class [mm]
            d(float):  effective height from cross section class[mm]
        Returns:
            ro(float): factor for reinforcement relation
        '''
        ro = Ap / (width * d)
        return ro
    
    def calculate_alpha_uncracked(self, netta: float, Ac: float, h: float, Ap: float, d: float)-> float:
        ''' Function that calculates alpha when cross section is uncracked  
        Args:
            netta(float):  factor
            Ac(float):  concrete area from cross section class [mm2]
            h(float):  height from cross section class [mm]
            Ap(float):  prestressed reinforcement area from cross section class[mm2]
            d(float):  effective height from cross section class[mm]
        Returns:
            alpha_uncracked(float):  factor for uncracked cross section
        '''
        alpha_uncracked = (Ac * 0.5 * h + netta * Ap * d) / (d * (Ac + netta * Ap))
        return alpha_uncracked

    def calculate_EI_uncracked(self, width: float, h: float, alpha: float, Ap: float, d: float, 
                                              Ec_middle: float, Ep: int)-> float:
        ''' Function that calculates bending stiffness when cross section is uncracked 
        Args:
            width(float): width from cross section class [mm]
            h(float):  height from cross section class [mm]
            alpha(float):  factor 
            Ap(float):  prestress reinforcement area from cross section class[mm2]
            d(float):  effective height from cross section class[mm]
            Ec_middle(float):  middle elasticity modulus [N/mm2]
            Ep(int):  elasiticity modulus for prestress reinforcement [N/mm2]
        Returns:
            EI_1(float):  bending stiffness for uncracked cross section [Nmm2]
        '''
        self.Ic1 = (width * h ** 3) / 12 + width * h * (alpha * d - h / 2) ** 2 
        self.Ip1 = Ap * (d - alpha * d) ** 2 
        EI_1 = Ec_middle * self.Ic1 + Ep * self.Ip1 
        return EI_1
    
    def calculate_deflection_uncracked(self, length: float, g: float, p: float, factor: float, EI_1: float)-> float:
        ''' Function that calculates longterm deflection including creep if the cross section is uncracked
        Args:
            length(float):  length of beam, defined by user [m]
            g(float):  design self load, from load class [kN/m]
            p(float):  design live load, from load class [kN/m]
            factor(float):  percentage of live load that is long lasting [%]
            EI_1(float):  bending stiffness for uncracked cross section [Nmm2]
        Returns:
            deflection_uncracked(float):  deflection including creep for cracked cross section [mm]
        '''
        deflection_uncracked = (5 * (g + p * (factor / 100) ) * (length * 1000) ** 4) / (384 * EI_1)
        return deflection_uncracked

    def calculate_alpha_cracked(self, netta: float, ro: float)-> float:
        ''' Function that calculates factor alpha
        Args:
            netta(float):  factor
            ro(float):  factor
        Returns:
            alpha_cracked(float):  factor for cracked cross section
        '''
        alpha_cracked = np.sqrt((netta * ro)** 2 + 2 * netta * ro) - netta * ro
        return alpha_cracked

    def calculate_EI_cracked(self, alpha: float, width: float, d: float, Ec_middle: float,
                                            Ap: float, Ep: int)-> float:
        ''' Function that calculates bending stiffness for cracked cross section 
        Args:
            width(float):  width of cross-section, defined by user [mm]
            height(float):  height of cross-section, defined by user [mm]
            Ec_middle(float):  middle elasticity modulus from longterm-effects class [N/mm2]
            Ap(float):  prestressed reinforcement area from cross section class [mm2]
            Ep(int):  prestress elasiticity modulus from material class [N/mm2]
        Returns:
            EI_2(float):  bending stiffnes for cracked cross section [Nmm2]
        '''
        self.Ic2 = 0.5 * alpha ** 2 * (1 - alpha/3) * width * d ** 3 
        self.Ip2 = Ap * ((1 - alpha) * d) ** 2
        EI_2 = Ec_middle * self.Ic2 + Ep * self.Ip2
        return EI_2
    
    def calculate_deflection_cracked(self, length: float, g: float, p: float, factor: float, EI_2: float)-> float:
        ''' Function that calculates longterm deflection including creep if the cross section is cracked
        Args:
            length(float):  length of beam, defined by user [m]
            g(float):  design self load, from load class [kN/m]
            p(float):  design live load, from load class [kN/m]
            factor(float):  percentage of live load that is long lasting [%]
            EI_2(float):  bending stiffness for cracked cross section [Nmm2]
        Returns:
            deflection_cracked(float):  deflection including creep for cracked cross section [mm]
        '''
        deflection_cracked = (5 * (g + p * factor / 100) * (length * 1000) ** 4) / (384 * EI_2)
        return deflection_cracked

    def calculate_M_cr(self, fctm: float, Ic1: float, netta: float, Ip1: float, h: float,
                        alpha_uncracked: float, d: float)-> float:
        ''' Function that calculates crack moment
        Args: 
            fctm(float):  middlevalue of concrete axial tension strength, from material class [N/mm2]
            Ic1(float):  second moment of inertia for concrete, for uncracked cross section [mm4]
            netta(float):  factor
            Is1(float):  second moment of inertia for steel, for uncracked cross section [mm4]
            h(float): height of cross section, defined by user [mm]
            alpha_uncracked(float):  factor for uncracked cross section
            d(float):  effective height from cross section class [mm]
        Returns:
            M_cr(float):  crack moment [kNm]
        '''
        M_cr = fctm * (Ic1 + netta * Ip1) / (h - alpha_uncracked * d)
        return M_cr * 10 ** (-6)
    
    def control_of_Mcr(self, M_cr: float, M_Ed: float)-> float:
        ''' Function that control crack moment with design moment. The cross section is cracked if the crack moment 
        is smaller than the design moment. Design moment with load factors is used to give a conservative solution 
        Args:
            M_cr(float):  crack moment [kNm]
            M_Ed(float):  design moment in ULS, from load class [kNm]
        Returns:        
            True or False(boolean):  True if cracked cross section. False if uncracked cross section
        '''
        if M_Ed >= M_cr:
            return True
        else:
            return False

    def calculate_eps_cd_0(self, cement_class: str, RH: int, fcm: int)-> float :
        '''Function that calculate nominal free shrinkage strain due to drying according to EC2 B.(1). 
        Args:
            cement_class(string):  cement class 'N','S' or 'R', defined by user. 
            RH(int):  relative humidity, defined by user [%]
            fcm(int):  middlevalue of cylinder compressive strength, from material class [N/mm2]
        Returns:
            eps_cd0(float):  nominal free shrinkage strain due to drying
        Raises:
            ValueError:  checks if the cement class equals R, N or S.
        '''
        if cement_class == 'S':
            alpha_ds1 = 3
            alpha_ds2 = 0.13
        elif cement_class == 'N':
            alpha_ds1 = 4
            alpha_ds2 = 0.12
        elif cement_class == 'R':
            alpha_ds1 = 6
            alpha_ds2 = 0.11
        else:
            raise ValueError(f'cement_class={cement_class}, expected R, N or S')
        fcm0 = 10 
        RH0 = 100
        beta_RH = 1.55 * (1 - (RH / RH0) ** 3)
        eps_cd0 = 0.85 * ((220 + 110 * alpha_ds1) * np.exp(- alpha_ds2 * (fcm/fcm0))) * 10 ** (-6) * beta_RH
        return eps_cd0

    def calculate_eps_cd(self, eps_cd0: float, Ac: float, width: float, height: float)-> float:
        ''' Function that calculates shrinkage strain due to drying over time, according to EC2 3.1.4(5) 
        and table 3.3. 't' is assumed 50 years = 18263 days, and for conservative calculations, its assumed
        t = infintiy, which makes beta_ds = 1. Interpolated table 3.3 to find correct k_h
        Args: 
            eps_cd0(float):  nominal free shrinkage strain due to drying
            Ac(float):  concrete area, from cross section class [mm2]
            width(float):  width of cross section, defined by user [mm]
            height(float):  height of cross section, defined by user [mm]
        Returns:
            eps_cd(float):  shrinkage strain due to drying over time
        '''
        h_0 = 2 * Ac / (2 * width + 2 * height)
        h_0_vector = [100, 200, 300, 500]
        k_h_vector = [1, 0.85, 0.75, 0.7]
        for i in range(len(h_0_vector)-1):
            if h_0_vector[i+1] >= h_0 >= h_0_vector[i]:
                k_h = (k_h_vector[i+1] - k_h_vector[i]) / (h_0_vector[i+1] - h_0_vector[i]) * (h_0 - h_0_vector[i]) + k_h_vector[i]
        beta_ds = 1 
        eps_cd = beta_ds * k_h * eps_cd0
        return eps_cd
    
    def calculate_eps_ca(self, fck: int)-> float:
        ''' Function that calculates autogenous shrinkage strain, according to EC2 3.1.4(5). 
        't' is assumed 50 years = 18263 days, and for conservative calculations, its assumed
        t = infintiy, which makes beta_as = 1. 
        Args: 
            fck(int):  cylinder compression strength, from material class [N/mm2]
        Returns:
            eps_ca(float):  autogenous shrinkage strain
        '''
        beta_as = 1 
        eps_ca_inf = 2.5 * (fck - 10) * 10 ** -6
        eps_ca = beta_as * eps_ca_inf
        return eps_ca

    def calculate_eps_cs(self, eps_cd: float, eps_ca: float)-> float:
        ''' Function that calculate total shrinkage strain, according to EC2 3.1.4(5)
        Args:
            eps_cd(float):  shrinkage strain due to drying over time
            eps_ca(float):  autogenous shrinkage strain
        Returns:
            eps_cs(float):  total shrinkage strain
        '''
        eps_cs = eps_cd + eps_ca 
        return eps_cs
    
    def calculate_curvature(self, eps_cs: float, netta: float, Ap: float, Ac: float, height: float,
                            d: float, width: float)-> float:
        ''' Function that calculate curvatue because of shrinkage
        Args: 
            eps_cs(float):  total shrinkage strain
            netta(float):  factor
            Ap(float):  prestressed reinforcement area, from cross section class [mm2]
            Ac(float):  concrete area, from cross section class [mm2]
            height(float):  height of cross section, defined by user [mm]
            d(float):  effective height, from cross section class [mm]
            width(float):  width of cross section, defined by user [mm]
        Returns: 
            K_s(float):  curvature because of shrinkage [mm-1]
        '''
        a = (Ac * 0.5 * height  + netta * Ap * d) / (Ac + netta * Ap)
        e = d - a
        I = (width * height ** 3) / 12 + width * height * (a - height / 2)**2 + netta * Ap * e**2
        K_s = eps_cs * netta * (Ap * e) / I 
        return K_s
    
    def calculate_deflection_shrinkage(self, K_s: float, length: float)-> float:
        ''' Funtion that calculates deflection only because of shrinkage
        Args:
            K_s(float):  curvature because of shrinkage [mm-1]
            length(float):  length of beam, defined by user [m]
        Returns:
            deflection_shrinkage(float):  delfection only because of shrinkage [mm]
        '''
        deflection_shrinkage = (K_s * (length * 1000) ** 2) / 8
        return deflection_shrinkage
    
    def calculate_deflection_tension_stiffening(self, M_cr: float, M_Ed: float, control: bool, deflection_shrinkage: float,
                                                deflection_cracked: float, deflection_uncracked: float)-> float: 
        ''' Function that calculates total deflection inclding tension stiffening, according to EC2 7.4.3(3)
        Assumed long term load to find beta. The zeta value is depending on if the cross section is cracked or not.
        The deflection because of shrinkage is the same for both cracked and uncracked, but the deflection 
        with creep is different for cracked and uncracked. 
       Args:
            M_cr(float):  crack moment [kNm]
            M_Ed(float):  design moment in ULS, from load class [kNm]
            control(bool): True if cracked cross section. False if uncracked cross section
            deflection_shrinkage(float):  delfection only because of shrinkage [mm]
            deflection_cracked(float):  deflection including creep for cracked cross section [mm]
            deflection_uncracked(float):  deflection including creep for uncracked cross section [mm]
        Returns: 
            total_deflection(float):  deflection including both shrinkage and creep, with tension stiffening [mm]
        '''
        beta = 0.5 
        if control == True: 
            zeta = 1 - beta * (M_cr / M_Ed) ** 2
        elif control == False: 
            zeta = 0
        total_deflection  = zeta * (deflection_cracked + deflection_shrinkage) + \
            (1 - zeta) * (deflection_uncracked + deflection_shrinkage) 
        return total_deflection

    def control_deflection(self, length: float, total_deflection: float)-> bool:
        ''' Function that control max deflection according to EC2 7.4.1(4)
        Args:
            length(float):  length of beam, defined by user [m]
            total_deflection(float):  deflection including both shrinkage and creep [mm]
        Returns:
            True or False(boolean):  Return true if the deflection is within the limit, and False
            if the deflection is to big
        '''
        max_deflection = (length * 1000) / 250 
        if max_deflection > total_deflection:
            return True
        else: 
            return False