import mediapipe as mp


class HandLandmark:
    def __init__(self, min_detection_confidence=0.6, min_tracking_confidence=0.6, max_num_hands=1):
        self.predictor = mp.solutions.hands.Hands(min_detection_confidence=min_detection_confidence,
                                                  min_tracking_confidence=min_tracking_confidence,
                                                  max_num_hands=max_num_hands)
        self.drawer = mp.solutions.drawing_utils

    def get_landmarks(self, imageRGB):
        return self.predictor.process(imageRGB).multi_hand_landmarks

    def draw_landmarks(self, imageBGR, landmarks):
        if landmarks:
            for landmark in landmarks:
                self.drawer.draw_landmarks(
                    imageBGR, landmark, mp.solutions.hands.HAND_CONNECTIONS)
