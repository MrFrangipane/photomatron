from PySide import QtGui
from PySide import QtCore


class CameraOverlayPlaceholder(QtGui.QLabel):
    def __init__(self, parent=None):
        QtGui.QLabel.__init__(self, parent)
        self.setText("CameraOverlayPlaceholder")
        self.setStyleSheet("background-color: yellow; qproperty-alignment: AlignCenter;")


class Ui(QtGui.QWidget):
    cameraGeometryChanged = QtCore.Signal()

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setStyleSheet("background-color: red")

        self.camera_placeholder = CameraOverlayPlaceholder()
        #self.camera_placeholder.setFixedSize(480, 480)

        self.layout_ = QtGui.QGridLayout(self)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.addWidget(self.camera_placeholder, 0, 0, 3, 1)
        self.layout_.addWidget(QtGui.QLabel("Title"), 0, 1)
        self.layout_.addWidget(QtGui.QLabel("Message"), 1, 1)
        self.layout_.addWidget(QtGui.QLabel("Buttons"), 2, 1)

        self._previous_camera_geometry = self.camera_placeholder_geometry()

    def notify_camera_geometry_changed(self):
        self.cameraGeometryChanged.emit()

    def camera_placeholder_geometry(self):
        geo = self.camera_placeholder.geometry()
        return QtCore.QRect(self.mapToGlobal(geo.topLeft()), geo.size())

    def resizeEvent(self, event):
        if self._previous_camera_geometry != self.camera_placeholder_geometry():
            self.notify_camera_geometry_changed()
            self._previous_camera_geometry = self.camera_placeholder_geometry()
