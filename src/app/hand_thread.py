import cv2

from stoppable_thread import StoppableThread
from hand_landmark import HandLandmark
from char_predictor import CharPredictor
import time


class HandThread(StoppableThread):
    def __init__(self, application=None):
        super().__init__()
        self.application = application
        self.hand_landmarker = HandLandmark()
        self.char_predictor = CharPredictor(application.xgb_model)

    def run(self):
        while not self.stopped():
            if self.application.is_record:
                frame = self.application.frame
                frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frameRGB.flags.writeable = False
                landmarks = self.hand_landmarker.get_landmarks(frameRGB)
                frameRGB.flags.writeable = True
                self.application.landmarks = landmarks
                if landmarks:
                    print(self.char_predictor.best_predict(landmarks[0]))
