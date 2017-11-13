"""
线下结果评价
"""
import pandas as pd

from core.path_config import file_offline_reference_set


def drop_duplicate(prediction):
    ui = prediction['user_id'] / prediction['item_id']

    return prediction[ui.duplicated() == False]


def evaluate(prediction):
    reference = pd.read_csv(file_offline_reference_set)

    prediction = drop_duplicate(prediction)

    prediction_ui = prediction['user_id'] / prediction['item_id']
    reference_ui = reference['user_id'] / reference['item_id']

    is_in = prediction_ui.isin(reference_ui)
    true_positive = prediction[is_in]

    tp = len(true_positive)
    predictionSetCount = len(prediction)
    referenceSetCount = len(reference)

    precision = tp / predictionSetCount
    recall = tp / referenceSetCount

    f_score = 2 * precision * recall / (precision + recall)

    tp = recall * referenceSetCount
    predictionSetCount = tp / precision

    print('%.8f%% %.8f %.8f %.0f %.0f' %
          (f_score * 100, precision, recall, tp, predictionSetCount))