"""
数据划分

使用数据集：user_subitem_drop1112_reshape_date.csv

对特定的某一天进行打标选作训练集
例如：选择对27号的数据进行打标，作为训练集
"""

import pandas as pd
from model.config import folder_core

IS_TRAINING = True
# IS_TRAINING = False

# 打标日期
LABEL_TRAINING_DATE = 27
# 样本数据来源（前一天的交互记录）
INSTANCE_TRAINING_DATE = LABEL_TRAINING_DATE - 1

file_data = folder_core + "user_subitem_drop1112_reshape_date.csv"


def print_pn_rate(data):
    counter = data['label'].value_counts()

    print(counter)
    print("positive:negative = 1:" + str(round(counter[0] / counter[1])))


def get_label_trainset(data):
    # 取出label day 前一天的记录作为打标记录
    data_train = data[data['date'] == INSTANCE_TRAINING_DATE]
    # 训练样本中，删除重复的样本
    data_train = data_train.drop_duplicates(['user_id', 'item_id'])
    data_train_ui = data_train['user_id'] / data_train['item_id']

    # 使用label day 的实际购买情况进行打标
    data_label = data[data['date'] == LABEL_TRAINING_DATE]
    data_label_buy = data_label[data_label['behavior_type'] == 4]
    data_label_buy_ui = data_label_buy['user_id'] / data_label_buy['item_id']

    # 对前一天的交互记录进行打标
    data_train_labeled = data_train_ui.isin(data_label_buy_ui)
    dict = {True: '1', False: '0'}
    data_train_labeled = data_train_labeled.map(dict)

    data_train['label'] = data_train_labeled
    print_pn_rate(data_train)

    return data_train[['user_id', 'item_id', 'label']]


def get_label_testset(data):
    # 测试集选为上一天所有的交互数据
    data_test = data[data['date'] == INSTANCE_TRAINING_DATE]
    data_test = data_test.drop_duplicates(['user_id', 'item_id'])

    return data_test[['user_id', 'item_id']]


if __name__ == "__main__":
    # 读取数据文件
    data = pd.read_csv(file_data)
    # 删除多余列
    data = data.drop(['user_geohash', 'item_category'], axis=1)

    if IS_TRAINING:
        # 训练集数据
        data_train = get_label_trainset(data)
        data_train.to_csv(folder_core + "model\\tr_" + str(LABEL_TRAINING_DATE) + ".csv", index=False)
    else:
        # 测试集数据
        data_test = get_label_testset(data)
        data_test.to_csv(folder_core + "model\\te_" + str(LABEL_TRAINING_DATE) + ".csv", index=False)
