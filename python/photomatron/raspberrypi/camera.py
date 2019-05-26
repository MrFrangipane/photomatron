import picamera

CAPTURE_RESOLUTION = 2048, 2048
FRAMERATE = 40


class Camera:

    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = CAPTURE_RESOLUTION
        self.camera.framerate = FRAMERATE
        self.camera.hflip = True

    def start_preview(self):
        if self.camera.preview is None:
            self.camera.start_preview(fullscreen=False)

    def set_geometry(self, x, y, width, height):
        self.camera.preview.window = x, y, width, height

    def capture(self, filepath):
        self.camera.capture(filepath)

    def set_filter(self, filter):
        if not filter:
            self.camera.image_effect = 'none'

        else:
            self.camera.image_effect = filter

    def close(self):
        self.camera.close()
