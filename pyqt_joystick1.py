import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt, QTimer

class JoystickWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.x = 0
        self.y = 0

    def initUI(self):
        self.setWindowTitle('Mini Joystick Widget')
        self.setGeometry(100, 100, 300, 300)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setText("Move the joystick")
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.textbox_x = QLineEdit(self)
        self.textbox_x.setReadOnly(True)
        self.textbox_y = QLineEdit(self)
        self.textbox_y.setReadOnly(True)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel('X:'))
        hbox.addWidget(self.textbox_x)
        hbox.addWidget(QLabel('Y:'))
        hbox.addWidget(self.textbox_y)

        self.layout.addLayout(hbox)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)  # Update every 100 milliseconds

        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw joystick
        painter.setBrush(Qt.GlobalColor.blue)
        painter.drawEllipse(self.x - 10, self.y - 10, 20, 20)

        # Update x and y values in the textboxes
        self.textbox_x.setText(str(self.x))
        self.textbox_y.setText(str(self.y))

    def mouseMoveEvent(self, event):
        self.x = event.x()
        self.y = event.y()
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = JoystickWidget()
    sys.exit(app.exec())
