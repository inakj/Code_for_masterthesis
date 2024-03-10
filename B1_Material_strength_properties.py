import sys

# This script is based on table 3.1 from the EC2, and givs out all strength
# and deformation properties based on the concrete class
#Last- og materialfaktorer fra EC2 2.4.2.1, 2.4.2.2, og 2.4.2.4


#defining a class for concrete properties
class Material: 
# defining initial values for all properties
    def __init__(self,concrete_class,steel_class): 
        
        #Loadfactors
        self.load_factors = self.get_load_factors()
        self.gamma_shrinkage = self.load_factors[0]
        self.gamma_prestress_favorable = self.load_factors[1]
        self.gamma_prestress_unfavorable = self.load_factors[2]

        #Materialfactors
        self.material_factors = self.get_material_factors()
        self.gamma_concrete = self.material_factors[0]
        self.gamma_reinforcement = self.material_factors[1]
        self.gamma_rebar = self.material_factors[2]

        #Concrete parameters
        self.index = self.get_index(concrete_class)
        self.fck = self.get_fck()
        self.fck_cube = self.get_fck_cube()
        self.fcm = self.get_fcm()
        self.fctm = self.get_fctm()
        self.fctk_005 = self.get_fctk_005()
        self.fctk_095 = self.get_fctk_095()
        self.Ecm = self.get_Ecm()
        self.eps_c1 = self.get_eps_c1()
        self.eps_cu1 = self.get_eps_cu1()
        self.eps_c2 = self.get_eps_c2()
        self.eps_cu2 = self.get_eps_cu2()
        self.n = self.get_n()
        self.eps_c3 = self.get_eps_c3()
        self.eps_cu3 = self.get_eps_cu3()
        self.alfa_cc = 0.85 # NA 3.1.6 ----- Burde denne ligge en annen plass?
        self.alfa_ct = 0.85 # NA 3.1.6 ----- Burde denne ligge en annen plass?
        self.fcd = self.fck * self.alfa_cc / self.gamma_concrete # design compression strength
        self.fctd = self.fctk_005 * self.alfa_ct / self.gamma_concrete # design tension strength

        # Steel parameters
        self.fyk = float(steel_class[1:4])
        self.Es = 2 * 10**5
        self.fyd = self.fyk / self.gamma_reinforcement # design strength
        self.eps_yk = self.fyk / self.Es
        self.eps_yd = self.fyd / self.Es

        # Prestress parameters
        self.fpk = 1860
        self.Fp01k = 115000 
        self.gamma_prestress = 1.15
        self.fpd = self.fpk / self.gamma_prestress
        self.Ep = 1.95 * 10 ** 6
        self.index_prestress = self.get_index(steel_name)


#get loadfactors 
    def get_load_factors(self):
        gamma_shrinkage = 1
        gamma_prestress_favorable = 1.1
        gamma_prestress_unfavorable = 1.3
        return gamma_shrinkage, gamma_prestress_favorable, gamma_prestress_unfavorable

#get materialfactors
    def get_material_factors(self):
        gamma_concrete:float = 1.5
        gamma_reinforcement:float = 1.15
        gamma_rebar:float = 1.15
        return gamma_concrete, gamma_rebar, gamma_reinforcement

# get index number based on concrete class
    def get_index(self,concrete_class): 
        match concrete_class:
            case 'C12':
                return 0
            case 'C16':
                return 1
            case 'C20':
                return 2
            case 'C25':
                return 3
            case 'C30':
                return 4
            case 'C35':
                return 5
            case 'C40':
                return 6
            case 'C45':
                return 7
            case 'C50':
                return 8
            case 'C55':
                return 9
            case 'C60':
                return 10 
            case 'C70':
                return 11
            case 'C80':
                return 12
            case 'C90':
                return 13
            case _:
                print("There is no concrete class called", concrete_class)
                sys.exit("Script terminated due to an error.")
    
# get fck based on index number  
    def get_fck(self):
        fck_vektor = [12,16,20,25,30,35,40,45,50,55,60,70,80,90]
        return fck_vektor[self.index]
    
