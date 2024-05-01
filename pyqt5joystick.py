from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QToolButton, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5 import QtCore
import sys

class JoystickWidget(QWidget):
    def __init__(self, parent=None):
        super(JoystickWidget, self).__init__(parent)

        self.field_joystick_up_button = QToolButton()
        self.field_joystick_up_button.setArrowType(QtCore.Qt.UpArrow)
        self.field_joystick_up_button.clicked.connect(self.joystick_up)
        self.field_joystick_up_button.setFixedWidth(75)
        self.field_joystick_down_button = QToolButton()
        self.field_joystick_down_button.setArrowType(QtCore.Qt.DownArrow)
        self.field_joystick_down_button.clicked.connect(self.joystick_down)
        self.field_joystick_down_button.setFixedWidth(75)
        self.field_joystick_right_button = QToolButton()
        self.field_joystick_right_button.setArrowType(QtCore.Qt.RightArrow)
        self.field_joystick_right_button.clicked.connect(self.joystick_right)
        self.field_joystick_right_button.setFixedWidth(75)
        self.field_joystick_left_button = QToolButton()
        self.field_joystick_left_button.setArrowType(QtCore.Qt.LeftArrow)
        self.field_joystick_left_button.clicked.connect(self.joystick_left)
        self.field_joystick_left_button.setFixedWidth(75)

        self.joystick_layout = QVBoxLayout()
        self.joystick_layout.addWidget(self.field_joystick_up_button, alignment=QtCore.Qt.AlignCenter)
        self.joystick_layout_row = QHBoxLayout()
        self.joystick_layout_row.addWidget(self.field_joystick_left_button)
        self.joystick_layout_row.addWidget(self.field_joystick_right_button)
        self.joystick_layout.addLayout(self.joystick_layout_row)
        self.joystick_layout.addWidget(self.field_joystick_down_button, alignment=QtCore.Qt.AlignCenter)

    def get_joystick_layout(self):
        return self.joystick_layout

    def joystick_up(self):
        print("Up")

    def joystick_down(self):
        print("Down")

    def joystick_right(self):
        print("Right")

    def joystick_left(self):
        print("Left")

if __name__ == '__main__':
    # Create main application window
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Using Fusion style for consistency across platforms
    mw = QMainWindow()
    mw.setWindowTitle('Joystick example')

    # Create and set widget layout
    # Main widget container
    cw = QWidget()
    ml = QGridLayout()
    cw.setLayout(ml)
    mw.setCentralWidget(cw)

    # Create joystick
    joystick = JoystickWidget()

    ml.addLayout(joystick.get_joystick_layout(), 0, 0)

    mw.show()

    # Start Qt event loop
    sys.exit(app.exec_())
