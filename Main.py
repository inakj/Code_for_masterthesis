

#---------------------------INPUT-------------------------------------
input_concrete_class:str = 'C45' #must be given with 'C + number'
input_steel_class:str = 'B500NC' #must be given with in this exact way
input_width: float = 200 
input_height: float = 500
input_nr_bars: int = 6
input_bar_diameter: float = 20
input_stirrup_diameter: float = 10
input_distributed_selfload: float = 5 
input_selfload_application: int = 7 #days
input_distributed_liveload: float = 15 #kN/m
input_liveload_application: int = 90 #days
input_percent_longlasting_liveload: int = 40 # %
input_beam_length: float = 8 
input_exposure_class: str = 'XC1'
input_cement_class: str = 'R'
input_RH: int = 40 #%
input_shear_reinforcement: float = 500 #mm2 / mm

input_nr_prestressed_bars: int = 2
input_prestress_diameter: float = 15.2
input_prestress_name: str = 'Y19060S3'
#----------------------------------------------------------------------------

# All relevant scripts

from B1_Material import Material
from B2_Cross_section import Cross_section
from B3_Load import Load_properties
from D1_ULS_nonprestressed import ULS_nonprestressed
from E1_Reinforcement_control import Reinforcement_control
from F1_SLS_Crack_width import Crack_control
from F2_SLS_deflection import Deflection
from F3_Creep_number import Creep_number


class beam:
    def __init__(self):
        # instanced
        self.materials_instance = Material(input_concrete_class,float(input_steel_class[1:4]),input_prestress_name,input_prestress_diameter)
        self.cross_section_instance = Cross_section(input_width,input_height,input_nr_bars,input_bar_diameter,input_stirrup_diameter,input_exposure_class,input_prestress_diameter,input_nr_prestressed_bars,self.materials_instance)
        self.loading_instance = Load_properties(input_distributed_selfload,input_distributed_liveload,input_beam_length,self.materials_instance,self.cross_section_instance)
        self.ULS_nonprestressed_instance = ULS_nonprestressed(self.cross_section_instance,self.materials_instance,self.loading_instance,input_width,input_shear_reinforcement)
        self.SLS_creep_number_nonprestressed_instance = Creep_number(self.cross_section_instance,self.materials_instance,input_selfload_application,input_liveload_application,input_RH,input_cement_class,input_width,input_height,t = 18263)
        self.SLS_crack_nonprestressed_instance = Crack_control(self.cross_section_instance,self.loading_instance,self.materials_instance,input_exposure_class,self.SLS_creep_number_nonprestressed_instance,input_width,input_bar_diameter)
        self.SLS_deflection_nonprestressed_instance = Deflection(self.cross_section_instance,self.materials_instance,self.loading_instance,self.SLS_creep_number_nonprestressed_instance,input_percent_longlasting_liveload,input_beam_length,input_RH,input_cement_class,input_width,input_height)
        self.reinforcement_nonprestressed_instance = Reinforcement_control(self.cross_section_instance,self.materials_instance,self.loading_instance,self.ULS_nonprestressed_instance.alpha_nonprestressed,input_shear_reinforcement,input_width)

        self.M_control = self.control_M(self.ULS_nonprestressed_instance )
        self.V_control = self.control_V(self.ULS_nonprestressed_instance)
        self.As_control = self.control_As(self.reinforcement_nonprestressed_instance)
        self.Asw_control = self.control_Asw(self.reinforcement_nonprestressed_instance)
        self.crack_control = self.control_crack(self.SLS_crack_nonprestressed_instance)
        self.deflection_control = self.control_deflection(self.SLS_deflection_nonprestressed_instance)

    def control_M(self,ULS):
        if ULS.M_control == True:
            return f'Moment capacity is suifficient'
        else:
            return f'Moment capacity is not suifficient'

    def control_V(self,ULS):
        if ULS.V_control == True:
            return f'Shear capacity is suifficient'
        else:
            return f'Shear capacity is not suifficient'
        
    def control_As(self,reinforcement):
        if reinforcement.As_control == True:
            return f'Reinforcement area is suifficient'
        else:
            return f'Reinforcement area is not suifficient'

    def control_Asw(self,reinforcemet):
        if reinforcemet.Asw_control == True:
            return f'Shear reinforcement area is suifficient'
        else:
            return f'Shear reinforcement area is not suifficient'

    def control_crack(self,crack):
        if crack.control_bar_diameter == True:
            return f'Crack width is suifficient'
        else:
            return f'Crack width is not suifficient'

    def control_deflection(self,deflection):
        if deflection.control == True:
            return f'Deflection is suifficient'
        else:
            return f'Deflection is not suifficient'
   

beam_test = beam()

print(beam_test.M_control)
print(beam_test.V_control)
print(beam_test.As_control)
print(beam_test.Asw_control)
print(beam_test.crack_control)
print(beam_test.deflection_control)

