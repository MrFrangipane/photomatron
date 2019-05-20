from PySide import QtGui
from PySide import QtCore


class ButtonsWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.drawText(
            event.rect(),
            QtCore.Qt.AlignCenter,
            "Bonjour"
        )
        painter.end()
