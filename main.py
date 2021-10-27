from Tubes import Tubes
from Shell import Shell
from HeatExchanger import HeatExchanger

def main():
    # Input error threshold for loop calculations (Normally set to 30%)
    error_threshold = 30 # In percentage

    # Input properties of TUBE Stream
    m_tube_in = 37.8 # kg/s
    Cp_tube = 1.989 * (10 ** 3) # J/kg K
    mu_tube = 2.9 * (10 ** (-3)) # Pa s
    rho_tube = 824.95 # kg/m3
    k_tube = 0.137 # W/m K

    # Input properties of SHELL Stream
    m_shell_in = 32.381 # kg/s
    Cp_shell = 2.198 * (10 ** 3)  # J/kg K
    mu_shell = 5.2 * (10 ** (-3))  # Pa s
    rho_shell = 866.60  # kg/m3
    k_shell = 0.119  # W/m K

    # Input properties of TUBES
    head_type = "SFH" # Options: PFH (pull-through floating head), SFH (split-ring floating head), OPB (outside packed bed), FAU (fixed and u-tube)
    k_tube_wall = 45 # W/m K
    L = 4.88 # m
    di = 0.0174 # m
    do = 0.020 # m
    pitch_type = "triangular" # "triangular" or "square"
    tube_passes = 2
    tube_fouling_factor = 1/0.0003 # W/m2 K
    tube_thermal_resistance = 45 # W/m K

    # Input properties of SHELL
    baffle_spacing = 0.7 # As a fraction of shell diameter
    baffle_cut = 25 # in percent. Available 15, 25, 35, 45,
    shell_fouling_factor = 2000 # W/m2 K

    # Input Initial Guess for Overall Coefficient
    U0ass = 300 # W/m2 K

    # Input duty
    Q = 2757004.614 # W

    # Input mean temp difference
    DTm = 84.60





    # Initialize Tubes Object
    he_tubes = Tubes(m_tube_in, Cp_tube, mu_tube, rho_tube, k_tube, head_type, k_tube_wall, L, di, do, pitch_type, tube_passes, tube_fouling_factor, tube_thermal_resistance)

    # Initialize Shell Object
    he_shell = Shell(m_shell_in, Cp_shell, mu_shell, rho_shell, k_shell, baffle_spacing, baffle_cut, shell_fouling_factor)

    # Initialize Heat Exchanger Object
    heat_exchanger = HeatExchanger(he_shell, he_tubes, U0ass, Q, DTm)

    # Solve the Heat Exchanger
    error = 100 # set initial error
    while error > error_threshold:
        U01 = heat_exchanger.U0
        heat_exchanger.solve() # update U0 of heat exchanger
        # Solve for error
        error = (abs(heat_exchanger.U0 - U01) / heat_exchanger.U0) * 100



if __name__ == "__main__":
    main()
