from PySide import QtGui
from PySide import QtCore

FONT_STRETCH = 0.90  # TODO : unify !!


class ButtonsWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.font = QtGui.QFont('Coolvetica Rg', 32)
        self.font.setStretch(FONT_STRETCH * 100)

        self.caption_left = "<"
        self.caption_center = "OK"
        self.caption_right = ">"

    def set_captions(self, left, center, right):
        self.caption_left = left
        self.caption_center = center
        self.caption_right = right

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setFont(self.font)
        painter.drawText(
            event.rect(),
            QtCore.Qt.AlignCenter,
            self.caption_left + " | " + self.caption_center + " | " + self.caption_right
        )
        painter.end()
