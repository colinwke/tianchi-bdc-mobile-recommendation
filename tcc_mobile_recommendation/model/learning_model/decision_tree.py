"""
使用J48预测分类
"""

from sklearn.tree import DecisionTreeClassifier


def predict_by_dt(train_x, train_y, test_x):
    clf = DecisionTreeClassifier(max_depth=4)
    clf = clf.fit(train_x, train_y)

    return clf.predict_proba(test_x)
