from PySide import QtCore


class ButtonsWorker(QtCore.QObject):
    leftChanged = QtCore.Signal(bool)
    centerChanged = QtCore.Signal(bool)
    rightChanged = QtCore.Signal(bool)

    def __init__(self, buttons, parent=None):
        QtCore.QObject.__init__(self, parent)
        self.buttons = buttons
        self.buttons.parent = self

    def left_changed(self, value):
        self.buttons.set_led(value)
        self.leftChanged.emit(value)

    def center_changed(self, value):
        self.buttons.set_led(value)
        self.centerChanged.emit(value)

    def right_changed(self, value):
        self.buttons.set_led(value)
        self.rightChanged.emit(value)

    def exec_(self):
        self.buttons.exec_()

    def stop(self):
        self.buttons.stop()
