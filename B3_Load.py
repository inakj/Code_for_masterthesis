

class Load_properties:
    '''Load class to contain load properties used in calculations. 
    All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2)
    '''
    def __init__(self,selfload: float, liveload: float, length: float, material, cross_section):
        '''Args:
            selfload(float):  concrete beam's self weight, defined by user [kN/m]
            liveload(float):  applied load, defined by user [kN/m]
            length(float):  length of beam, defined by user [m]
            material(class):  class that contain all material properties
            cross_section(class): class that contain all cross section properties
        Returns: 
            g_k(float):  characteristic selfload [kN/m]
            p_k(float):  characteristic liveload [kN/m]
            q_k(float):  characteristic load [kN/m]
            g_d(float):  design selfload, including load factor [kN/m]
            p_d(float):  design liveload, including load factor [kN/m]
            q_d(float):  design load, including load factor [kN/m]
            Mg_SLS(float):  max moment in middle of beam because of characteristic selfload [kNm]
            Mp_SLS(float):  max moment in middle of beam because of characteristic liveload [kNm]
            M_SLS(float):  max total moment in middle of beam because of characteristic load [kNm]
            Mg_ULS(float):  max moment in middle of beam because of design selfload [kNm]
            Mp_ULS(float):  max moment in middle of beam because of design live load [kNm]
            M_ULS(float):  max total moment in middle of beam because of design load [kNm]
            V_SLS(float):  max shear force near supports because of characteristic total load [kN]
            V_ULS(float):  max shear force near supports becasue of design total load [kN]
            sigma_p_max(float):  design value of prestressing stress [N/mm2]
            P0_max:   design value of prestressign force [N]

        '''
        self.g_k: float = selfload
        self.p_k: float = liveload
        self.q_k: float = selfload + liveload
        self.g_d: float  = self.g_k * material.gamma_selfload
        self.p_d: float = self.p_k * material.gamma_liveload
        self.q_d: float = self.g_d + self.p_d
        self.Mg_SLS = self.calculate_Mg_SLS(self.g_k,length)
        self.Mp_SLS = self.calculate_Mp_SLS(self.p_k,length)
        self.M_SLS = self.calculate_M_SLS(self.Mg_SLS,self.Mp_SLS)
        self.Mg_ULS = self.calculate_Mg_ULS(self.g_d,length)
        self.Mp_ULS = self.calculate_Mg_ULS(self.p_d,length)
        self.M_ULS = self.calculate_M_ULS(self.Mg_ULS,self.Mp_ULS)
        self.V_SLS = self.calculate_V_SLS(self.q_k,length)
        self.V_ULS = self.calculate_V_ULS(self.q_d,length)
        self.sigma_p_max = self.calculate_sigma_p_max(material.fpk,material.fp01k)
        self.P0_max = self.calculate_P0_max(self.sigma_p_max,cross_section.Ap)
    

    def calculate_Mg_SLS(self,g: float, length: float)-> float:
        ''' Function that calculates Mg_SLS according to table 3.1 
        in "Stålkonstrukjoner; profiler og formler"
        Args:
            g(float):  characteristic selfload [kN/m]
            length(float): length of beam [m]
        Returns:
            Mg_SLS(float):  moment because of characteristic selfload [kNm]
        '''
        Mg_SLS = (g * length ** 2)/8
        return Mg_SLS
    
    def calculate_Mp_SLS(self,p: float, length: float)-> float:
        ''' Function that calculates Mp_SLS according to table 3.1 
        in "Stålkonstrukjoner; profiler og formler"
        Args:
            p(float):  characteristic liveload [kN/m]
            length(float): length of beam [m]
        Returns:
            Mp_SLS(float):  moment because of characteristic liveload [kNm]
        '''
        Mp_SLS = (p * length ** 2)/8
        return Mp_SLS

    def calculate_M_SLS(self,Mg_SLS: float,Mp_SLS: float)-> float:
        ''' Function that calculates M_SLS 
        Args:
            Mg_SLS(float):  moment because of characteristic selfload [kNm]
            Mp_SLS(float):  moment because of characteristic liveload [kNm]
        Returns:
            M_SLS(float):  total moment because of characteristic load [kNm]
        '''
        M_SLS= Mg_SLS + Mp_SLS
        return M_SLS
    
    def calculate_Mg_ULS(self,g: float, length: float):
        ''' Function that calculates Mg_ULS according to table 3.1 
        in "Stålkonstrukjoner; profiler og formler"
        Args:
            g(float):  design selfload [kN/m]
            length(float): length of beam [m]
        Returns:
            Mg_ULS(float):  moment because of design selfload [kNm]
        '''
        Mg_ULS = (g * length ** 2)/8
        return Mg_ULS

    def calculate_Mp_ULS(self,p: float, length: float)-> float:
        ''' Function that calculates Mp_ULS according to table 3.1 
        in "Stålkonstrukjoner; profiler og formler"
        Args:
            p(float):  design liveload [kN/m]
            length(float): length of beam [m]
        Returns:
            Mp_ULS(float):  moment because of design liveload [kNm]
        '''
        Mp_ULS = (p * length ** 2)/8
        return Mp_ULS

    def calculate_M_ULS(self,Mg_ULS: float, Mp_ULS: float)-> float:
        ''' Function that calculates M_SLS
        Args:
            Mg_ULS(float):  moment because of design selfload [kNm]
            Mp_ULS(float):  moment because of design liveload [kNm]
        Returns:
            M_ULS(float):  total moment because of design load [kNm]
        '''
        M_ULS = Mg_ULS + Mp_ULS
        return M_ULS

    def calculate_V_SLS(self,q: float, length: float)-> float:
        ''' Function that calculates V_SLS according to table 3.1 
        in "Stålkonstrukjoner; profiler og formler"
        Args:
            q(float):  total characteristic load [kN/m]
            length(float): length of beam [m]
        Returns:
            V_SLS(float):  shear force because of characteristic load [kNm]
        '''
        V_SLS = q * length / 2 
        return V_SLS #kN
    
    def calculate_V_ULS(self,q: float, length: float)-> float:
        ''' Function that calculates V_ULS according to table 3.1 
        in "Stålkonstrukjoner; profiler og formler"
        Args:
            q(float):  total design load [kN/m]
            length(float): length of beam [m]
        Returns:
            V_ULS(float):  shear force because of design load [kNm]
        '''
        V_ULS = q * length / 2 
        return V_ULS 
    
# ---------------- PRESTRESS VALUES --------------------------------------------

    def calculate_sigma_p_max(self,fpk: float, fp01k: float)-> float:
        ''' Functon that calculates sigma_p_max according to EC2 5.10.2.1(1)
        Args: 
            fpk(int):  tensile strength for prestress from material class [N/mm2]
            fp01k(float): characteristic 0.1% proof force from material class [N/mm2]
        Returns:
            sigma_p_max(float):  design value of prestressing stress [N/mm2]
        '''
        sigma_p_max = min(0.8 * fpk, 0.9 * fp01k)
        return sigma_p_max 
    
    def calculate_P0_max(self,sigma_p_max: float, Ap: float):
        ''' Function that calculates P0_max according to EC2 5.10.2.1(1)
        Args: 
            sigma_p_max(float):  design value of prestressing stress [N/mm2]
            Ap(float):  prestressed reinforcement area in cross section [mm2]
        Returns:
        P0_max(float): design value of prestressign force [N]
        '''
        P0_max = sigma_p_max * Ap
        return P0_max 
    

