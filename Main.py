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
from D1_Beam_ULS_ikke_ferdig import capacity_beam_ULS
from D2_Beam_SLS_ikke_ferdig import capacity_beam_SLS
from F1_Crack_width_control import crack_control
from E1_As_control import reinforcement


#Material object
materials_instance = Material(input_concrete_class,float(input_steel_class[1:4]))

#Cross section object
cross_section_instance = cross_section_parameters(input_width,input_height,input_nr_bars,input_bar_diameter,input_stirrup_diameter,input_exposure_class)

#Loading object 
loading_instance = design_values(input_distributed_selfload,input_distributed_liveload,input_beam_length) 

crack = crack_control(cross_section_instance,loading_instance,materials_instance)

#beam_crack = crack_control(cross_section_instance,loading_instance,materials_instance)

#beam_ULS = capacity_beam_ULS(cross_section_instance,materials_instance,loading_instance)

# Reinforcement object
#reinforcement_instance = reinforcement(loading_instance,beam_ULS,cross_section_instance,materials_instance)

#beam_SLS = capacity_beam_SLS(cross_section_instance,loading_instance,materials_instance)
"""""
class beam:
    
    def __inti__(self,cross_section,material,loading):
        self.cross = cross_section
        self.material = material
        self.loading = loading

    def calculate_all(self,cross_section,material,loading):
        self.beam_ULS = beam_ULS(cross_section,material,loading)
        self.beam_SLS = beam_SLS(cross_section,material,loading)

    def get_utilization_degree(self):
        self.beam_ULS.utilization_degree_M

#beam1 = beam(cross_section_instance,materials_instance,loading_instance)

"""









