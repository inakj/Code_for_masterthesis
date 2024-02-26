#-----------INPUT-------------------
input_concrete_class:str = 'C20' #must be given with 'C + number'
input_steel_class:str = 'B500NC' #must be given with in this exact way
input_width: int = 200 
input_height: int = 500
input_nr_bars: int = 6
input_bar_diameter: int = 20
input_stirrup_diameter: int = 10
input_distributed_load: int = 20 #kN/m
input_beam_length: int = 8 
input_exposure_class:str = 'XC1'
input_axial_force = 0
#-----------------------------------

#class input_parameters:
    #def __init__(self,input):
        #self.concrete_class = input[0]
        #self.steel_class = input[1]
        #self.width = input[2]
        #self.height = input[3]
        #self.nr_bars = input[4]
        #self.bar_diameter = input[5]
        #self.stirrup_diameter = input[6]
        #self.distributed_load = input[7]
        #self.length = input[8]
        #self.exposure_class = input[9]
        #self.N_Ed = input[10]
                        

#inputs = [input_concrete_class,input_steel_class,input_width,input_height,input_nr_bars,input_bar_diameter,input_stirrup_diameter,input_distributed_load,input_beam_length,input_exposure_class,input_axial_force]

#input = input_parameters(inputs)

