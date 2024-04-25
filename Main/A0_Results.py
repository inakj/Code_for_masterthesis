
# Imports all relevant scripts

from A0_Input import Input
from B0_Material import Material
from B0_Cross_section import Cross_section
from B0_Load import Load_properties
from C1_ULS import ULS
from D1_Reinforcement import Reinforcement_control
from E1_SLS_Crack import Crack_control
from F1_SLS_Deflection import Deflection
from B0_Creep_number import Creep_number
from D2_Reinforcement import Reinforcement_control_prestressed
from E2_SLS_Crack import Crack_control_prestressed
from F2_SLS_Deflection import Deflection_prestressed
from H2_SLS_Uncracked import Uncracked_stress
from G2_SLS_Cracked import Cracked_Stress
from I2_SLS_Stress import Stress
from J2_Time_effects import time_effects
from C2_ULS import ULS_prestressed
from C3_ULS import ULS_prestress_and_ordinary


class Beam:
    def __init__(self,input):

        self.material_instance = Material(input.concrete_class,(float(input.steel_class[1:4])),input.prestressed_reinforcment_name,input.prestressed_reinforcment_diameter)
        self.cross_section_instance = Cross_section(input.width,input.height,input.nr_ordinary_reinforcement_bars,input.ordinary_reinforcement_diameter,input.stirrup_diameter,input.exposure_class,input.prestressed_reinforcment_diameter,input.nr_prestressed_bars,self.material_instance)
        self.load_instance = Load_properties(input.distributed_selfload,input.distributed_liveload,input.beam_length,self.material_instance,self.cross_section_instance)
        self.creep_instance = Creep_number(self.cross_section_instance,self.material_instance,input.selfload_application,input.liveload_application,input.relative_humidity,input.cement_class)
        self.deflection_instance_1 = Deflection(self.cross_section_instance,self.material_instance,self.load_instance,self.creep_instance,input.percent_longlasting_liveload,input.beam_length,input.relative_humidity,input.cement_class)

    
        if input.is_the_beam_prestressed == True:
            
            self.is_the_beam_prestressed = True
            self.stress_uncracked_instance = Uncracked_stress(self.material_instance,self.cross_section_instance,self.load_instance)
            self.time_effect_instance = time_effects(self.material_instance,self.cross_section_instance,self.creep_instance,self.stress_uncracked_instance,self.deflection_instance_1,self.load_instance)
            self.deflection_instance = Deflection_prestressed(self.cross_section_instance,self.material_instance,self.load_instance,self.creep_instance,input.percent_longlasting_liveload,input.beam_length,input.relative_humidity,input.cement_class,self.time_effect_instance)
            self.stress_cracked_instance = Cracked_Stress(self.material_instance,self.cross_section_instance,self.load_instance,self.deflection_instance,self.time_effect_instance,self.creep_instance)
            self.stress_instance = Stress(self.material_instance,self.deflection_instance,self.stress_uncracked_instance,self.stress_cracked_instance,self.load_instance,self.time_effect_instance)
            self.ULS_instance = ULS_prestressed(self.material_instance,self.load_instance,self.cross_section_instance,self.time_effect_instance,input.shear_reinforcement)
            self.crack_instance = Crack_control_prestressed(self.cross_section_instance,self.load_instance,self.material_instance,input.exposure_class,self.stress_instance,input.ordinary_reinforcement_diameter)
            self.reinforcement_instance = Reinforcement_control_prestressed(self.cross_section_instance,self.material_instance,self.load_instance,self.ULS_instance,input.shear_reinforcement)
        

            self.M_control = self.control_M(self.ULS_instance)
            self.V_control = self.control_V(self.ULS_instance)
            self.As_control = self.control_As(self.reinforcement_instance)
            self.Asw_control = self.control_Asw(self.reinforcement_instance)
            self.crack_control = self.control_crack(self.crack_instance)
            self.deflection_control = self.control_deflection(self.deflection_instance)
            self.stress_control = self.control_stress(self.stress_instance)
            self.concrete_emission = self.calculate_emissinos_concrete(input)
            self.ordinary_reinforcement_emission = self.calculate_emissions_ordinary_reinforcement(self.reinforcement_instance,7700,input)
            self.prestressed_reinforcement_emission = self.calculate_emissions_prestressed_reinforcement(7810,self.cross_section_instance,input)
            self.total_emission = round(self.ordinary_reinforcement_emission + self.prestressed_reinforcement_emission + self.concrete_emission,1)
            self.printed_emission = f'Total emission is {self.total_emission} kg'

            if input.prestressed_and_ordinary_in_top == True:

                self.prestressed_and_ordinary_in_top = True
                self.ULS_instance = ULS_prestress_and_ordinary(self.material_instance,self.load_instance,self.cross_section_instance,self.time_effect_instance,input.shear_reinforcement)
                self.M_control = self.control_M(self.ULS_instance)
                self.V_control = self.control_V(self.ULS_instance)
                self.ordinary_reinforcement_emission = self.calculate_emissions_ordinary_reinforcement(self.reinforcement_instance,7700,input)
                self.prestressed_reinforcement_emission = self.calculate_emissions_prestressed_reinforcement(7810,self.cross_section_instance,input)
                self.total_emission = round(self.ordinary_reinforcement_emission + self.prestressed_reinforcement_emission + self.concrete_emission,1)
                self.printed_emission = f'Total emission is {self.total_emission} kg'
            
        else:
            self.is_the_beam_prestressed = False
            self.prestressed_and_ordinary_in_top = False
            self.ULS_instance = ULS(self.cross_section_instance,self.material_instance,self.load_instance,input.shear_reinforcement)
            self.reinforcement_instance = Reinforcement_control(self.cross_section_instance,self.material_instance,self.load_instance,self.ULS_instance,input.shear_reinforcement)
            self.crack_instance= Crack_control(self.cross_section_instance,self.load_instance,self.material_instance,input.exposure_class,self.creep_instance,input.ordinary_reinforcement_diameter)
            self.deflection_instance = self.deflection_instance_1

            self.M_control = self.control_M(self.ULS_instance)
            self.V_control = self.control_V(self.ULS_instance)
            self.As_control = self.control_As(self.reinforcement_instance)
            self.Asw_control = self.control_Asw(self.reinforcement_instance)
            self.crack_control = self.control_crack(self.crack_instance)
            self.deflection_control = self.control_deflection(self.deflection_instance)
            self.concrete_emission = self.calculate_emissinos_concrete(input)
            self.ordinary_reinforcement_emission = self.calculate_emissions_ordinary_reinforcement(self.cross_section_instance,7700,input)
            self.total_emission = round(self.ordinary_reinforcement_emission + self.concrete_emission,1)
            self.printed_emission = f'Total emission is {self.total_emission} kg'


    def control_M(self,ULS):
        if ULS.M_control == True:
            return f'Moment capacity is suifficient and the utilization degree is {ULS.M_utilization} %'
        else:
            return f'Moment capacity is not suifficient since utilization degree is {ULS.M_utilization} %'
        
    def control_V(self,ULS):
        if ULS.V_control == True:
            return f'Shear capacity is suifficient and the utilization degree is {ULS.V_utilization} %'
        else:
            return f'Shear capacity is not suifficient since the utilization degree is {ULS.V_utilization} %'
        
    def control_As(self,reinforcement):
        if reinforcement.control == True:
            return f'Reinforcement area is suifficient and the utilization degree is {reinforcement.utilization} %'
        else:
            return f'Reinforcement area is not suifficient since the utilization degree is {reinforcement.utilization} %'

    def control_Asw(self,reinforcement):
        if reinforcement.Asw_control == True:
            return f'Shear reinforcement area is suifficient and the utilization degree is {reinforcement.utilization_shear} %'
        else:
            return f'Shear reinforcement area is not suifficient since the utilization degree is {reinforcement.utilization_shear} %'

    def control_crack(self,crack):
        if crack.control_bar_diameter == True:
            return f'Crack width is suifficient and the utiliation degree is {crack.utilization} %'
        else:
            return f'Crack width is suifficient since the utiliation degree is {crack.utilization} %'

    def control_deflection(self,deflection):
        if deflection.control == True:
            return f'Deflection is suifficient and the utilization degree is {deflection.utilization} %'
        else:
            return f'Deflection is not suifficient since the utilization degree is {deflection.utilization} %'
   
    def control_stress(self,stress):
        if stress.control == True:
            return f'Stress is suifficient'
        else:
            return f'Stress is not suifficient'

    def calculate_emissinos_concrete(self,input):
        ''' kg CO2 equivalents for entire beam
        '''
        match input.concrete_class:
            case 'C20':
                return 180 * input.width * input.height * 10 ** -6 * input.beam_length
            case 'C25':
                return 190 * input.width * input.weight * 10 ** -6 * input.beam_length
            case 'C30':
                return 225 * input.width * input.height * 10 ** -6 * input.beam_length
            case 'C35':
                return 240 * input.width * input.height * 10 ** -6 * input.beam_length
            case 'C45':
                return 270 * input.width * input.height * 10 ** -6 * input.beam_length
            case 'C55': 
                return 280 * input.width * input.height * 10 ** -6 * input.beam_length
            case 'C65':
                return 300 * input.width * input.height * 10 ** -6 * input.beam_length
            
    def calculate_emissions_ordinary_reinforcement(self,reinforcement,density_ordinary,input):
        emission = reinforcement.As * 10 ** -6 * density_ordinary * input.beam_length * 0.34
        return emission
    
    def calculate_emissions_prestressed_reinforcement(self,density_prestressed,cross_section,input):
        emission_prestress = cross_section.Ap * 10 ** -6 * input.beam_length * density_prestressed * 1.86
        return emission_prestress 


    
