import math
import numpy as np
from data import clearance_data, jh_tube_data

class Tubes:

    def __init__(self, m_tube_in, Cp_tube, mu_tube, rho_tube, k_tube, head_type, k_tube_wall, L, di, do, pitch_type, tube_passes):
        self.m= m_tube_in
        self.Cp = Cp_tube
        self.mu = mu_tube
        self.rho = rho_tube
        self.k = k_tube
        self.head_type = head_type
        self.k_wall = k_tube_wall
        self.L = L
        self.di = di
        self.do = do
        self.pitch_type = pitch_type
        self.tube_passes = tube_passes

    def solve_number_of_tubes(self, A0):
        # Solves for the number of tubes

        # Solve for area of one tube
        area_1_tube = math.pi * self.do * self.L

        # Solve for integer number of tubes. Rounded up
        self.nt = (A0 // area_1_tube) + 1

        # Ensure that the number of tubes is divisible by the number of tube passes
        while self.nt % self.tube_passes != 0:
            self.nt = self.nt + 1

    def solve_velocity(self):
        # Solves for the tube velocity

        # calculate tubes per pass
        tubes_per_pass = self.nt / self.tube_passes

        # Calculate flow area per pass
        flow_area_per_pass = tubes_per_pass * math.pi * (self.di ** 2) / 4

        # Calculate volumetric flow
        volumetric_flow = self.m / self.rho

        # Calculate tube velocity
        self.velocity = volumetric_flow / flow_area_per_pass

    def solve_bundle_diameter(self):
        # Solves for the bundle diameter

        # Get constants from Table 12.4
        if self.pitch_type == "triangular":
            data = {1:[0.319, 2.142], 2:[0.249, 2.207], 4:[0.175, 2.285], 6:[0.0743, 2.499], 8:[0.0365, 2.675]}
            K1, n1 = data[self.tube_passes][0], data[self.tube_passes][1]
        elif self.pitch_type == "square":
            data = {1: [0.215, 2.207], 2: [0.156, 2.291], 4: [0.158, 2.263], 6: [0.0402, 2.617], 8: [0.0331, 2.643]}
            K1, n1 = data[self.tube_passes][0], data[self.tube_passes][1]
        else:
            print("Invalid pitch type")
            exit()

        # Compute bundle diameter
        self.Db = self.do * ((self.nt / K1) **  (1 / n1))

    def solve_clearance(self):
        # Solves for bundle clearance

        # Get clearance from Figure 12.10
        if self.head_type == "PFH":
            data = clearance_data()["PFH"]
            self.clearance = np.interp(self.Db, data[0], data[1])
        elif self.head_type == "SFH":
            data = clearance_data()["SFH"]
            self.clearance = np.interp(self.Db, data[0], data[1])
        elif self.head_type == "OPB":
            data = clearance_data()["OPB"]
            self.clearance = np.interp(self.Db, data[0], data[1])
        elif self.head_type == "FAU":
            data = clearance_data()["FAU"]
            self.clearance = np.interp(self.Db, data[0], data[1])
        else:
            print("Invalid Head Type")
            exit()

    def solve_coefficient(self):
        # Solves for heat transfer coefficient

        # Compute for Reynolds
        self.Re = self.di * self.velocity * self.rho / self.mu

        # Compute for L/Di
        l_over_di = self.L / self.di

        # Compute for jh using FIgure 12.23
        data = jh_tube_data()

        # Create list containing jh data for each value of L/di
        y_data = []
        for i in data.keys():
            # get jh data for Re for each value of L/di
            y_data.append(np.interp(self.Re, data[i][0], data[i][1]))

        # Interpolate value of jh
        self.jh = np.interp(l_over_di, list(data.keys()), y_data)


        # SOlve for Prandtl number
        self.Pr = self.Cp * self.mu / self.k

        # Solve for heat transfer coefficient
        self.hi = self.jh * self.Re * (self.Pr ** 0.33) * self.k / self.di

    def solve_pitch(self):
        # Solves for the pitch length

        self.pitch = 1.25 * self.do




