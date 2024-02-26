
from typing import Any
import numpy as np
import sys

# This script is based on table 3.1 from the EC2, and givs out all strength
# and deformation properties based on the concrete class

# Defining a class for the cross section
class cross_section_parameters:

    def __init__(self,width,height,nr_bars,bar_diameter,stirrup_diameter,exposure_class):
        self.width = width
        self.height = height
        self.nr_bars = nr_bars
        self.stirrup_diameter = stirrup_diameter
        self.bar_diameter = bar_diameter
        self.exposure_class = exposure_class
        self.Ac = width * height
        self.c_min_b = self.get_c_min_b(bar_diameter)
        self.c_min_dur = self.get_c_min_dur(exposure_class,self.c_min_b)
        self.cnom = self.calculate_cnom(self.c_min_b,self.c_min_dur)
        self.d = self.get_d(height,self.cnom,bar_diameter,stirrup_diameter)
        self.As = self.calculate_As(bar_diameter,nr_bars)
        self.I = self.calculate_I(height,width)
        

    
    def get_c_min_b(self,bar_diameter):
        c_min_b = max(bar_diameter,10) # minimal cover based on bonding
        return c_min_b

    def get_c_min_dur(self,exposure_class,c_min_b):
        # Table NA 4.4.N, assuming 50 years
        if exposure_class == 'X0':
            c_min_dur = c_min_b
        elif exposure_class == 'XC1':
            c_min_dur = 15
        elif exposure_class in ['XC2','XC3','XC4']:
            c_min_dur = 25
        elif exposure_class in ['XD1','XS1','XD2','XD3','XS2']:
            c_min_dur = 40
        elif exposure_class == 'XS3':
            c_min_dur = 50
        else:
            print("There is no exposure class called",exposure_class,'and therefor no value for c.min.dur')
            sys.exit("Script terminated due to an error.")   
        return c_min_dur

    # Function that calculas nominal cover based on exposure class 
    def calculate_cnom(self,c_min_b,c_min_dur):
        c_min = max(c_min_b,c_min_dur,10) # 4.4.1.2
        delta_c_dev = 10 # NA.4.4.1.3
        cnom = c_min + delta_c_dev #4.4.1.1
        return cnom #mm


    # Function that calculates how much longditual reinforcement the cross section has
    def calculate_As(self,bar_diameter,nr_bars): 
        As = (0.5 * bar_diameter) ** 2 * np.pi * nr_bars
        return As #mm2

    # Function that finds the distance between top and reinforcement 
    def get_d(self,height,cnom,bar_diameter,stirrup_diameter): 
        d = height - cnom - 0.5 * bar_diameter - stirrup_diameter
        return d #mm
    
    def calculate_I(self,height,width):
        I = height * width ** 3 / 12
        return I #mm4
    
# defining a instance beam that uses the class 

test = cross_section_parameters(200,500,6,20,10,'XC1')

print(test.d)

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