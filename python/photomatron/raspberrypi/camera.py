import picamera

SCREEN_RESOLUTION = 800, 480
CAPTURE_RESOLUTION = 2048, 2048
IDLE_RESOLUTION = 256, 256
LIVE_RESOLUTION = 480, 480
FRAMERATE = 40


class Camera:

    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = CAPTURE_RESOLUTION
        self.camera.framerate = FRAMERATE

    def start_preview(self):
        if self.camera.preview is None:
            self.camera.start_preview(fullscreen=False)
            self.set_resolution(IDLE_RESOLUTION, centered_y=True)

    def set_resolution(self, resolution, centered_x=False, centered_y=False):
        if self.camera.preview is None:
            return

        x = (SCREEN_RESOLUTION[0] - resolution[0]) // 2 if centered_x else 0
        y = (SCREEN_RESOLUTION[1] - resolution[1]) // 2 if centered_y else 0
        self.camera.preview.window = x, y, *resolution

    def capture(self, filepath):
        self.camera.capture(filepath)

    def close(self):
        self.camera.close()
