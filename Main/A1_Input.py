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
input_nr_prestressed_bars: int = 2
input_prestress_diameter: float = 15.2
input_prestress_name: str = 'Y19060S3'

if input_prestressed == True:
    input_nr_prestressed_bars: int = 2
    input_prestress_diameter: float = 15.2
    input_prestress_name: str = 'Y19060S3'
else:
    input_nr_prestressed_bars: int = 0
    input_prestress_diameter: float = 0
    input_prestress_name: str = None
#----------------------------------------------------------------------------