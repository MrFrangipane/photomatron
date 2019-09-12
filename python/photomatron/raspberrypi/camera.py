import time
import picamera


CAPTURE_RESOLUTION = 2048, 2048
FRAMERATE = 40
CAPTURE_SLEEP = .2
OVER_SATURATION = 25
OVER_BRIGHTNESS = 5


class Camera:

    def __init__(self):
        self.init_cam()

    def init_cam(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = CAPTURE_RESOLUTION
        self.camera.framerate = FRAMERATE
        self.camera.hflip = True

    def start_preview(self):
        if self.camera.preview is None:
            self.camera.start_preview(fullscreen=False)

    def set_geometry(self, x, y, width, height):
        self._geometry = x, y, width, height
        self.camera.preview.window = x, y, width, height

    def capture(self, filepath):
        time.sleep(CAPTURE_SLEEP)
        self.camera.saturation = min(100, self.camera.saturation + OVER_SATURATION)
        self.camera.brightness = min(100, self.camera.brightness + OVER_BRIGHTNESS)

        self.camera.capture(filepath)
        self.camera.close()

        self.init_cam()
        self.start_preview()
        self.camera.preview.window = self._geometry

    def set_filter(self, filter):
        if not filter or filter.lower() == 'normal':
            self.camera.image_effect = 'none'

        else:
            self.camera.image_effect = filter

    def close(self):
        self.camera.close()
