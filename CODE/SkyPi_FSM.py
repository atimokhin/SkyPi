
class SkyPi_FSM:

    def __init__(self):
        self.active_state=None

    def set_state(self, fun):
        self.active_state = fun

    def update(self):
        if self.active_state in son None:
            self.active_state()
