import time
from PySide import QtGui
from PySide import QtCore


class ButtonsState:
    def __init__(self):
        self.left = False
        self.center = False
        self.right = False
        self.led = True

    def __eq__(self, other):
        return self.left == other.left and self.center == other.center and self.right == other.right

    def __repr__(self):
        return "<{}(left={}, center={}, right={}, led={})>".format(
            self.__class__.__name__,
            self.left,
            self.center,
            self.right,
            self.led
        )


class ButtonEmulatorWidget(QtGui.QWidget):
    changed = QtCore.Signal(ButtonsState)

    def __init__(self, parent_, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle("GPIO Emulator")
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowStaysOnTopHint)

        self.parent_ = parent_

        self.button_left = QtGui.QPushButton('LEFT')
        self.button_left.pressed.connect(self._update)
        self.button_left.released.connect(self._update)

        self.button_middle = QtGui.QPushButton('BIG MIDDLE')
        self.button_middle.pressed.connect(self._update)
        self.button_middle.released.connect(self._update)

        self.button_right = QtGui.QPushButton('RIGHT')
        self.button_right.pressed.connect(self._update)
        self.button_right.released.connect(self._update)

        self.checkbox = QtGui.QCheckBox('LED')
        self.checkbox.setEnabled(False)

        self.layout_ = QtGui.QGridLayout(self)
        self.layout_.addWidget(self.button_left, 0, 0)
        self.layout_.addWidget(self.button_middle, 0, 1)
        self.layout_.addWidget(self.button_right, 0, 2)
        self.layout_.addWidget(self.checkbox, 1, 0, 3, 1)

    def closeEvent(self, event):
        if self.parent_.is_running:
            event.ignore()

    def set_checkbox(self, checked):
        self.checkbox.setChecked(checked)

    def _update(self):
        state = ButtonsState()
        state.left = self.button_left.isDown()
        state.center = self.button_middle.isDown()
        state.right = self.button_right.isDown()
        state.led = self.checkbox.isChecked()

        self.changed.emit(state)


class Buttons:
    INTERVAL = 0.02

    def __init__(self):
        self.parent = None
        self.previous_state = ButtonsState()
        self._state = self.previous_state
        self.is_running = False

        self.widget = ButtonEmulatorWidget(self)
        self.widget.moveToThread(QtGui.QApplication.instance().thread())
        self.widget.changed.connect(self._changed)
        self.widget.show()

    def _changed(self, state):
        self._state = state

    def state(self):
        return self._state

    def exec_(self):
        self.is_running = True

        assert hasattr(self.parent, 'left_changed')
        assert hasattr(self.parent, 'center_changed')
        assert hasattr(self.parent, 'right_changed')

        while self.is_running:
            time.sleep(self.INTERVAL)
            try:
                state = self.state()
            except RuntimeError as e:
                break

            if self.previous_state.left != state.left:
                self.previous_state.left = state.left
                self.parent.left_changed(state.left)

            if self.previous_state.center != state.center:
                self.previous_state.center = state.center
                self.parent.center_changed(state.center)

            if self.previous_state.right != state.right:
                self.previous_state.right = state.right
                self.parent.right_changed(state.right)

        self.widget.close()

    def stop(self):
        self.is_running = False

    def set_led(self, status):
        self.widget.set_checkbox(status)

    def cleanup(self):
        pass