height_1 = 300
width_1 = 200

height_2 = 400
width_2 = 200

height_3 = 500
width_3 = 200

height_4 = 600
width_4 = 200

height_5 = 700
width_5 = 200


input_1 = Input(height_1,width_1,False,False)
input_2 = Input(height_2,width_2,False,False)
input_3 = Input(height_3,width_3,False,False)
input_4 = Input(height_4,width_4,False,False)
input_5 = Input(height_5,width_5,False,False) 

input_6 = Input(height_1,width_1,True,False)
input_7 = Input(height_2,width_2,True,False)
input_8 = Input(height_3,width_3,True,False)
input_9 = Input(height_4,width_4,True,False)
input_10 = Input(height_5,width_5,True,False)

input_11 = Input(height_1,width_1,True,True)
input_12 = Input(height_2,width_2,True,True)
input_13 = Input(height_3,width_3,True,True)
input_14 = Input(height_4,width_4,True,True)
input_15 = Input(height_5,width_5,True,True)

beam_1 = Beam(input_1)
beam_2 = Beam(input_2)
beam_3 = Beam(input_3)
beam_4 = Beam(input_4)
beam_5 = Beam(input_5)

beam_6 = Beam(input_6)
beam_7 = Beam(input_7)
beam_8 = Beam(input_8)
beam_9 = Beam(input_9)
beam_10 = Beam(input_10)

