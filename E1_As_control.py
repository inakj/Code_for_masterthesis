
# EC2 9.2.1.1 
class reinforcement:
    def __init__(self,loading,ULS,cross_section,material):
        self.z = self.calculate_z(loading.M_Ed,ULS.M_Rd,cross_section.d)
        self.necessary = self.calculate_necessary_reinforcement(loading.M_Ed,self.z,material.fyd)
        self.min = self.calculate_As_min(material.fctm,material.fyk,cross_section.width,cross_section.d)
        self.max = self.calculate_As_max(cross_section.Ac)
        self.control = self.check_reinforcement(cross_section.As,self.max,self.min,self.necessary)

    def calculate_z(self,M_Ed,M_Rd,d):
        z = (1 - 0.17 * M_Ed / M_Rd) * d
        return z
    
    def calculate_necessary_reinforcement(self,M_Ed,z,fyd):
        As_necessary = M_Ed * 10**6 / (z * fyd)
        return As_necessary

    def calculate_As_min(self,fctm,fyk,width,d):
        As_min_1 = 0.26 * fctm / fyk * width * d 
        As_min_2 = 0.0013 * width * d 
        
        if As_min_1 > As_min_2:
            As_min = As_min_1
        else: 
            As_min = As_min_2
        return As_min
    
    def calculate_As_max(self,Ac):
        As_max = 0.04 * Ac
        return As_max
    
    def check_reinforcement(self,As,As_max,As_min,As_necessary):
        if As > As_max:
            return f'Reinforcment area is too big!'
        elif As < As_min or As < As_necessary:
            return f'Reinforcment area is too small!'
        else: 
            return f'Reinforcment area is OK!'
        


