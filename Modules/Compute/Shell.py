import numpy as np
from Modules.Compute.data_sets import jh_shell_data, jf_shell_data

class Shell:
    def __init__(self, m_shell_in, Cp_shell, mu_shell, rho_shell, k_shell, baffle_spacing, baffle_cut, fouling_factor, shell_passes):
        self.m = m_shell_in
        self.Cp = Cp_shell
        self.mu= mu_shell
        self.rho = rho_shell
        self.k = k_shell
        self.baffle_spacing = baffle_spacing
        self.baffle_cut = baffle_cut
        self.hod = fouling_factor
        self.shell_passes = shell_passes

    def solve_velocity(self, shell_diameter, pitch, do):
        # Solves for coefficient in shell side

        # Solve for baffle spacing length
        self.lB = self.baffle_spacing * shell_diameter


        # Solve for shell area
        self.As = (pitch - do) * shell_diameter * self.lB / (pitch * self.shell_passes)

        # Solve for flux
        self.Gs = self.m / self.As

        # Solve for velocity
        self.velocity = self.Gs / self.rho

    def solve_reynolds(self, do, pitch, pitch_type):
        # Solves for the Reynolds number of shell side

        # Solve for equivalent diameter
        if pitch_type == "Triangular":
            self.de = (1.10 / do) * ((pitch ** 2) - 0.917 * (do ** 2))
        elif pitch_type == "Square":
            self.de = (1.27 / do) * ((pitch ** 2) - 0.785 * (do ** 2))

        # Solve for Reynolds number
        self.Re = self.velocity * self.de * self.rho / self.mu

    def solve_coefficient(self):
        # Solves for the shell side heat transfer coefficient

        # Interpolate the jh for shell side
        data = jh_shell_data()
        self.jh = np.interp(self.Re, data[self.baffle_cut][0], data[self.baffle_cut][1])

        # Compute for Prandtl number
        self.Pr = self.Cp * self.mu / self.k

        # Compute for shell side heat transfer coefficient
        self.hs = self.jh * self.Re * (self.Pr ** (1/3)) * self.k / self.de

    def solve_pressure_drop(self, Ds, L):
        # Solves for the shell side pressure drop

        # Interpolate shell jf
        data = jf_shell_data()
        self.jf = np.interp(self.Re, data[self.baffle_cut][0], data[self.baffle_cut][1])

        # Solve for pressure drop
        self.deltaP = (8 * self.jf * (Ds / self.de) * (L / self.lB) * self.rho * (self.velocity ** 2) / 2) * self.shell_passes


