
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

input_prestressed: bool = True

if input_prestressed == True:
    input_nr_prestressed_bars: int = 2
    input_prestress_diameter: float = 15.2
    input_prestress_name: str = 'Y1770S7'
else:
    input_nr_prestressed_bars: int = 0
    input_prestress_diameter: float = 0
    input_prestress_name: str = None

#----------------------------------------------------------------------------

# All relevant scripts

from B1_Material import Material
from B2_Cross_section import Cross_section
from B3_Load import Load_properties
from C1_ULS_case_1 import ULS_nonprestressed
from D1_Reinforcement_case_1 import Reinforcement_control
from E1_SLS_Crack_case_1 import Crack_control
from F1_SLS_deflection_case_1 import Deflection
from F0_Creep_number import Creep_number
from D2_Reinforcement_case_2 import Reinforcement_control_prestressed
from E2_SLS_Crack_case_2 import Crack_control_prestressed
from F2_SLS_deflection_case_2 import Deflection_prestressed
from G3_SLS_uncracked_stress_case_2 import Stress_uncracked
from G2_SLS_cracked_stress_case_2 import Stress_cracked
from Main.G1_SLS_stress import Stress
from G0_time_effects import time_effects
from C2_ULS_case_2 import ULS_prestress


class beam:
    def __init__(self):

        material_instance = Material(input_concrete_class,float(input_steel_class[1:4]),input_prestress_name,input_prestress_diameter)
        cross_section_instance = Cross_section(input_width,input_height,input_nr_bars,input_bar_diameter,input_stirrup_diameter,input_exposure_class,input_prestress_diameter,input_nr_prestressed_bars,material_instance)
        load_instance = Load_properties(input_distributed_selfload,input_distributed_liveload,input_beam_length,material_instance,cross_section_instance)
        creep_instance = Creep_number(cross_section_instance,material_instance,input_selfload_application,input_liveload_application,input_RH,input_cement_class,input_width,input_height)
        Deflection_instance_1 = Deflection(cross_section_instance,material_instance,load_instance,creep_instance,input_percent_longlasting_liveload,input_beam_length,input_RH,input_cement_class,input_width,input_height)

        if input_prestressed == True:
            
            stress_uncracked_instance = Stress_uncracked(material_instance,cross_section_instance,load_instance,input_width,input_height)
            time_effect_instance_2 = time_effects(material_instance,cross_section_instance,creep_instance,stress_uncracked_instance,Deflection_instance_1,load_instance)
            Deflection_instance_2 = Deflection_prestressed(cross_section_instance,material_instance,load_instance,creep_instance,input_percent_longlasting_liveload,input_beam_length,input_RH,input_cement_class,input_width,input_height,time_effect_instance_2)
            stress_cracked_instance = Stress_cracked(material_instance,cross_section_instance,load_instance,input_width,Deflection_instance_2,time_effect_instance_2,creep_instance)
            Stress_instance_2 = Stress(material_instance,Deflection_instance_2,stress_uncracked_instance,stress_cracked_instance,load_instance,time_effect_instance_2)
            ULS_instance_2 = ULS_prestress(material_instance,load_instance,cross_section_instance,input_width,time_effect_instance_2)
            reinforcement_instance_2 = Reinforcement_control_prestressed(cross_section_instance,material_instance,load_instance,input_shear_reinforcement,input_width,ULS_instance_2)
            #crack_instance_2 = Crack_control_prestressed(cross_section_instance,load_instance,material_instance,input_exposure_class,creep_instance,time_effect_instance_2,input_width,Stress_instance_2,input_prestress_diameter)

            self.M_control = self.control_M(ULS_instance_2)
            self.V_control = self.control_V(ULS_instance_2)
            self.As_control = self.control_As(reinforcement_instance_2)
            self.Asw_control = self.control_Asw(reinforcement_instance_2)
            #self.crack_control = self.control_crack(crack_instance_2)
            self.deflection_control = self.control_deflection(Deflection_instance_2)
            self.stress_control = self.control_stress(Stress_instance_2)
            
        else:

            ULS_instance_1 = ULS_nonprestressed(cross_section_instance,material_instance,load_instance,input_width,input_shear_reinforcement)
            Reinforcment_instance_1 = Reinforcement_control(cross_section_instance,material_instance,load_instance,ULS_instance_1,input_shear_reinforcement,input_width)
            Crack_instance_1 = Crack_control(cross_section_instance,load_instance,material_instance,input_exposure_class,creep_instance,input_width,input_bar_diameter)
    

            self.M_control = self.control_M(ULS_instance_1)
            self.V_control = self.control_V(ULS_instance_1)
            self.As_control = self.control_As(Reinforcment_instance_1)
            self.Asw_control = self.control_Asw(Reinforcment_instance_1)
            self.crack_control = self.control_crack(Crack_instance_1)
            self.deflection_control = self.control_deflection(Deflection_instance_1)

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
        if reinforcement.control == True:
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
   
    def control_stress(self,stress):
        if stress.control == True:
            return f'Stress is suifficient'
        else:
            return f'Stress is not suifficient'



beam_test = beam()


if input_prestressed == True:
    print(beam_test.M_control)
    print(beam_test.V_control)
    print(beam_test.As_control)
    print(beam_test.Asw_control)
    #print(beam_test.crack_control)
    print(beam_test.deflection_control)
    print(beam_test.stress_control)
else:
    print(beam_test.M_control)
    print(beam_test.V_control)
    print(beam_test.As_control)
    print(beam_test.Asw_control)
    print(beam_test.crack_control)
    print(beam_test.deflection_control)

