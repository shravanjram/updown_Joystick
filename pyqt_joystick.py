import sys
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, QPoint, QRect, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QPainter, QColor

class MiniJoystick(QWidget):
    positionChanged = pyqtSignal(QPoint)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(100, 100)
        self.center = QPoint(50, 50)
        self.radius = 40
        self.thumb_radius = 10
        self.thumb_position = QPoint(self.center)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), Qt.GlobalColor.white)
        painter.setBrush(QColor(100, 100, 100))
        painter.drawEllipse(self.center, self.radius, self.radius)
        painter.setBrush(QColor(50, 50, 50))
        painter.drawEllipse(self.thumb_position, self.thumb_radius, self.thumb_radius)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.updateThumbPosition(event.pos())
            self.positionChanged.emit(self.calculatePosition())

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.updateThumbPosition(event.pos())
            self.positionChanged.emit(self.calculatePosition())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.thumb_position = self.center
            self.update()
            self.positionChanged.emit(self.calculatePosition())

    def updateThumbPosition(self, position):
        delta = position - self.center
        if delta.manhattanLength() <= self.radius:
            self.thumb_position = position
            self.update()

    def calculatePosition(self):
        x = (self.thumb_position.x() - self.center.x()) / self.radius
        y = (self.thumb_position.y() - self.center.y()) / self.radius
        return QPoint(x, y)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MiniJoystick()
    
    def on_position_changed(position):
        print("Joystick Position:", position)

    widget.positionChanged.connect(on_position_changed)
    widget.show()
    sys.exit(app.exec())
