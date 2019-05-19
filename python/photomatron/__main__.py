from PySide import QtGui
from PySide import QtCore
from photomatron.ui import PhotoBooth
from photomatron.raspberrypi import RaspberryPi


if __name__ == '__main__':
    app = QtGui.QApplication([])

    with RaspberryPi() as raspberrypi:

        window = PhotoBooth(raspberrypi)
        window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        window.showFullScreen()

        app.exec_()
