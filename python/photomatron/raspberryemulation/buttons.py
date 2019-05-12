import time


class ButtonsState:
    def __init__(self):
        self.left = False
        self.center = False
        self.right = False
        self.led = True

    def __eq__(self, other):
        return self.left == other.left and self.center == other.center and self.right == other.right

    def __repr__(self):
        return "<{}(left={}, center={}, right={}, led={})>".format(
            self.__class__.__name__,
            self.left,
            self.center,
            self.right,
            self.led
        )


class Buttons:
    INTERVAL = 0.02

    def __init__(self):
        self.parent = None

        self.previous_state = ButtonsState()

        self.is_running = False

    def state(self):
        state = ButtonsState()
        '''
        state.left = GPIO.input(self.GPIO_BUTTON_LEFT) == GPIO.LOW
        state.center = GPIO.input(self.GPIO_BUTTON_CENTER) == GPIO.LOW
        state.right = GPIO.input(self.GPIO_BUTTON_RIGHT) == GPIO.LOW
        state.led = GPIO.input(self.GPIO_LED) == GPIO.HIGH
        '''
        return state

    def exec_(self):
        self.is_running = True

        assert hasattr(self.parent, 'left_changed')
        assert hasattr(self.parent, 'center_changed')
        assert hasattr(self.parent, 'right_changed')

        while self.is_running:
            time.sleep(self.INTERVAL)
            try:
                state = self.state()
            except RuntimeError as e:
                break

            if self.previous_state.left != state.left:
                self.previous_state.left = state.left
                self.parent.left_changed(state.left)

            if self.previous_state.center != state.center:
                self.previous_state.center = state.center
                self.parent.center_changed(state.center)

            if self.previous_state.right != state.right:
                self.previous_state.right = state.right
                self.parent.right_changed(state.right)

    def stop(self):
        self.is_running = False

    def set_led(self, status):
        print('GPIOEmulation : set_led(status={})'.format(status))

    def cleanup(self):
        print('GPIOEmulation : cleanup()')
