"""
使用GBDT进行预测
"""

from sklearn.ensemble import GradientBoostingClassifier


def predict_by_gbdt(train_x, train_y, test_x):
    clf = GradientBoostingClassifier(min_samples_leaf=40, learning_rate=0.05, n_estimators=120)
    clf.fit(train_x, train_y)

    return clf.predict_proba(test_x)
