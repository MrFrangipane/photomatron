from .camera import Camera
from .buttons import Buttons
from .printer import Printer


class RaspberryPi:
    def __enter__(self):
        self.buttons = Buttons()
        self.camera = Camera()
        self.printer = Printer()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.buttons.cleanup()
        self.camera.close()
