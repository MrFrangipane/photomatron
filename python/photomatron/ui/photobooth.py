import os
from glob import glob
from datetime import datetime
from PySide import QtGui
from PySide import QtCore
from .ui import Ui
from .buttonsworker import ButtonsWorker

PADDING_X = 40
PADDING_Y = 75
SIZE = 540
TIMER_INTERVAL = 100
STYLESHEET = """
* {
    color: white; 
    background-color: black; 
    qproperty-alignment: AlignCenter;
}

QProgressBar {
    border: 0px solid white;
}

QProgressBar::chunk {
    background-color: white;
    width: 1px;
}
"""


def assemble():
    root = (os.path.dirname(os.path.dirname(__file__)))
    assembly = QtGui.QPixmap(os.path.join(root, 'resources', 'assembly.png'))

    photos = glob(os.path.join(root, '*.jpg'))[-4:]
    photo_0 = QtGui.QPixmap(photos[0]).scaled(SIZE, SIZE, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
    photo_1 = QtGui.QPixmap(photos[1]).scaled(SIZE, SIZE, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
    photo_2 = QtGui.QPixmap(photos[2]).scaled(SIZE, SIZE, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
    photo_3 = QtGui.QPixmap(photos[3]).scaled(SIZE, SIZE, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

    painter = QtGui.QPainter()
    painter.begin(assembly)
    painter.drawPixmap(PADDING_X, PADDING_Y, photo_0)
    painter.drawPixmap(PADDING_X + PADDING_X + SIZE, PADDING_Y, photo_1)
    painter.drawPixmap(PADDING_X, PADDING_Y + PADDING_Y + SIZE, photo_2)
    painter.drawPixmap(PADDING_X + PADDING_X + SIZE, PADDING_Y + PADDING_Y + SIZE, photo_3)
    painter.end()

    assembly_filepath = 'assembly_{}.jpg'.format(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    assembly.save(os.path.join(root, assembly_filepath))


class PhotoBooth(QtGui.QWidget):
    closed = QtCore.Signal()

    def __init__(self, raspberrypi, menus, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setStyleSheet(STYLESHEET)

        self.raspberrypi = raspberrypi
        self.menus = menus

        self._message = ""
        self._button_left_ = ""
        self._button_center_ = ""
        self._button_right_ = ""
        self._show_progress = True

        self._button_left_action = None
        self._button_center_action = None
        self._button_right_action = None
        self._elapsed_action = None

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

        self.time_gauge = 0.0  # in seconds
        self.elapsed = 0.0  # in seconds
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._update_ui)
        self.timer.start(TIMER_INTERVAL)

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
        name, arguments = list(action.items())[0]

        if name == 'camera':
            if arguments == {'reset': True}:
                self.raspberrypi.camera.set_filter(None)

            elif 'filter' in arguments.keys():
                self.raspberrypi.camera.set_filter(arguments['filter'])

            elif 'capture' in arguments.keys():
                self.raspberrypi.camera.capture(arguments['capture'].format(
                    timestamp=datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                ))

        elif name == 'goto':
            self._load_menu(self.menus['menus'][arguments])

        elif name == 'assemble':
            assemble()

    def _update_ui(self):
        self.ui.set_message(self._message.format(
            elapsed=int(self.elapsed),
            time_left=min(self.time_gauge, max(1, int(self.time_gauge - self.elapsed + 1)))
        ))
        self.ui.set_caption_buttons(
            left=self._button_left,
            center=self._button_center,
            right=self._button_right
        )

        if self.elapsed <= self.time_gauge and self.time_gauge:
            self.elapsed += TIMER_INTERVAL * 0.001
            if self._show_progress:
                self.ui.set_progress(100 - int(self.elapsed / self.time_gauge * 100))

        else:
            if self.time_gauge:
                self.time_gauge = 0
                self.elapsed = 0
                self.ui.set_progress(0)
                self._do_action(self._elapsed_action)

    def _register_timer(self, time, **action):
        self.time_gauge = time
        self._show_progress = action.get('show_progress', True)
        self._elapsed_action = action

    def _load_menu(self, menu):
        caption = menu['caption']
        self._message = caption['main']
        self._button_left = caption['button_left']
        self._button_center = caption['button_center']
        self._button_right = caption['button_right']

        action = menu['action']
        if 'enter' in action.keys():
            self._do_action(action['enter'])

        if 'elapsed' in action.keys():
            self._register_timer(**action['elapsed'])

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
