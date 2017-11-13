"""
规则模型融合
先使用模型预测的结果
再使用规则进一步过滤
"""

import pandas as pd

from core.evaluator import evaluate

from model.config import folder_core
from model.config import path_commit
from model.util.item_category_adder import add_item_category

# 模式选择
# IS_OFFLINE = True
IS_OFFLINE = False

# 规则参数
PARAMS_MAX_UC = 6
PARAMS_MAX_RATE_USER = 14
PARAMS_MAX_RATE_ITEM = 5

file_model2 = "\\2017-2-242"
# file_model2 = "\\5tr01"

file_model1 = "D:\\DataAnalysis\\tcc_mobile_recommendation\\data\\commit"
file_model3 = "\\tianchi_mobile_recommendation_predict.csv"

file_model_addtion = folder_core + "gp_uc_count_behavior.csv"


# == drop bad record =======================================================================

def get_ui_columns(data):
    # data = data.drop(['behavior_type', 'user_geohash', 'item_category', 'time'], axis=1)
    data = data[['user_id', 'item_id']]
    ui = data['user_id'] / data['item_id']

    return data[ui.duplicated() == False]  # drop duplicated ui


def drop_bad_users(data, max_rate=15):
    # bad_users = pd.read_csv(folder_core + 'statistic\\bad_user.csv', header=None)
    from rule.statistic.user_cart_to_buy_ratio import get_bad_user
    bad_users = get_bad_user(max_rate)
    print("bad user count:", len(bad_users))
    # dataFrame to series
    # bad_users = bad_users[0]

    is_in = data['user_id'].isin(bad_users)
    # print(is_in.value_counts())

    return data[is_in == False]


def drop_bad_items(data):
    bad_users = pd.read_csv(folder_core + 'statistic\\bad_item.csv', header=None)
    # dataFrame to series
    bad_users = bad_users[0]

    is_in = data['item_id'].isin(bad_users)
    print(is_in.value_counts())

    return data[is_in == False]


def drop_bad_uc(data, threshold):
    data = add_item_category(data)

    uc = data['user_id'] / data['item_category']

    uc_counter = uc.value_counts()
    upper = uc_counter[uc_counter > threshold]
    data = data[uc.isin(upper.index) == False]

    print("drop bad uc: threshold = ", threshold)
    print(len(uc) - len(data))

    return data


# =========================================================================


if __name__ == "__main__":
    data = pd.read_csv(file_model1 + file_model2 + file_model3)
    # 模型数据merge原始数据得到完整信息的模型数据
    data_addition = pd.read_csv(file_model_addtion)
    data = pd.merge(data, data_addition, how="left", on=['user_id', 'item_id'])

    # == 进行过滤 ===================================================
    data = drop_bad_users(data, PARAMS_MAX_RATE_USER)
    print("drop bad user length:", len(data))
    data = drop_bad_items(data)
    print("drop bad item length:", len(data))
    data = drop_bad_uc(data, PARAMS_MAX_UC)
    print("drop bad uc length:", len(data))

    # 保存
    data = get_ui_columns(data)
    print("commit record count:", len(data))
    if IS_OFFLINE:
        evaluate(data)
    else:
        data.to_csv(path_commit, index=False)

    # # == 参数调优 ===================================================
    # data = drop_bad_items(data)
    # data = drop_bad_uc(data, PARAMS_MAX_UC)
    # for i in range(2, 19):
    #     print(i)
    #     data1 = drop_bad_users(data, i)
    #     # 保存
    #     data1 = get_ui_columns(data1)
    #     if IS_OFFLINE:
    #         evaluate(data1)
    #     else:
    #         data1.to_csv(path_commit, index=False)







# =========================================================================
# =========================================================================
