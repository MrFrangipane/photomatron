from PySide import QtGui
from PySide import QtCore


FONT_STRETCH = 0.72


class Fonts:
    def __init__(self):
        self.title = QtGui.QFont('Coolvetica Rg', 32)
        self.title.setStretch(FONT_STRETCH * 100)

        self.message = QtGui.QFont('Open Sans', 16)
        self.message.setStretch(FONT_STRETCH * 100)

        self.buttons = QtGui.QFont('Coolvetica Rg', 20)
        self.buttons.setStretch(FONT_STRETCH * 100)


class CameraOverlayPlaceholder(QtGui.QLabel):
    def __init__(self, parent=None):
        QtGui.QLabel.__init__(self, parent)
        self.setText("Camera Overlay Placeholder")


class Ui(QtGui.QWidget):
    cameraGeometryChanged = QtCore.Signal()

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.fonts = Fonts()

        self.camera_placeholder = CameraOverlayPlaceholder()
        self.camera_placeholder.setFixedSize(475, 475)

        self.label_tile = QtGui.QLabel("Photomatron")
        self.label_tile.setFixedHeight(80)
        self.label_tile.setFont(self.fonts.title)

        self.label_message = QtGui.QLabel("This is a message from the Queen of Great Britain : Keep calm and take a picture")
        self.label_message.setWordWrap(True)
        self.label_message.setFont(self.fonts.message)

        self.buttons_guide = QtGui.QLabel("Prev | OK | Next")
        self.buttons_guide.setFont(self.fonts.buttons)
        self.buttons_guide.setFixedHeight(80)

        self.layout_ = QtGui.QGridLayout(self)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.addWidget(self.camera_placeholder, 0, 0, 3, 1)
        self.layout_.addWidget(self.label_tile, 0, 1)
        self.layout_.addWidget(self.label_message, 1, 1)
        self.layout_.addWidget(self.buttons_guide, 2, 1)

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
