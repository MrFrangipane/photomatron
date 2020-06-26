import os
from glob import glob
from datetime import datetime
from PySide import QtGui
from PySide import QtCore
from .ui import Ui
from .buttonsworker import ButtonsWorker
from .. import gdrive
from .. import photoboothfrangitron


NEXT = '#N#E#X#T#'
PADDING_X = 40
PADDING_Y = 40
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
    padding-left: 50px;
    padding-right: 50px;
}

QProgressBar::chunk {
    background-color: white;
    width: 1px;
}
"""


def assemble():
    root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    assembly = QtGui.QPixmap(os.path.join(root, 'photomatron', 'resources', 'assembly.png'))
    photos = sorted(glob(os.path.join(root, '*.jpg')))[-4:]

    if not photos:
        print('No photos found in ' + root)
        return

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

    assembly_filename = 'assembly_{}.jpg'.format(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    assembly_filepath = os.path.join(root, assembly_filename)

    # Rotation messes up the margins
    # rotation = QtGui.QTransform()
    # rotation.rotate(180)
    # assembly = assembly.transformed(rotation)

    assembly.save(assembly_filepath, 'jpg', 100)
    return assembly_filepath


class PhotoBooth(QtGui.QWidget):
    closed = QtCore.Signal()

    def __init__(self, raspberrypi, menus, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setStyleSheet(STYLESHEET)
        self.setCursor(QtCore.Qt.BlankCursor)

        self.raspberrypi = raspberrypi
        self.menus = menus
        self.menu_index = 0
        self.last_filepath = None

        self._message = ""
        self._button_left_ = ""
        self._button_center_ = ""
        self._button_right_ = ""

        self._button_left_action = None
        self._button_center_action = None
        self._button_right_action = None
        self._elapsed_menu = None

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

        self.elapsed = 0.0  # in seconds
        self.time_gauge = 0.0  # in seconds
        self.show_progress = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._update_ui)
        self.timer.start(TIMER_INTERVAL)

        self.resize(800, 480)
        self._init_menus()

    def _init_menus(self):
        self.menu_index = 0
        self._load_menu()

    def _do_action(self, action):
        self.update()
        QtGui.QApplication.processEvents()

        if action == NEXT:
            self._load_menu()

        elif action['type'] == 'idle':
            self._button_left_action = NEXT
            self._button_center_action = NEXT
            self._button_right_action = NEXT

        elif action['type'] == 'countdown':
            self._register_timer(
                time=action['duration'],
                show_progress=True
            )

        elif action['type'] == 'photo':
            self.raspberrypi.camera.capture(
                action['filename'].format(
                    timestamp=datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                )
            )
            self._load_menu()

        elif action['type'] == 'assemble':
            self.last_filepath = assemble()
            self._load_menu()

        elif action['type'] == 'post':
            if self.last_filepath is not None:
                photoboothfrangitron.post_image(self.last_filepath)
                #
                # gdrive.post_picture(
                #     self.last_filepath,
                #     action['gdrive_folder_id']
                # )
            self._load_menu()

        elif action['type'] == 'print':
            if self.last_filepath is not None:
                self.raspberrypi.printer.print_picture(
                    filepath=self.last_filepath,
                    printer_name=action['printer_name']
                )
            self._load_menu()

        elif action['type'] == 'message':
            self._register_timer(
                time=action['duration'],
                show_progress=False
            )

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
            if self.show_progress:
                self.ui.set_progress(100 - int(self.elapsed / self.time_gauge * 100))

        else:
            if self.time_gauge:
                self.time_gauge = 0
                self.elapsed = 0
                self.ui.set_progress(0)
                self._load_menu()

    def _register_timer(self, time, show_progress):
        self.time_gauge = time
        self.show_progress = show_progress

    def _load_menu(self):
        if self.menu_index >= len(self.menus):
            self.menu_index = 0

        menu = self.menus[self.menu_index]

        self._button_left_action = None
        self._button_center_action = None
        self._button_right_action = None

        self._message = menu['message']
        self._button_left = menu['button_left']
        self._button_center = menu['button_center']
        self._button_right = menu['button_right']

        self.menu_index += 1

        self._update_ui()
        self._do_action(menu)

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
