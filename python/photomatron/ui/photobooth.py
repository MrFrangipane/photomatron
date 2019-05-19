from PySide import QtGui
from PySide import QtCore
from .ui import Ui
from .buttonsworker import ButtonsWorker


class PhotoBooth(QtGui.QWidget):
    closed = QtCore.Signal()

    def __init__(self, raspberrypi, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.raspberrypi = raspberrypi
        self.image_index = 1

        self.buttons = ButtonsWorker(self.raspberrypi.buttons)
        self.buttons.centerChanged.connect(self._center_changed)
        self.init_buttons_thread()

        self.raspberrypi.camera.start_preview()

        self.ui = Ui()
        self.ui.cameraGeometryChanged.connect(self.update_camera_window)
        self.layout_ = QtGui.QGridLayout(self)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.addWidget(self.ui)

        self.resize(720, 400) #self.resize(800, 480)

    def init_buttons_thread(self):
        self.buttons_thread = QtCore.QThread()
        self.buttons.moveToThread(self.buttons_thread)
        self.closed.connect(self.buttons.stop)
        self.buttons_thread.started.connect(self.buttons.exec_)
        self.buttons_thread.finished.connect(self.buttons_thread.deleteLater)
        self.buttons_thread.start()

    def _center_changed(self, value):
        if value:
            self.raspberrypi.camera.capture('photo.jpg')

    def update_camera_window(self):
        geometry = self.ui.camera_placeholder_geometry()
        self.raspberrypi.camera.set_geometry(geometry.x(), geometry.y(), geometry.width(), geometry.height())

    def closeEvent(self, event):
        self.closed.emit()
        self.buttons_thread.quit()
        QtGui.QWidget.closeEvent(self, event)
