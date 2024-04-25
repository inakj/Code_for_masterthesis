#---------------------------INPUT-------------------------------------

class Input:
    def __init__(self,height,width,case2,case3):
        '''
        All input for the script is given here by the user. 
        The code works for a one span beam, with distributed self and live load. The cross section must be quadratic og rectangular. 
        The ordinary reinforcent must be in one layer. The prestressed reinforcement must also be in one layer.
        All values with a comment are where your input should be. Do not change the code or write something where there is no comments.
        '''
       # Material attributes
        self.concrete_class: str    = 'C45'    # must be given with C + number between 12 and 90
        self.steel_class: str       = 'B500NC' # must be givenin this exact format 
        self.cement_class: str      = 'R'      # must be 'R', 'S' or 'N'
        self.relative_humidity: int  = 40      # relative humidity around beam [%]
        self.exposure_class: str    = 'XC1'   # must be one of the following 
                                               # ['X0','XC1','XC2','XC3','XC4','XD1','XS1','XD2','XD3','XS2','XS3']
        
        # Geometry attributes
        self.width: float        = width #200  # width of cross section [mm]
        self.height: float       = height #500  # height of cross section [mm]
        self.beam_length: float  = 8   # total length of beam [m]

        # Reinforcement attributes
        self.nr_ordinary_reinforcement_bars: int    = 6 # number of ordinary reinforcement bars in longitudinal direction
        self.ordinary_reinforcement_diameter: float = 20 # diameter of ordinary reinforcement bars in longitudinal direction [mm]
        self.stirrup_diameter: float                = 10 # diameter of stirrup diameter / shear reinforcement around the longitudinal bars [mm]
        self.shear_reinforcement: float             = 200 / 125 # shear reinforcement / stirrup reinforcement given as area of 
                                                         # reinforcement divided on distance between stirrups [mm2] / [mm]

        # Load attributes
        self.distributed_selfload: float        = 5 # evenly distributed characteristic selfload [kN/m]
        self.selfload_application: int          = 7 # days after casting when selfload is applied as load in calculation [days]
        self.distributed_liveload: float        = 15 # evenly distributed characteristic liveload [kN/m]
        self.liveload_application: int          = 90 # days after casting when liveload is applied as load in calculation [days]
        self.percent_longlasting_liveload: int  = 40 # part of liveload that is assumed to be longlasting [%]
            
        # Prestressed attributes    
        self.is_the_beam_prestressed: bool            =  case2 #True# if the beam is prestressed, write True here. If not, write False.
        if self.is_the_beam_prestressed              == True:
            self.nr_prestressed_bars: int                 = 4 # number of prestressed reinforcement bars in longitudinal direction
            self.prestressed_reinforcment_diameter: float = 15.2 # diameter of prestressed reinforcement bars in longitudinal direction [mm]
            self.prestressed_reinforcment_name: str       = 'Y1770S7' # name of prestressed reinforcement, if not prestressed, type None
        else:
            self.nr_prestressed_bars: int                 = 0 # number of prestressed reinforcement bars in longitudinal direction
            self.prestressed_reinforcment_diameter: float = 0 # diameter of prestressed reinforcement bars in longitudinal direction [mm]
            self.prestressed_reinforcment_name: str       = None # name of prestressed reinforcement, if not prestressed, type None
       
        self.prestressed_and_ordinary_in_top: bool = case3 #False # if the beam is prestressed, but also have ordinary reinforcement in top, write True here, if not, write False)

#----------------------------------------------------------------------------
