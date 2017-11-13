"""
数据划分

已知（1-29）号交互记录，预测30号购买记录

线下：
训练：提取标签：28，提取特征2-27
验证：提取标签：29，提取特征3-28
线上：
训练：提取标签：29，提取特征3-28
测试：预测标签：30，提取特征4-29
"""

import pandas as pd

from core.path_config import file_user_drop1112_subitem_reshape_date

from core.path_config import file_offline_trainset
from core.path_config import file_offline_testset
from core.path_config import file_online_trainset
from core.path_config import file_online_testset

# 参数
# OFF_LINE = True  # 线下测试
OFF_LINE = False  # 线上测试

if OFF_LINE:
    # 线下测试
    # 训练打标日期
    LABEL_TRAINING_DATE = 28
    # 提取记录日期（打标日期的前一天）
    INSTANCE_TRAINING_DATE = LABEL_TRAINING_DATE - 1
    # 测试打标日期
    LABEL_TEST_DATE = 29
    # 提取记录日期（打标前一天）
    INSTANCE_TEST_DATE = LABEL_TEST_DATE - 1
else:
    # 线上提交
    # 训练打标日期
    LABEL_TRAINING_DATE = 29
    # 提取记录日期（打标日期的前一天）
    INSTANCE_TRAINING_DATE = LABEL_TRAINING_DATE - 1
    # 测试打标日期
    LABEL_TEST_DATE = 30
    # 提取记录日期（打标前一天）
    INSTANCE_TEST_DATE = LABEL_TEST_DATE - 1


def print_pn_rate(data):
    counter = data['label'].value_counts()

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
    data_test = data[data['date'] == INSTANCE_TEST_DATE]
    data_test = data_test.drop_duplicates(['user_id', 'item_id'])

    return data_test[['user_id', 'item_id']]


if __name__ == "__main__":
    # 读取数据文件
    data = pd.read_csv(file_user_drop1112_subitem_reshape_date)
    # 删除多余列
    data = data.drop(['user_geohash', 'item_category'], axis=1)

    # 训练集数据
    data_train = get_label_trainset(data)
    # 测试数据集
    data_test = get_label_testset(data)

    # 保存
    if OFF_LINE:
        # 线下数据集
        data_train.to_csv(file_offline_trainset, index=False)
        data_test.to_csv(file_offline_testset, index=False)
    else:
        # 线上数据集
        data_train.to_csv(file_online_trainset, index=False)
        data_test.to_csv(file_online_testset, index=False)
