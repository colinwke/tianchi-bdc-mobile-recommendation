"""
使用logistic回归进行预测
"""

from sklearn.linear_model import LogisticRegression


def predict_by_lr(train_x, train_y, test_x):
    clf = LogisticRegression().fit(train_x, train_y)

    return clf.predict_proba(test_x)
