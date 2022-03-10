from Tubes import Tubes
from Shell import Shell
from HeatExchanger import HeatExchanger
from scipy import optimize
from TCorrFactor import GetDTM

def main(input):
    # Input Initial Guess for Overall Coefficient
    U0ass = input[0] # W/m2 K

    # Input relative error for U0
    relative_error = input[1] # in decimal

    # Input duty
    Q = input[2] # W

    # Input properties of hot stream
    T1 = input[3] # K
    T2 = input[4] # K

    # Input properties of cold stream
    t1 = input[5] # K
    t2 = input[6] # K

    # Input properties of TUBE Stream
    m_tube_in = input[7] # kg/s
    Cp_tube = input[8] # J/kg K
    mu_tube = input[9] # Pa s
    rho_tube = input[10] # kg/m3
    k_tube = input[11] # W/m K

    # Input properties of SHELL Stream
    m_shell_in = input[12] # kg/s
    Cp_shell = input[13]  # J/kg K
    mu_shell = input[14]  # Pa s
    rho_shell = input[15]  # kg/m3
    k_shell = input[16]  # W/m K

    # Input properties of TUBES
    head_type = input[17] # Options: PFH (pull-through floating head), SFH (split-ring floating head), OPB (outside packed bed), FAU (fixed and u-tube)
    L = input[18] # m
    di = input[19] # m
    do = input[20] # m
    pitch_type = input[21] # "Triangular" or "Square"
    tube_passes = input[22]
    tube_fouling_factor = input[23] # W/m2 K
    tube_thermal_resistance = input[24] # W/m K

    # Input properties of SHELL
    baffle_spacing = input[25] # As a fraction of shell diameter
    baffle_cut = input[26] # in percent. Available 15, 25, 35, 45,
    shell_fouling_factor = input[27] # W/m2 K
    shell_passes = input[28]


    # Compute for true temperature difference
    DTm = GetDTM(T1, T2, t1, t2, shell_passes)

    # Initialize Tubes Object
    he_tubes = Tubes(m_tube_in, Cp_tube, mu_tube, rho_tube, k_tube, head_type, L, di, do, pitch_type, tube_passes, tube_fouling_factor, tube_thermal_resistance)

    # Initialize Shell Object
    he_shell = Shell(m_shell_in, Cp_shell, mu_shell, rho_shell, k_shell, baffle_spacing, baffle_cut, shell_fouling_factor, shell_passes)

    # Initialize Heat Exchanger Object
    HE = HeatExchanger(he_shell, he_tubes, U0ass, Q, DTm)

    def error(U0_old):
        # Obtains the difference between the new U and old U

        # Set the U0 of exchanger to old U and solve
        HE.U0 = U0_old
        HE.solve() # Updates the U0 of the HE object
        U0_new = HE.U0

        # Compute error and return the value
        err = U0_new - U0_old
        return err

    # Set the error to zero using newton's method
    optimize.newton(error, U0ass, rtol=relative_error)

    # Print properties
    output = [HE.U0, DTm, HE.tubes.deltaP, HE.tubes.velocity, HE.tubes.nt, HE.tubes.Db, HE.tubes.hi, HE.shell.deltaP, HE.shell.velocity, HE.Ds, HE.shell.hs]
    return output

# Input Initial Guess for Overall Coefficient
#    U0ass = 600 # W/m2 K

#    # Input relative error for U0
#    relative_error = 0.30 # in decimal

#    # Input duty
#    Q = 4340000 # W

    # Input properties of hot stream
    #    T1 = 368.15 # K
    #    T2 = 313.15 # K

    # Input properties of cold stream
    #    t1 = 298.15 # K
    #    t2 = 313.15 # K

    # Input properties of TUBE Stream
    #    m_tube_in = 68.9 # kg/s
    #    Cp_tube = 4.2 * (10 ** 3) # J/kg K
    #   mu_tube = 0.8 * (10 ** (-3)) # Pa s
    #   rho_tube = 995 # kg/m3
    #   k_tube = 0.59 # W/m K

    #   # Input properties of SHELL Stream
    #   m_shell_in = 27.778 # kg/s
    #   Cp_shell = 2.84 * (10 ** 3)  # J/kg K
    #   mu_shell = 0.34 * (10 ** (-3))  # Pa s
    #   rho_shell = 750  # kg/m3
    #   k_shell = 0.19  # W/m K

    #  # Input properties of TUBES
    #  head_type = "SFH" # Options: PFH (pull-through floating head), SFH (split-ring floating head), OPB (outside packed bed), FAU (fixed and u-tube)
    #  L = 4.83 # m
    #  di = 0.016 # m
    #  do = 0.020 # m
    #  pitch_type = "triangular" # "triangular" or "square"
    #  tube_passes = 2
    # tube_fouling_factor = 3000 # W/m2 K
    # tube_thermal_resistance = 50 # W/m K

    #   # Input properties of SHELL
    #  baffle_spacing = 0.2 # As a fraction of shell diameter
    #  baffle_cut = 25 # in percent. Available 15, 25, 35, 45,
    # shell_fouling_factor = 5000 # W/m2 K
    # shell_passes = 1"
