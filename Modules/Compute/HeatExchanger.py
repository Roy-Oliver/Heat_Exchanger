import math

class HeatExchanger:
    def __init__(self, Shell, Tubes, U0ass, Q, DTm):
        self.shell = Shell
        self.tubes = Tubes
        self.U0 = U0ass
        self.Q = Q
        self.DTm = DTm

    def solve_heat_transfer_area(self):
        # Solves for the heat transfer area

        self.A0 = self.Q / (self.U0 * self.DTm)

    def solve_shell_diameter(self):
        # Solves for the shell diameter

        self.Ds = self.tubes.Db + self.tubes.clearance


    def solve_Uo(self):
        # Solves for the overall heat transfer coefficient

        self.U0 = (1 / self.shell.hs + 1 / self.shell.hod + self.tubes.do * math.log(self.tubes.do / self.tubes.di) / (2 * self.tubes.kw) + (self.tubes.do / self.tubes.di) * (1 / self.tubes.hid + 1 / self.tubes.hi)) ** (-1)



    def solve(self):
        self.solve_heat_transfer_area()
        self.tubes.solve_number_of_tubes(self.A0)
        self.tubes.solve_velocity()
        self.tubes.solve_bundle_diameter()
        self.tubes.solve_clearance()
        self.solve_shell_diameter()
        self.tubes.solve_coefficient()
        self.tubes.solve_pitch()
        self.shell.solve_velocity(self.Ds, self.tubes.pitch, self.tubes.do)
        self.shell.solve_reynolds(self.tubes.do, self.tubes.pitch, self.tubes.pitch_type)
        self.shell.solve_coefficient()
        self.solve_Uo()
        self.tubes.solve_pressure_drop()
        self.shell.solve_pressure_drop(self.Ds, self.tubes.L)





