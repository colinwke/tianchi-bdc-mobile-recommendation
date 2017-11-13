"""
数据清洗
1. 用户交互记录中，删除12.11, 12.12号的数据（异常数据）
2. 用户交互记录中，只保留与商品子集相关的数据
3. 重塑时间，把原始日期按照天数排列
原始日期
11.18, 11,19, ..., 11.30, 12.01, ..., 12.10, 12.13, ... 12.18
排列日期
    1,     2, ...,    13,    14, ...,    23,    24, ...    29
现在问题转化为知道1-29天的交互记录，预测第30天的购买
"""

import pandas as pd

from core.path_config import file_user
from core.path_config import file_item
from core.path_config import file_user_drop1112_subitem_reshape_date


def drop_1112_data(data):
    temp = data['time'].map(lambda x: (x[:10] != '2014-12-11') & (x[:10] != '2014-12-12'))

    return data[temp]


def get_sub_item():
    data_sub_item = pd.read_csv(file_item)
    sub_item = data_sub_item['item_id'].drop_duplicates()

    return sub_item


def union_sub_item(data):
    sub_item = get_sub_item()
    temp = data['item_id'].isin(sub_item)

    return data[temp]


def reshape_date(data):
    # 取出日期
    date = data['time'].map(lambda x: x[5:10])
    # 取出日期集合
    time_index = date.drop_duplicates().sort_values()
    time_index.index = range(len(time_index))

    dict_replace = {}
    for i in time_index.index:
        dict_replace[time_index[i]] = i + 1

    # 重塑成新的日期索引
    date = date.map(dict_replace)
    data['date'] = date

    # 取出时间中的小时
    data['hour'] = data['time'].map(lambda x: int(x[11:13]))

    return data.drop('time', axis=1)


if __name__ == '__main__':
    data = pd.read_csv(file_user)
    print('crude data length:', len(data))

    data = drop_1112_data(data)
    print('drop 11, 12 data length:', len(data))

    data = union_sub_item(data)
    print('union sub item data length:', len(data))

    data = reshape_date(data)

    data.to_csv(file_user_drop1112_subitem_reshape_date, index=False)
