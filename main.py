from Tubes import Tubes
from Shell import Shell
from HeatExchanger import HeatExchanger

def main():
    # Input Initial Guess for Overall Coefficient
    U0ass = 300 # W/m2 K

    # Input duty
    Q = 1509400 # W

    # Input mean temp difference
    DTm = 71 # Kelvin

    # Input error threshold for loop calculations (Normally set to 30%)
    error_threshold = 30 # In percentage

    # Input properties of TUBE Stream
    m_tube_in = 19.444 # kg/s
    Cp_tube = 2.05 * (10 ** 3) # J/kg K
    mu_tube = 3.2 * (10 ** (-3)) # Pa s
    rho_tube = 820 # kg/m3
    k_tube = 0.134 # W/m K

    # Input properties of SHELL Stream
    m_shell_in = 5.56 # kg/s
    Cp_shell = 2.47 * (10 ** 3)  # J/kg K
    mu_shell = 0.43 * (10 ** (-3))  # Pa s
    rho_shell = 730  # kg/m3
    k_shell = 0.132  # W/m K

    # Input properties of TUBES
    head_type = "SFH" # Options: PFH (pull-through floating head), SFH (split-ring floating head), OPB (outside packed bed), FAU (fixed and u-tube)
    L = 3.5 # m
    di = 0.01483 # m
    do = 0.01905 # m
    pitch_type = "triangular" # "triangular" or "square"
    tube_passes = 4
    tube_fouling_factor = 1/0.00035 # W/m2 K
    tube_thermal_resistance = 55 # W/m K

    # Input properties of SHELL
    baffle_spacing = 0.2764 # As a fraction of shell diameter
    baffle_cut = 25 # in percent. Available 15, 25, 35, 45,
    shell_fouling_factor = 1/0.0002 # W/m2 K
    shell_passes = 1







    # Initialize Tubes Object
    he_tubes = Tubes(m_tube_in, Cp_tube, mu_tube, rho_tube, k_tube, head_type, L, di, do, pitch_type, tube_passes, tube_fouling_factor, tube_thermal_resistance)

    # Initialize Shell Object
    he_shell = Shell(m_shell_in, Cp_shell, mu_shell, rho_shell, k_shell, baffle_spacing, baffle_cut, shell_fouling_factor, shell_passes)

    # Initialize Heat Exchanger Object
    HE = HeatExchanger(he_shell, he_tubes, U0ass, Q, DTm)

    # Solve the Heat Exchanger
    error = 100 # set initial error
    loop_count = 0
    while error > error_threshold:
        U01 = HE.U0
        HE.solve() # update U0 of heat exchanger
        # Solve for error
        error = (abs(HE.U0 - U01) / HE.U0) * 100

        loop_count += 1

    # Print properties
    print(f"Number of Loops = {loop_count}")
    print(f"U0 = {HE.U0}, Tube Pressure Drop = {HE.tubes.deltaP}, Shell Side Pressure Drop = {HE.shell.deltaP}, Tube Number = {HE.tubes.nt}")



if __name__ == "__main__":
    main()
