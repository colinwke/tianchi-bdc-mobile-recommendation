"""
坏数据统计
加入购物车数量与购买数量比率低的用户
加入购物车数量与购买数量比率低的商品
"""
import pandas as pd
import numpy as np

from core.path_config import file_gp_ui_bahavior_count

MAX_CTB_RATE_USER = 14
MAX_CTB_RATE_ITEM = 5

REPLACER_ZERO = 1


def get_bad_user(max_rate=MAX_CTB_RATE_USER):
    data = pd.read_csv(file_gp_ui_bahavior_count)
    data = data.drop(['item_id', 'browser', 'mark'], axis=1)
    data = data.groupby('user_id').aggregate(np.sum)
    # 对购买记录为0的用户进行缺失值填充
    data['buy'].replace(0, REPLACER_ZERO, inplace=True)
    # 计算转换率
    # cart buy rate 为1 最好
    # 为0 表示没有加入购物车就购买了
    # 越大越不好
    cart_buy_rate = data['cart'] / data['buy']
    # 排序
    cart_buy_rate_sort = cart_buy_rate.sort_values().reset_index()
    # 选出 bad user
    cart_to_buy_upper = cart_buy_rate_sort[cart_buy_rate_sort[0] > max_rate]

    return cart_to_buy_upper['user_id']


def get_bad_item(max_rate=MAX_CTB_RATE_ITEM):
    data = pd.read_csv(file_gp_ui_bahavior_count)
    data = data.drop(['user_id', 'browser', 'mark'], axis=1)
    data = data.groupby('item_id').aggregate(np.sum)
    # 对购买记录为0的用户进行缺失值填充
    data['buy'].replace(0, REPLACER_ZERO, inplace=True)
    # 计算转换率
    # cart buy rate 为1 最好
    # 为0 表示没有加入购物车就购买了
    # 越大越不好
    cart_buy_rate = data['cart'] / data['buy']
    # 排序
    cart_buy_rate_sort = cart_buy_rate.sort_values().reset_index()
    # 选出 bad item
    bad_item = cart_buy_rate_sort[cart_buy_rate_sort[0] > max_rate]

    return bad_item['item_id']


if __name__ == '__main__':
    pass
