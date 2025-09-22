from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt

class GraphPaperWidget(QWidget):
    """
    A QWidget that draws a light grey background with dark grey grid lines,
    like graph paper.
    """

    def __init__(self, parent=None, grid_spacing=20,
                 bg_color=QColor(220, 220, 220),
                 grid_color=QColor(100, 100, 100)):
        super().__init__(parent)
        self.grid_spacing = grid_spacing
        self.bg_color = bg_color
        self.grid_color = grid_color

    def paintEvent(self, event):
        painter = QPainter(self)
        # Fill background
        painter.fillRect(self.rect(), self.bg_color)

        # Draw grid
        pen = QPen(self.grid_color)
        pen.setWidth(1)
        painter.setPen(pen)

        # Vertical lines
        x = 0
        while x < self.width():
            painter.drawLine(x, 0, x, self.height())
            x += self.grid_spacing

        # Horizontal lines
        y = 0
        while y < self.height():
            painter.drawLine(0, y, self.width(), y)
            y += self.grid_spacing
