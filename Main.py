#-----------INPUT-------------------
input_concrete_class:str = 'C20' #must be given with 'C + number'
input_steel_class:str = 'B500NC' #must be given with in this exact way
input_width: int = 200 
input_height: int = 500
input_nr_bars: int = 6
input_bar_diameter: int = 20
input_stirrup_diameter: int = 10
input_distributed_selfload: int = 5 #kN/m
input_selfload_application: int = 7 #days
input_distributed_liveload: int = 15 #kN/m
input_liveload_application: int = 90 #days
input_percent_longlasting_liveload: float = 40 # %
input_beam_length: int = 8 
input_exposure_class:str = 'XC1'
input_axial_force = 0
input_cement_class = 'R'
input_RH = 40 #%
#-------------------------------------

# import relevant scripts

from C2_Design_values import design_values
from B1_Material_strength_properties import Material
from C1_Cross_section import cross_section_parameters
from D1_Beam_ULS import capacity_beam_ULS
from F1_Crack_width_control import crack_control
from E1_As_control import reinforcement
from F3_Deflection_short_time import deflection_shorttime
from F2_Deflection_longterm import deflection_longtime 
from F2_Deflection_longterm import creep_deflection
from F2_Deflection_longterm import shrink_deflection
from F4_phi_calculation import creep_number


#Material object
materials_instance = Material(input_concrete_class,float(input_steel_class[1:4]))

#Cross section object
cross_section_instance = cross_section_parameters(input_width,input_height,input_nr_bars,input_bar_diameter,input_stirrup_diameter,input_exposure_class)

#Loading object 
loading_instance = design_values(input_distributed_selfload,input_distributed_liveload,input_beam_length) 

# ULS object
ULS = capacity_beam_ULS(cross_section_instance,materials_instance,loading_instance)

#Crack-control object
crack = crack_control(cross_section_instance,loading_instance,materials_instance)

# Deflection object
deflection_short_time = deflection_shorttime(loading_instance,cross_section_instance,materials_instance)

t1 = input_selfload_application
t2 = input_liveload_application
t = 18263 # 50 years
factor = input_percent_longlasting_liveload
cement_class = input_cement_class
RH = input_RH

phi_t1 = creep_number(t1,t,cross_section_instance,materials_instance,cement_class,RH)

phi_t2 = creep_number(t2,t,cross_section_instance,materials_instance,cement_class,RH)

creep = creep_deflection(loading_instance,cross_section_instance,materials_instance,phi_t1,phi_t2,factor)

shrink = shrink_deflection(cement_class,materials_instance,RH,loading_instance,creep,cross_section_instance)

deflection_long_time = deflection_longtime(shrink,creep,cross_section_instance)

class beam:
    
    def __init__(self,crack,deflection_short_time,deflection_long_time,ULS):
        self.crack = crack
        self.deflection_short_time = deflection_short_time
        self.deflection_long_time = deflection_long_time
        self.ULS = ULS

    def controll_all_SLS(self):
        self.crack_control = crack.control_bar_diameter
        self.control_shorttime_deflection = deflection_short_time.control
        self.control_longtime_deflection = deflection_long_time.control

    def controll_all_ULS(self,ULS):
        self.M_and_V_control  = ULS.control

control = beam(crack,deflection_short_time,deflection_long_time,ULS)


#beam1 = beam(cross_section_instance,materials_instance,loading_instance)

print(cross_section_instance.cnom)