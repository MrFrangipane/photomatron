import yaml
from PySide import QtGui
from photomatron.ui import PhotoBooth
from photomatron.raspberryemulation import RaspberryPi


if __name__ == '__main__':
    with open('menus.yml', 'r') as f_menus:
        menus_data = yaml.safe_load(f_menus.read())

    app = QtGui.QApplication([])

    with RaspberryPi() as raspberrypi:
        window = PhotoBooth(raspberrypi, menus_data)
        window.show()

        app.exec_()