beam_11 = Beam(input_11)
beam_12 = Beam(input_12)
beam_13 = Beam(input_13)
beam_14 = Beam(input_14)
beam_15 = Beam(input_15)


import matplotlib.pyplot as plt

# Example data
moment_utilization_1 = [beam_1.ULS_instance.M_Rd, beam_2.ULS_instance.M_Rd, beam_3.ULS_instance.M_Rd, beam_4.ULS_instance.M_Rd, beam_5.ULS_instance.M_Rd]  # Control measures
total_emission_1 = [beam_1.total_emission, beam_2.total_emission, beam_3.total_emission, beam_4.total_emission, beam_5.total_emission]  # Emission measures

moment_utilization_2 = [beam_6.ULS_instance.M_Rd, beam_7.ULS_instance.M_Rd, beam_8.ULS_instance.M_Rd, beam_9.ULS_instance.M_Rd, beam_10.ULS_instance.M_Rd]  # Control measures
total_emission_2 = [beam_6.total_emission, beam_7.total_emission, beam_8.total_emission, beam_9.total_emission, beam_10.total_emission]  # Emission measures

moment_utilization_3 = [beam_11.ULS_instance.M_Rd, beam_12.ULS_instance.M_Rd, beam_13.ULS_instance.M_Rd, beam_14.ULS_instance.M_Rd, beam_15.ULS_instance.M_Rd]  # Control measures
total_emission_3 = [beam_11.total_emission, beam_12.total_emission, beam_13.total_emission, beam_14.total_emission, beam_15.total_emission]  # Emission measures


# Create scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(moment_utilization_1,total_emission_1, color='blue', marker='o',label= 'Case 1: Ordinary reinforced')  # Plot points
plt.scatter(moment_utilization_2,total_emission_2, color='green', marker='o',label = 'Case 2: Prestressed reinforcement')  # Plot points
plt.scatter(moment_utilization_3,total_emission_3, color='red', marker='o',label = 'Case 3: Ordinary reinforced in top and prestressed in bottom')  # Plot points
plt.title('Moment capacity vs. Total Emission')
plt.xlabel('Moment capcity [kNm]')
plt.ylabel('Total Emission [kg CO2 eq.]')
plt.legend()
plt.grid(True)
plt.show()

'''
if my_beam.is_the_beam_prestressed == True:
    print(my_beam.M_control)
    print(my_beam.V_control)
    print(my_beam.As_control)
    print(my_beam.Asw_control)
    print(my_beam.crack_control)
    print(my_beam.deflection_control)
    print(my_beam.stress_control)
    print(my_beam.total_emission)

elif my_beam.prestressed_and_ordinary_in_top == True:
    print(my_beam.M_control)
    print(my_beam.V_control)
    print(my_beam.total_emission)

else:
    print(my_beam.M_control)
    print(my_beam.V_control)
    print(my_beam.As_control)
    print(my_beam.Asw_control)
    print(my_beam.crack_control)
    print(my_beam.deflection_control)
    print(my_beam.total_emission)
'''







