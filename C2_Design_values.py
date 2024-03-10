
# Making a class to define the design values for the given inputs

class design_values:
    def __init__(self,selfload,liveload,length):
        self.length = length
        self.g = selfload
        self.p = liveload
        self.q = selfload + liveload
        self.g_d = self.g * 1.2
        self.p_d = self.p * 1.5
        self.q_d = self.g_d + self.p_d
        self.M_ULS = self.calculate_M_ULS(self.g_d,self.p_d,length)
        self.M_SLS = self.calculate_M_SLS(self.g,self.p,length)
        self.M1 = self.M_SLS[0]
        self.M2 = self.M_SLS[1]
        self.M_SLS_tot = self.M_SLS[2]
        self.M_Ed = self.M_ULS[2]
        self.V_Ed = self.calculate_V_Ed(self.q_d,length)
        self.N_Ed = self.calculate_N_Ed()
        

    def calculate_M_SLS(self,g,p,length):
        Mg_SLS = (g * length ** 2)/8
        Mp_SLS = (p * length ** 2)/8
        M_SLS_tot = Mg_SLS + Mp_SLS
        M_SLS = [Mg_SLS,Mp_SLS,M_SLS_tot]
        return M_SLS
    
    def calculate_M_ULS(self,g_d,p_d,length):
        Mg_ULS = (g_d * length ** 2)/8
        Mp_ULS = (p_d * length ** 2)/8
        M_ULS_tot = Mg_ULS + Mp_ULS
        M_ULS = [Mg_ULS,Mp_ULS,M_ULS_tot]
        return M_ULS

    # Function to calculate design shear force
    def calculate_V_Ed(self,load,length):
        V_Ed = load * length / 2 
        return V_Ed #kN

    # Function to calculate design axial force
    def calculate_N_Ed(self):
        N_Ed = 0
        return N_Ed #kN
    
test = design_values(5,15,8)

print(test.M_SLS_tot)