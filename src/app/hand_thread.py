import cv2

from stoppable_thread import StoppableThread
from hand_landmark import HandLandmark
from char_predictor import CharPredictor
import time


class HandThread(StoppableThread):
    def __init__(self, application=None, acceptable_dist=0.20, consecutive_seq=20, consecutive_letter=5):
        super().__init__()
        self.application = application
        self.hand_landmarker = HandLandmark()
        self.char_predictor = CharPredictor(application.xgb_model)
        self.acceptable_dist = acceptable_dist
        self.consecutive_seq = consecutive_seq
        self.consecutive_letter = consecutive_letter
        self.reset_default_values()

    def reset_default_values(self):
        self.prev_landmarks = None
        self.consecutive_stable = 0
        self.cur_letter = None
        self.consecutive_stable_letter = 0

    def run(self):
        self.reset_default_values()
        self.consecutive_stable_letter = 0
        while not self.stopped():
            if self.application.is_record:
                frame = self.application.frame
                frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frameRGB.flags.writeable = False
                landmarks = self.hand_landmarker.get_landmarks(frameRGB)
                frameRGB.flags.writeable = True
                self.application.landmarks = landmarks
                if landmarks:
                    if self.prev_landmarks:
                        dist = 0
                        for lm, plm in zip(landmarks[0].landmark, self.prev_landmarks[0].landmark):
                            dist = (lm.x - plm.x)**2 + (
                                lm.y - plm.y)**2 + (lm.z - plm.z)**2
                        dist = dist**0.5

                        if dist < self.acceptable_dist:
                            self.consecutive_stable += 1
                        else:
                            self.consecutive_stable = 0

                        if self.consecutive_stable == self.consecutive_seq:
                            self.consecutive_stable = 0
                            char, _ = self.char_predictor.best_predict(
                                landmarks[0])
                            if self.cur_letter != char:
                                self.cur_letter = char
                                self.consecutive_stable_letter = 0
                            self.consecutive_stable_letter += 1

                            if self.consecutive_stable_letter == self.consecutive_letter:
                                self.application.letter_queue.append(char)

                        self.prev_landmarks = landmarks
                    else:
                        self.prev_landmarks = landmarks
                else:
                    self.consecutive_stable = 0
