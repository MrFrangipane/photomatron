

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

    def set_resolution(self, resolution, centered_x=False, centered_y=False):
        if self.is_previewing is None:
            return

        print('CameraEmulation : start_preview(resolution={}, centered_x={}, centered_y={})'.format(
            resolution, centered_x, centered_y
        ))

    def capture(self, filepath):
        print('CameraEmulation : capture({})'.format(filepath))

    def close(self):
        print('CameraEmulation : close()')
