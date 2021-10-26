import math
import numpy as np

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
            data = {"x": [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2], "y": [0.087, 0.088, 0.089, 0.091, 0.092, 0.093, 0.094, 0.095, 0.096, 0.097, 0.098]}
            self.clearance = np.interp(self.Db, data["x"], data["y"])
        elif self.head_type == "SFH":
            data = {"x": [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2], "y": [0.050, 0.053, 0.055, 0.058, 0.061, 0.064, 0.067, 0.069, 0.072, 0.075, 0.078]}
            self.clearance = np.interp(self.Db, data["x"], data["y"])
        elif self.head_type == "OPB":
            data = {"x": [0.2, 1.2], "y": [0.038, 0.038]}
            self.clearance = np.interp(self.Db, data["x"], data["y"])
        elif self.head_type == "FAU":
            data = {"x": [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2], "y": [0.010, 0.011, 0.012, 0.013, 0.014, 0.015, 0.016, 0.017, 0.018, 0.019, 0.020]}
            self.clearance = np.interp(self.Db, data["x"], data["y"])
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
        data = {"x": [10,20,30,40,50,60,70,80,90,100,200,300,400,500,600,700,800,900,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,20000,30000,40000,50000,60000,70000,80000,90000,100000,200000,300000,400000,500000,600000,700000,800000,900000,1000000],
                24: [0.14,0.085,0.066,0.058,0.05,0.043,0.038,0.036,0.034,0.031,0.02,0.016,0.013,0.011,0.0093,0.0085,0.0079,0.0072,0.0068,0.0043,0.0042,0.0041,0.004,0.004,0.0041,0.0042,0.0042,0.0041,0.0038,0.0036,0.0035,0.0033,0.0032,0.003,0.0029,0.0028,0.0028,0.0025,0.0023,0.0022,0.002,0.0019,0.0018,0.0018,0.0018,0.0018],
                48: [0.11,0.069,0.055,0.048,0.04,0.036,0.033,0.029,0.028,0.025,0.016,0.013,0.0099,0.0088,0.0078,0.007,0.0065,0.006,0.0056,0.0037,0.0039,0.004,0.004,0.004,0.0041,0.0042,0.0042,0.0041,0.0038,0.0036,0.0035,0.0033,0.0032,0.003,0.0029,0.0028,0.0028,0.0025,0.0023,0.0022,0.002,0.0019,0.0018,0.0018,0.0018,0.0018],
                120: [0.08,0.053,0.04,0.035,0.03,0.026,0.024,0.023,0.021,0.018,0.013,0.009,0.0077,0.0067,0.0059,0.0053,0.0049,0.0045,0.0042,0.0028,0.0035,0.0039,0.004,0.004,0.0041,0.0042,0.0042,0.0041,0.0038,0.0036,0.0035,0.0033,0.0032,0.003,0.0029,0.0028,0.0028,0.0025,0.0023,0.0022,0.002,0.0019,0.0018,0.0018,0.0018,0.0018],
                240: [0.06,0.039,0.03,0.025,0.022,0.019,0.018,0.016,0.015,0.014,0.0088,0.0067,0.0057,0.0049,0.0043,0.0039,0.0038,0.0034,0.0031,0.002,0.003,0.0035,0.0038,0.004,0.0041,0.0042,0.0042,0.0041,0.0038,0.0036,0.0035,0.0033,0.0032,0.003,0.0029,0.0028,0.0028,0.0025,0.0023,0.0022,0.002,0.0019,0.0018,0.0018,0.0018,0.0018],
                500: [0.045,0.029,0.022,0.019,0.017,0.015,0.014,0.012,0.011,0.0097,0.0064,0.005,0.0042,0.0038,0.0033,0.0029,0.0028,0.0025,0.0023,0.0015,0.0027,0.003,0.0033,0.0036,0.0037,0.0038,0.0039,0.0039,0.0038,0.0036,0.0035,0.0033,0.0032,0.003,0.0029,0.0028,0.0028,0.0025,0.0023,0.0022,0.002,0.0019,0.0018,0.0018,0.0018,0.0018]}
        l_over_di_list = [24, 48, 120, 240, 500]

        # Create list containing jh data for each value of L/di
        y_data = []
        for i in l_over_di_list:
            # get jh data for Re for each value of L/di
            y_data.append(np.interp(self.re, data["x"], data[i]))

        # Interpolate value of jh
        self.jh = np.interp(l_over_di, l_over_di_list, y_data)


