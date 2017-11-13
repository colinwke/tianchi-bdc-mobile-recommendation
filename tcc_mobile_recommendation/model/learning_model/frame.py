"""
使用模型进行预测
"""

import pandas as pd

from core.evaluator import evaluate
from debug import TimeStamp

from model.learning_model.decision_tree import predict_by_dt
from model.learning_model.logistic_regression import predict_by_lr
from model.learning_model.random_forest import prediction_by_rf
from model.learning_model.gbdt import predict_by_gbdt

from model.config import folder_core

file_train = "train_offline.csv"
file_test = "test_offline.csv"

path_commit = "D:\\DataAnalysis\\tcc_mobile_recommendation\\data\\commit\\tianchi_mobile_recommendation_predict.csv"

if __name__ == "__main__":
    ts = TimeStamp()

    # ==  数据读取  ====================================================
    train_data = pd.read_csv(folder_core + "model\\" + file_train)
    test_data = pd.read_csv(folder_core + "model\\" + file_test)
    ts.cat("load data success!")

    # ==  对负样本进行采样===============================================
    # train_data_ng = train_data['label'] == 0
    # print(train_data_ng.value_counts())
    # # 只保留负样本
    # train_data_ng = train_data_ng[train_data_ng]
    # # 采样
    # train_data_ng = train_data_ng.sample(frac=0.9)
    # # 删除
    # train_data = train_data.drop(train_data_ng.index, axis=0)
    # train_data_ng = train_data['label'] == 0
    # print(train_data_ng.value_counts())
    #
    # print(len(train_data_ng))


    # ==  只选加入购物车的记录作为测试集 ==================================
    # print("train data length: ", len(train_data))
    # train_data = train_data[train_data['lbt'] == 3]
    # print("train data length by cart", len(train_data))
    # print("test data length:", len(test_data))
    # test_data = test_data[test_data['lbt'] == 3]
    # evaluate(test_data[['user_id', 'item_id']])
    #
    # print("test data length by cart", len(test_data))
    # exit(2)


    # ==  数据转换  ======================================================
    train_y = train_data['label'].values
    train_x = train_data.drop(['user_id', 'item_id', 'label'], axis=1).values
    test_x = test_data.drop(['user_id', 'item_id'], axis=1).values

    # ==  简单预测  ======================================================
    # predicted_proba = predict_by_dt(train_x, train_y, test_x)
    # predicted_proba = prediction_by_rf(train_x, train_y, test_x)
    # predicted_proba = predict_by_lr(train_x, train_y, test_x)
    predicted_proba = predict_by_gbdt(train_x, train_y, test_x, 1)

    predicted_proba = pd.DataFrame(predicted_proba)
    predicted = pd.concat([test_data[['user_id', 'item_id']], predicted_proba], axis=1)
    predicted = predicted.sort_values(1, ascending=False)
    predicted = predicted.iloc[:750, [0, 1]]
    # 保存到文件
    predicted.to_csv(path_commit, index=False)
    evaluate(predicted)

    # # ==  试参预测  ======================================================
    # for i in range(1, 10):
    #     # predicted_proba = predict_by_dt(train_x, train_y, test_x, i)
    #     # predicted_proba = prediction_by_rf(train_x, train_y, test_x, i)
    #     # predicted_proba = predict_by_lr(train_x, train_y, test_x)
    #     predicted_proba = predict_by_gbdt(train_x, train_y, test_x, i * 0.005)
    #
    #     predicted_proba = pd.DataFrame(predicted_proba)
    #     predicted = pd.concat([test_data[['user_id', 'item_id']], predicted_proba], axis=1)
    #     predicted = predicted.sort_values(1, ascending=False)
    #     predicted = predicted.iloc[:750, [0, 1]]
    #     evaluate(predicted)


    # # ==  求得提交最佳集合数  =============================================
    # # predicted_proba = predict_by_dt(train_x, train_y, test_x)
    # # predicted_proba = prediction_by_rf(train_x, train_y, test_x)
    # # predicted_proba = predict_by_lr(train_x, train_y, test_x)
    # predicted_proba = predict_by_gbdt(train_x, train_y, test_x, 1)
    # for i in range(2, 30):
    #     predicted_proba = pd.DataFrame(predicted_proba)
    #     predicted = pd.concat([test_data[['user_id', 'item_id']], predicted_proba], axis=1)
    #     predicted = predicted.sort_values(1, ascending=False)
    #     predicted = predicted.iloc[:i * 50, [0, 1]]
    #     evaluate(predicted)
    #

    # ===================================================================
    ts.end(sound=True)
