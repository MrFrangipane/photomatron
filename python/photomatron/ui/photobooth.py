from PySide import QtGui
from PySide import QtCore
from .ui import Ui
from .buttonsworker import ButtonsWorker


class PhotoBooth(QtGui.QWidget):
    closed = QtCore.Signal()

    def __init__(self, raspberrypi, menus, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setStyleSheet("color: white; background-color: black; qproperty-alignment: AlignCenter;")

        self.raspberrypi = raspberrypi
        self.menus = menus

        self._button_left_action = None
        self._button_center_action = None
        self._button_right_action = None

        self.buttons = ButtonsWorker(self.raspberrypi.buttons)
        self.buttons.leftChanged.connect(self._left_changed)
        self.buttons.centerChanged.connect(self._center_changed)
        self.buttons.rightChanged.connect(self._right_changed)
        self._init_buttons_thread()

        self.raspberrypi.camera.start_preview()

        self.ui = Ui()
        self.ui.cameraGeometryChanged.connect(self.update_camera_window)
        self.layout_ = QtGui.QGridLayout(self)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.addWidget(self.ui)

        self.resize(800, 480)
        self._init_menus()

    def _init_menus(self):
        try:
            menus = self.menus['menus']
            menu_start = menus.get(self.menus.get('start_with'))
        except ValueError as e:
            print("Check menu.yml for mistakes")
            return

        self._load_menu(menu_start)

    def _do_action(self, action):
        print("DO", action)

    def _load_menu(self, menu):
        caption = menu['caption']
        self.ui.set_caption_message(caption['main'])
        self.ui.set_caption_buttons(
            left=caption['button_left'],
            center=caption['button_center'],
            right=caption['button_right']
        )

        action = menu['action']
        if 'enter' in action.keys():
            self._do_action(action['enter'])

        self._button_left_action = action.get('button_left')
        self._button_center_action = action.get('button_center')
        self._button_right_action = action.get('button_right')

    def _init_buttons_thread(self):
        self.buttons_thread = QtCore.QThread()
        self.buttons.moveToThread(self.buttons_thread)
        self.closed.connect(self.buttons.stop)
        self.buttons_thread.started.connect(self.buttons.exec_)
        self.buttons_thread.finished.connect(self.buttons_thread.deleteLater)
        self.buttons_thread.start()

    def _left_changed(self, value):
        if value and self._button_left_action:
            self._do_action(self._button_left_action)

    def _center_changed(self, value):
        if value and self._button_center_action:
            self._do_action(self._button_center_action)

    def _right_changed(self, value):
        if value and self._button_right_action:
            self._do_action(self._button_right_action)

    def update_camera_window(self):
        geometry = self.ui.camera_placeholder_geometry()
        self.raspberrypi.camera.set_geometry(geometry.x(), geometry.y(), geometry.width(), geometry.height())

    def closeEvent(self, event):
        self.closed.emit()
        self.buttons_thread.quit()
        QtGui.QWidget.closeEvent(self, event)
