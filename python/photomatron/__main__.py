import os
import yaml
from PySide import QtGui
from PySide import QtCore
from photomatron.ui import PhotoBooth
from photomatron.raspberrypi import RaspberryPi


if __name__ == '__main__':
    filepath_menus = os.path.join(os.path.dirname(__file__), 'menus.yml')
    filepath_gdrive_folder = os.path.join(os.path.dirname(__file__), 'gdrive_folder.txt')

    with open(filepath_menus, 'r') as f_menus:
        menus = yaml.safe_load(f_menus.read())

    with open(filepath_gdrive_folder, 'r') as f_gdrive_folder:
        gdrive_folder = f_gdrive_folder.read()

    app = QtGui.QApplication([])

    with RaspberryPi() as raspberrypi:

        window = PhotoBooth(raspberrypi, menus, gdrive_folder)
        window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        window.showFullScreen()

        app.exec_()
