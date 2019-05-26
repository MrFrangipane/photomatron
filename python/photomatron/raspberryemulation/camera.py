

SCREEN_RESOLUTION = 800, 480
CAPTURE_RESOLUTION = 2048, 2048
IDLE_RESOLUTION = 256, 256
LIVE_RESOLUTION = 480, 480
FRAMERATE = 40


class Camera:

    def __init__(self):
        self.is_previewing = False

    def start_preview(self):
        self.is_previewing = True
        print('CameraEmulation : start_preview()')

    def set_geometry(self, x, y, width, height):
        if self.is_previewing is None:
            return

        print('CameraEmulation : set_geometry(x={}, y={}, width={}, height={})'.format(
            x, y, width, height
        ))

    def capture(self, filepath):
        print('CameraEmulation : capture({})'.format(filepath))

    def set_filter(self, filter):
        print('CameraEmulation : set_filter({})'.format(filter))

    def close(self):
        print('CameraEmulation : close()')
