import os
import yaml
from PySide import QtGui
from photomatron.ui import PhotoBooth
from photomatron.raspberryemulation import RaspberryPi


if __name__ == '__main__':
    filepath_menus = os.path.join(os.path.dirname(__file__), 'menus.yml')

    with open(filepath_menus, 'r') as f_menus:
        menus_data = yaml.safe_load(f_menus.read())

    app = QtGui.QApplication([])

    with RaspberryPi() as raspberrypi:

        window = PhotoBooth(raspberrypi, menus_data, '')
        window.show()

        app.exec_()
