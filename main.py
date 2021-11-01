from Tubes import Tubes
from Shell import Shell
from HeatExchanger import HeatExchanger

def main():
    # Input Initial Guess for Overall Coefficient
    U0ass = 10000 # W/m2 K

    # Input duty
    Q = 2233333 # W

    # Input mean temp difference
    DTm = 56.16 # Kelvin

    # Input properties of TUBE Stream
    m_tube_in = 13.8888 # kg/s
    Cp_tube = 2.68 * (10 ** 3) # J/kg K
    mu_tube = 0.684 * (10 ** (-3)) # Pa s
    rho_tube = 763.2 # kg/m3
    k_tube = 0.158 # W/m K

    # Input properties of SHELL Stream
    m_shell_in = 5.56 # kg/s
    Cp_shell = 2.47 * (10 ** 3)  # J/kg K
    mu_shell = 0.43 * (10 ** (-3))  # Pa s
    rho_shell = 730  # kg/m3
    k_shell = 0.132  # W/m K

    # Input properties of TUBES
    head_type = "PFH" # Options: PFH (pull-through floating head), SFH (split-ring floating head), OPB (outside packed bed), FAU (fixed and u-tube)
    L = 4 # m
    di = 0.025 # m
    do = 0.029 # m
    pitch_type = "triangular" # "triangular" or "square"
    tube_passes = 4
    tube_fouling_factor = 1/0.0002 # W/m2 K
    tube_thermal_resistance = 50 # W/m K

    # Input properties of SHELL
    baffle_spacing = 0.2 # As a fraction of shell diameter
    baffle_cut = 25 # in percent. Available 15, 25, 35, 45,
    shell_fouling_factor = 5000 # W/m2 K
    shell_passes = 1

    # Input error threshold for loop calculations (Normally set to 30%)
    error_threshold = 30 # In percentage








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
        print(f"U0 = {HE.U0}")
        print("Tube Side:")
        print(f"   Tube Pressure Drop = {HE.tubes.deltaP}")
        print(f"   Velocity = {HE.tubes.velocity}\n")
        print(f"   Number of tubes = {HE.tubes.nt}")
        print(f"   Bundle Diameter = {HE.tubes.Db}")
        print(f"   Shell Diameter = {HE.Ds}")
        print(f"   Reynolds = {HE.tubes.Re}")
        print(f"   Prandtl = {HE.tubes.Pr}")
        print(f"   jh = {HE.tubes.jh}")
        print(f"   jf = {HE.tubes.jf}")
        print(f"   Tube side coefficient = {HE.tubes.hi}\n")

        print("Shell Side:")
        print(f"   Shell Pressure Drop = {HE.shell.deltaP}")
        print(f"   Velocity = {HE.shell.velocity}\n")
        print(f"   Shell flow area (As) = {HE.shell.As}")
        print(f"   Reynolds = {HE.shell.Re}")
        print(f"   Prandtl = {HE.shell.Pr}")
        print(f"   jh = {HE.shell.jh}")
        print(f"   jf = {HE.shell.jf}")
        print(f"   Shell side coefficient = {HE.shell.hs}\n\n")



if __name__ == "__main__":
    main()
