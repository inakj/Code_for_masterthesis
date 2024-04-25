
class Geometry: 
    def __init__(self,width,height):
        self.width = width
        self.height = height
    
    def calculate_area(self):
        return self.width * self.height


Rectangular = Geometry(0.2,0.4)
Quadratic = Geometry(0.2,0.2)


class Material:
    def __init__(self,density):
        self.density = density


Concrete = Material(24) 
Steel = Material(78.5) 

class Beam(Geometry, Material):
    def __init__(self, geometry, material):
        self.geometry = geometry
        self.material = material

    def calculate_self_weight(self):
        area = self.geometry.calculate_area()
        return area * self.material.density

beam_1 = Beam(Rectangular,Concrete)
beam_2 = Beam(Quadratic,Steel)




        
