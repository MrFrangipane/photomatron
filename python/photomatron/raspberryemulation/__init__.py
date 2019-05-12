from .camera import Camera
from .buttons import Buttons


class RaspberryPi:
    def __enter__(self):
        self.buttons = Buttons()
        self.camera = Camera()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.buttons.cleanup()
        self.camera.close()
