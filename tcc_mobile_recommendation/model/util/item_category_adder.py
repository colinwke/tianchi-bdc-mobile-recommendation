"""
添加item_category列
"""

import pandas as pd
from core.path_config import file_item


def add_item_category(data):
    data_item_info = pd.read_csv(file_item)
    data_item_info = data_item_info[['item_id', 'item_category']]
    data_item_info = data_item_info.drop_duplicates(['item_id', 'item_category'])
    data = pd.merge(data, data_item_info, how='left', on='item_id')

    return data
