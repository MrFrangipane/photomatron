from PySide import QtGui
from PySide import QtCore
from .buttonsworker import ButtonsWorker


class PhotoBooth(QtGui.QWidget):
    def __init__(self, raspberrypi, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.raspberrypi = raspberrypi
        self.image_index = 1

        self.buttons = ButtonsWorker(self.raspberrypi.buttons)
        self.buttons.centerChanged.connect(self._center_changed)
        self.init_buttons_thread()

        self.raspberrypi.camera.start_preview()

    def init_buttons_thread(self):
        self.buttons_thread = QtCore.QThread()
        self.buttons.moveToThread(self.buttons_thread)
        self.buttons_thread.started.connect(self.buttons.exec_)
        self.buttons_thread.finished.connect(self.buttons_thread.deleteLater)
        self.buttons_thread.start()

    def _center_changed(self, value):
        if value:
            self.raspberrypi.camera.capture('photo.jpg')

    def closeEvent(self, event):
        self.buttons.stop()  # TODO : use signals for thread safety
        self.buttons_thread.quit()
        QtGui.QWidget.closeEvent(self, event)
