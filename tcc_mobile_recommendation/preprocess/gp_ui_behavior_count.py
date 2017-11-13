"""
对ui对（user_id, item_id）的行为进行统计
结果为：
user_id, item_id, browser, mark, cart, buy
"""

import pandas as pd

from core.path_config import file_user_drop1112_subitem_reshape_date
from core.path_config import file_gp_ui_bahavior_count

if __name__ == '__main__':
    data = pd.read_csv(file_user_drop1112_subitem_reshape_date)

    val = data.values
    dictionary = {}  # {(user_id, item_id): [user_id, item_id, 0, 0, 0, 0]}
    for i in range(len(val)):
        ui = (val[i, 0], val[i, 1])
        if ui not in dictionary:
            dictionary[ui] = [val[i, 0], val[i, 1], 0, 0, 0, 0]
        dictionary[ui][val[i, 2] + 1] += 1

    temp = pd.DataFrame(list(dictionary.values()))
    temp.columns = ['user_id', 'item_id', 'browser', 'mark', 'cart', 'buy']

    temp.to_csv(file_gp_ui_bahavior_count, index=False)
