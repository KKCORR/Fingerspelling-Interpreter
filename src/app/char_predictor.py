import numpy as np
import xgboost as xgb


class CharPredictor:

    def __init__(self, xgb_model):
        self.xgb_model = xgb_model
        self.char_classes = ["1", "2", "3", "4", "5", "ก", "ง2", "จ1", "จ2", "ฉ1", "ซ2", "ด", "ต", "ท1", "น", "บ", "พ",
                             "ฟ", "ม", "ย", "ร", "ล", "ว", "ส", "ห", "อ"]

    def get_features(self, hand_landmark):
        x = []
        y = []
        for i in range(21):
            x.append(hand_landmark.landmark[i].x)
            y.append(hand_landmark.landmark[i].y)
        norm_x = (np.array(x) - np.min(x)) / (np.max(x) - np.min(x))
        norm_y = (np.array(y) - np.min(y)) / (np.max(y) - np.min(y))

        # use only norm_x and norm_y and merge element wise
        # e.g. norm_x = [1, 3, 5] and norm_y = [2, 4, 6] => row = [1, 2, 3, 4, 5, 6]
        row = np.insert(norm_y, np.arange(len(norm_x)), norm_x)
        features = xgb.DMatrix(np.asmatrix(row))
        return features

    def predict(self, hand_landmark):
        features = self.get_features(hand_landmark)
        preds = self.xgb_model.predict(features)
        first_pred = preds[0]
        # list of (character, percentage of the confidence)
        return list(zip(self.char_classes, first_pred))

    def best_predict(self, hand_landmark):
        features = self.get_features(hand_landmark)
        preds = self.xgb_model.predict(features)
        first_pred = preds[0]
        best_arg = np.argmax(first_pred)
        # (character, percentage of the confidence)
        return (self.char_classes[best_arg], first_pred[best_arg])
