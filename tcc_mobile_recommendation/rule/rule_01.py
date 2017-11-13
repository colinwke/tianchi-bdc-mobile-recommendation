"""
使用规则进行预测：
1. 选取预测日前一日的数据
2. 选取加入购物车又没购买同类商品的数据
3. 选取加入购物车时间在12、13、15~23点的数据
4. 删除加入购物车后购买率低的用户数据
5. 删除加入购物车后购买率低的商品数据
6. 删除某一用户加入购物车的同类商品数过多的数据
"""

import pandas as pd

from core.evaluator import evaluate

from core.path_config import file_user_drop1112_subitem_reshape_date
from core.path_config import file_online_commit

from statistics_util.bad_cart_to_buy_record import get_bad_user
from statistics_util.bad_cart_to_buy_record import get_bad_item

# 模式选择
# IS_OFFLINE = True
IS_OFFLINE = False

# 规则参数
PARAMS_BAD_UC = 6
PARAMS_BAD_RATE_ITEM = 5
PARAMS_BAD_RATE_USER = 14
PARAMS_TIME_SLOT = [12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23]

# 加入购物车的日期
if IS_OFFLINE:
    CART_DATE = 28
else:
    CART_DATE = 29


def get_data_by_date(data, date):
    data_date = data['date'] == date
    data_date = data[data_date]

    return data_date


def get_data_by_hour(data, hour):
    data_hour = data['hour'] == hour
    data_hour = data[data_hour]

    return data_hour


def get_data_by_behavior_type(data, behavior_type):
    data_cart = data['behavior_type'] == behavior_type
    data_cart = data[data_cart]

    return data_cart


def get_cart_unbuy_data(data):
    # 加入购物车又没有购买同类商品的记录
    cart = get_data_by_behavior_type(data, 3)
    buyed = get_data_by_behavior_type(data, 4)
    cart_uc = cart['user_id'] / cart['item_category']
    buyed_uc = buyed['user_id'] / buyed['item_category']
    # 去除重复的
    cart_unbuy = cart_uc.isin(buyed_uc)
    cart_unbuy = cart[cart_unbuy == False]

    return cart_unbuy


def get_data_in_time_slot(data):
    pieces = []
    slot = PARAMS_TIME_SLOT
    for hour in slot:
        df = get_data_by_hour(data, hour)
        pieces.append(df)
    data_slot = pd.concat(pieces, ignore_index=True)

    return data_slot


def get_ui_columns(data):
    data = data[['user_id', 'item_id']]
    # 删除重复的user_id, item_id 对
    data = data.drop_duplicates(['user_id', 'item_id'])

    return data


def drop_bad_uc(data, threshold):
    uc = data['user_id'] / data['item_category']
    uc_counter = uc.value_counts()
    upper = uc_counter[uc_counter > threshold]
    data = data[uc.isin(upper.index) == False]
    print('drop bad uc: threshold = ', threshold)
    print(len(uc) - len(data))

    return data


def drop_bad_users(data, max_rate):
    bad_users = get_bad_user(max_rate)
    is_in = data['user_id'].isin(bad_users)
    print('drop bad user:')
    print(is_in.value_counts()[1])

    return data[is_in == False]


def drop_bad_items(data, max_rate):
    bad_users = get_bad_item(max_rate)
    is_in = data['item_id'].isin(bad_users)
    print('drop bad item:')
    print(is_in.value_counts()[1])

    return data[is_in == False]


if __name__ == '__main__':
    data = pd.read_csv(file_user_drop1112_subitem_reshape_date)
    data = get_data_by_date(data, CART_DATE)
    data = get_cart_unbuy_data(data)
    data = get_data_in_time_slot(data)
    data = drop_bad_users(data, PARAMS_BAD_RATE_USER)
    data = drop_bad_items(data, PARAMS_BAD_RATE_ITEM)
    data = drop_bad_uc(data, PARAMS_BAD_UC)
    data = get_ui_columns(data)
    if CART_DATE == 29:
        print('commit record counts:', len(data))
        data.to_csv(file_online_commit, index=False)
    else:
        evaluate(data)