# get fck_cube based on index number  
    def get_fck_cube(self):
        fck_cube_vektor = [15,20,25,30,37,45,50,55,60,67,75,85,95,105]
        return fck_cube_vektor[self.index]
    
# get fcm based on index number  
    def get_fcm(self):
        fcm_vektor = [20,24,28,33,38,43,48,53,58,63,68,78,88,98]
        return fcm_vektor[self.index]

# get fctm based on index number  
    def get_fctm(self):
        fctm_vektor = [1.6,1.9,2.2,2.6,2.9,3.2,3.5,3.8,4.1,4.2,4.4,4.6,4.8,5.0]
        return fctm_vektor[self.index]

# get fctk0.05 based on index number  
    def get_fctk_005(self):
        fctk_005_vektor = [1.1,1.3,1.5,1.8,2.0,2.2,2.5,2.7,2.9,3.0,3.1,3.2,3.4,3.5]
        return fctk_005_vektor[self.index]
    
# get fctk0.95 based on index number      
    def get_fctk_095(self):
        fctk_095_vektor = [2.0,2.5,2.9,3.3,3.8,4.2,4.6,4.9,5.3,5.5,5.7,6.0,6.3,6.6]
        return fctk_095_vektor[self.index]
    
# get Ecm based on index number  
    def get_Ecm(self):
        Ecm_vektor = [27,29,30,31,33,34,35,36,37,38,39,41,42,44]
        return Ecm_vektor[self.index]*1000 #GPa --> MPa

# get eps_c1 based on index number
    def get_eps_c1(self):
        eps_c1_vektor = [1.8,1.9,2.0,2.1,2.2,2.25,2.3,2.4,2.45,2.5,2.6,2.7,2.8,2.8]
        return eps_c1_vektor[self.index]

# get eps_cu1 based on index number  
    def get_eps_cu1(self):
        eps_cu1_vektor = [3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.2,3.0,2.8,2.8,2.8]
        return eps_cu1_vektor[self.index]

# get eps_c2 based on index number    
    def get_eps_c2(self):
        eps_c2_vektor = [2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.2,2.3,2.4,2.5,2.6]
        return eps_c2_vektor[self.index]

# get eps_cu2 based on index number    
    def get_eps_cu2(self):
        eps_cu2_vektor = [3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.1,2.9,2.7,2.6,2.6]
        return eps_cu2_vektor[self.index]

# get n based on index number    
    def get_n(self):
        n_vektor = [2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,1.75,1.6,1.45,1.4,1.4]
        return n_vektor[self.index]

# get eps_c3 based on index number   
    def get_eps_c3(self):
        eps_c3_vektor = [1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.8,1.9,2.0,2.2,2.3]
        return eps_c3_vektor[self.index]

# get eps_cu3 based on index number    
    def get_eps_cu3(self):
        eps_cu3_vektor = [3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.1,2.9,2.7,2.6,2.6]
        return eps_cu3_vektor[self.index]
    
#PRESTRESSING 
    def get_index(self,steel_name): 
        match steel_name:
            case 'Y19060S3':
                return 0
            case 'Y1860S3':
                return 1
            case 'Y1860S7':
                return 2
            case 'Y1770S7':
                return 3
            case 'Y1860S7G':
                return 4
            case 'Y1820S7G':
                return 5
            case 'Y1700S7G':
                return 6
            case 'Y2160S3':
                return 7
            case 'Y2060S3':
                return 8
            case 'Y1960S3':
                return 9
            case 'Y2160S7':
                return 10 
            case 'Y2060S7':
                return 11
            case 'Y1960S7':
                return 12
            case _:
                print("There is no steel name called", steel_name)
                sys.exit("Script terminated due to an error.")

    def get_steel_diameter(self):
        prestress_diameter = [5.2,6.5,6.8,7.5,7,9,11,12.5,13,15.2,16,15.2,
                              16,18,12.7,15.2,18,5.2,5.2,6.5,6.85,7,9]
        return prestress_diameter[self.index_prestress]
    
    def get_tensile_strength(self): # DU Stoppet her!
        tensile_strength = [1960]
        return tensile_strength[self.index_prestress]

