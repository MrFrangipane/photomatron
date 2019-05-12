from PySide import QtGui
from .ui import PhotoBooth
from .raspberrypi import RaspberryPi


if __name__ == '__main__':
    app = QtGui.QApplication([])

    with RaspberryPi() as raspberrypi:

        window = PhotoBooth(raspberrypi)
        window.show()

        app.exec_()
