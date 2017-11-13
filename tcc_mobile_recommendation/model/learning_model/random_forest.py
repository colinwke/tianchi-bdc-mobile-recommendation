"""
使用随机森林进行预测
"""

from sklearn.ensemble import RandomForestClassifier


def prediction_by_rf(train_x, train_y, test_x):
    clf = RandomForestClassifier(n_estimators=300, max_features=15, max_depth=5)
    clf = clf.fit(train_x, train_y)
    predicted = clf.predict_proba(test_x)

    return predicted
