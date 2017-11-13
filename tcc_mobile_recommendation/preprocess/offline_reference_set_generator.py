"""
生成线下reference set
reference set为线下验证的真是答案值（购买数据集合）
线下验证集为29号购买的ui对
"""

import pandas as pd

from core.path_config import file_user_drop1112_subitem_reshape_date
from core.path_config import file_offline_reference_set

if __name__ == '__main__':
    data = pd.read_csv(file_user_drop1112_subitem_reshape_date)
    data = data[data['date'] == 29]  # 29号的交互记录
    data = data[data['behavior_type'] == 4]  # 购买的记录
    data = data[['user_id', 'item_id']]  # 获取ui对
    data = data.drop_duplicates(['user_id', 'item_id'])  # 去重

    data.to_csv(file_offline_reference_set, index=False)
