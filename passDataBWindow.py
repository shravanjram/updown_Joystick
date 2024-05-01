import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QTimer

class JoystickWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.x = 0
        self.y = 0

    def initUI(self):
        # Set up the layout
        layout = QVBoxLayout()

        # Add a label for the joystick widget
        label = QLabel("Joystick Widget")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add the joystick widget
        self.joystick = QWidget()
        self.joystick.setFixedSize(200, 200)
        layout.addWidget(self.joystick, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add a label for the x and y values
        self.xy_label = QLabel("X: 0, Y: 0")
        layout.addWidget(self.xy_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add a text box for x and y values
        self.x_textbox = QLineEdit()
        self.y_textbox = QLineEdit()
        self.x_textbox.setPlaceholderText("X value")
        self.y_textbox.setPlaceholderText("Y value")
        layout.addWidget(self.x_textbox)
        layout.addWidget(self.y_textbox)

        self.setLayout(layout)

        # Set up the timer to update the joystick widget and text boxes
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateValues)
        self.timer.start(100)  # Update every 100 milliseconds

    def paintEvent(self, event):
        painter = QPainter(self.joystick)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw joystick
        painter.setBrush(Qt.GlobalColor.blue)
        painter.drawEllipse(self.x - 10, self.y - 10, 20, 20)

    def updateValues(self):
        # Update x and y values
        self.x = self.mapFromGlobal(QApplication.desktop().cursor().pos()).x() - self.joystick.geometry().center().x()
        self.y = self.mapFromGlobal(QApplication.desktop().cursor().pos()).y() - self.joystick.geometry().center().y()
        self.xy_label.setText(f"X: {self.x}, Y: {self.y}")
        self.x_textbox.setText(str(self.x))
        self.y_textbox.setText(str(self.y))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = JoystickWidget()
    widget.setWindowTitle('Mini Joystick Widget')
    widget.show()
    sys.exit(app.exec())
