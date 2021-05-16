from stoppable_thread import StoppableThread
import time

class HandThread(StoppableThread):
    def __init__(self, application=None):
        super().__init__()
        self.application = application

    def run(self):
        while not self.stopped():
            time.sleep(2)