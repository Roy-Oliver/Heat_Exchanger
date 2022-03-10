from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QLineEdit, QPushButton, QMessageBox
from PyQt5 import uic
import sys
import main
import traceback

class UI(QMainWindow):

    def __init__(self):
        super(UI, self).__init__()

        # Load UI File
        uic.loadUi("gui.ui", self)

        # Define our widgets
        # Inputs
        self.guess_u = self.findChild(QLineEdit, "guess_u_line")
        self.error = self.findChild(QLineEdit, "error_line")
        self.duty = self.findChild(QLineEdit, "duty_line")
        self.t_in_cold = self.findChild(QLineEdit, "t_in_cold_line")
        self.t_out_cold = self.findChild(QLineEdit, "t_out_cold_line")
        self.flow_cold = self.findChild(QLineEdit, "flow_cold_line")
        self.cp_cold = self.findChild(QLineEdit, "cp_cold_line")
        self.myu_cold = self.findChild(QLineEdit, "myu_cold_line")
        self.rho_cold = self.findChild(QLineEdit, "rho_cold_line")
        self.k_cold = self.findChild(QLineEdit, "k_cold_line")
        self.t_in_hot = self.findChild(QLineEdit, "t_in_hot_line")
        self.t_out_hot = self.findChild(QLineEdit, "t_out_hot_line")
        self.flow_hot = self.findChild(QLineEdit, "flow_hot_line")
        self.cp_hot = self.findChild(QLineEdit, "cp_hot_line")
        self.myu_hot = self.findChild(QLineEdit, "myu_hot_line")
        self.rho_hot = self.findChild(QLineEdit, "rho_hot_line")
        self.k_hot = self.findChild(QLineEdit, "k_hot_line")
        self.fouling_shell = self.findChild(QLineEdit, "fouling_shell_line")
        self.length = self.findChild(QLineEdit, "length_line")
        self.outside_diameter = self.findChild(QLineEdit, "outside_diameter_line")
        self.inside_diameter = self.findChild(QLineEdit, "inside_diameter_line")
        self.fouling_tube = self.findChild(QLineEdit, "fouling_tube_line")
        self.k_tube = self.findChild(QLineEdit, "k_tube_line")
        self.stream_location = self.findChild(QComboBox, "stream_location_box")
        self.baffle_spacing = self.findChild(QComboBox, "baffle_spacing_box")
        self.baffle_cut = self.findChild(QComboBox, "baffle_cut_box")
        self.shell_passes = self.findChild(QComboBox, "shell_passes_box")
        self.head_type = self.findChild(QComboBox, "head_type_box")
        self.pitch = self.findChild(QComboBox, "pitch_box")
        self.tube_passes = self.findChild(QComboBox, "tube_passes_box")

        # Edit Shell Pass and Tube Passes ComboBoxes to be dependent
        self.shell_passes.addItem("",[""])
        self.shell_passes.addItem("1", ["", "2", "4", "6", "8"])
        self.shell_passes.addItem("2", ["", "4", "8", "12"])
        self.shell_passes.activated.connect(self.dep_box)

        # Outputs
        self.u = self.findChild(QLineEdit, "u_line")
        self.mean_temp = self.findChild(QLineEdit, "mean_temp_line")
        self.pressure_tube = self.findChild(QLineEdit, "pressure_tube_line")
        self.velocity_tube = self.findChild(QLineEdit, "velocity_tube_line")
        self.tubes = self.findChild(QLineEdit, "tubes_line")
        self.bundle_diameter = self.findChild(QLineEdit, "bundle_diameter_line")
        self.coefficient_tube = self.findChild(QLineEdit, "coefficient_tube_line")
        self.pressure_shell = self.findChild(QLineEdit, "pressure_shell_line")
        self.velocity_shell = self.findChild(QLineEdit, "velocity_shell_line")
        self.shell_diameter = self.findChild(QLineEdit, "shell_diameter_line")
        self.coefficient_shell = self.findChild(QLineEdit, "coefficient_shell_line")

        # Button
        self.solve = self.findChild(QPushButton, "solve_button")



        # Do main operation when button is clicked
        self.solve.clicked.connect(self.solver)



        # Show the App
        self.show()

    def dep_box(self, index):
        # Makes the shell and tube passes dependent

        # Clear the tubes box
        self.tube_passes.clear()

        # Make it dependent
        self.tube_passes.addItems(self.shell_passes.itemData(index))

    def solver(self):
        try:
            inputs = []

            inputs.append(float(self.guess_u.text()))
            inputs.append(float(self.error.text()))
            inputs.append(float(self.duty.text()))
            inputs.append(float(self.t_in_hot.text()))
            inputs.append(float(self.t_out_hot.text()))
            inputs.append(float(self.t_in_cold.text()))
            inputs.append(float(self.t_out_cold.text()))


            if self.stream_location.currentText() == "Shell":
                inputs.append(float(self.flow_hot.text()))
                inputs.append(float(self.cp_hot.text()))
                inputs.append(float(self.myu_hot.text()))
                inputs.append(float(self.rho_hot.text()))
                inputs.append(float(self.k_hot.text()))

                inputs.append(float(self.flow_cold.text()))
                inputs.append(float(self.cp_cold.text()))
                inputs.append(float(self.myu_cold.text()))
                inputs.append(float(self.rho_cold.text()))
                inputs.append(float(self.k_cold.text()))
            else:
                inputs.append(float(self.flow_cold.text()))
                inputs.append(float(self.cp_cold.text()))
                inputs.append(float(self.myu_cold.text()))
                inputs.append(float(self.rho_cold.text()))
                inputs.append(float(self.k_cold.text()))

                inputs.append(float(self.flow_hot.text()))
                inputs.append(float(self.cp_hot.text()))
                inputs.append(float(self.myu_hot.text()))
                inputs.append(float(self.rho_hot.text()))
                inputs.append(float(self.k_hot.text()))

            if self.head_type.currentText() == "Pull-Through Floating Head":
                inputs.append("PFH")
            elif self.head_type.currentText() == "Split-Ring Floating Head":
                inputs.append("SFH")
            elif self.head_type.currentText() == "Outside Packed Bed":
                inputs.append("OPB")
            else:
                inputs.append("FAU")

            inputs.append(float(self.length.text()))
            inputs.append(float(self.inside_diameter.text()))
            inputs.append(float(self.outside_diameter.text()))
            inputs.append(self.pitch.currentText())
            inputs.append(int(self.tube_passes.currentText()))
            inputs.append(float(self.fouling_tube.text()))
            inputs.append(float(self.k_tube.text()))

            inputs.append(float(self.baffle_spacing.currentText()))
            inputs.append(int(self.baffle_cut.currentText()))
            inputs.append(float(self.fouling_shell.text()))
            inputs.append(int(self.shell_passes.currentText()))

            results = main.main(inputs)

            self.u.setText("{:.3f}".format(results[0]))
            self.mean_temp.setText("{:.3f}".format(results[1]))
            self.pressure_tube.setText("{:.3f}".format(results[2]))
            self.velocity_tube.setText("{:.3f}".format(results[3]))
            self.tubes.setText(f"{results[4]}")
            self.bundle_diameter.setText("{:.3f}".format(results[5]))
            self.coefficient_tube.setText("{:.3f}".format(results[6]))
            self.pressure_shell.setText("{:.3f}".format(results[7]))
            self.velocity_shell.setText("{:.3f}".format(results[8]))
            self.shell_diameter.setText("{:.3f}".format(results[9]))
            self.coefficient_shell.setText("{:.3f}".format(results[10]))

            success_message = QMessageBox()
            success_message.setWindowTitle("Success!")
            success_message.setText("Calculations completed successfully")
            success_message.setIcon(QMessageBox.Information)
            success_message.exec_()


        except:
            error_message = QMessageBox()
            error_message.setWindowTitle("Error")
            error_message.setText(f"An Error Occured! Traceback: \n\n {traceback.format_exc()}")
            error_message.setIcon(QMessageBox.Critical)
            error_message.exec_()

# Initialize the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec()