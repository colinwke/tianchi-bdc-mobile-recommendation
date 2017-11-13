"""
做表格链接工作

左边：打标数据
右边：特征数据

注意：
有两个配置
1. 模式选择
2. 标记文件路径
3. 特征文件路径及特征列名
"""

import pandas as pd
from model.config import folder_core

# ---------------------------------------------------
# 程序配置
# ---------------------------------------------------

# MODE_OFFLINE = True
MODE_OFFLINE = False
# MODE_TRAIN = True
MODE_TRAIN = False

file_left_postfix = "_gp_ui_v1_gp_uc_v1_gp_u_v1_gp_i_v1"
# file_left_postfix = "_gp_ui_v1"

folder_right2 = "out_gp_c_v1"
right_columns = "item_category:STRING,cbtc1:BIGINT,cbtc2:BIGINT,cbtc3:BIGINT,cbtc4:BIGINT,cbtoc1:BIGINT,cbtoc2:BIGINT,cbtoc3:BIGINT,cbtoc4:BIGINT,cbta1:DOUBLE,cbta2:DOUBLE,cbta3:DOUBLE,cbta4:DOUBLE,cbr1:DOUBLE,cbr2:DOUBLE,cbr3:DOUBLE"

# --------------------------------------------------

# 左侧文件路径
if MODE_OFFLINE:
    if MODE_TRAIN:
        file_left = "of_tr" + file_left_postfix
    else:
        file_left = "of_te" + file_left_postfix
else:
    if MODE_TRAIN:
        file_left = "on_tr" + file_left_postfix
    else:
        file_left = "on_te" + file_left_postfix

# 右侧文件路径
folder_right1 = "D:\\ProgramFilesDev\\eclipse\\projects\\tcc_mobile_recommendation\\tcc_mr_mobile_recommendation\\warehouse\\example_project\\__tables__\\"
folder_right = folder_right1 + folder_right2

file_right = folder_right + "\\R_000000"

# 格式化列名
replace_old = [":STRING", ":BIGINT", ":DOUBLE"]
for i in replace_old:
    right_columns = right_columns.replace(i, "")

right_columns = right_columns.split(',')


# ---------------------------------------------------

def merge_by_ui(left, right):
    # 生成ui pair
    merge = pd.merge(right, left, how='right', on=['user_id', 'item_id'])

    return merge


def merge_by_uc(left, right):
    # 先要对打标数据添加 item_category
    # 打标数据为left
    data_item_info = pd.read_csv(folder_core + "tianchi_fresh_comp_train_item.csv")
    data_item_info = data_item_info[['item_id', 'item_category']]
    data_item_info = data_item_info.drop_duplicates(['item_id', 'item_category'])

    left = pd.merge(left, data_item_info, how='left', on='item_id')
    # 生成ui pair
    merge = pd.merge(right, left, how='right', on=['user_id', 'item_category'])
    merge = merge.drop('item_category', axis=1)

    return merge


def merge_by_u(left, right):
    # 生成ui pair
    merge = pd.merge(right, left, how='right', on='user_id')

    return merge


def merge_by_i(left, right):
    # 生成ui pair
    merge = pd.merge(right, left, how='right', on='item_id')

    return merge


def merge_by_c(left, right):
    # 先要对打标数据添加 item_category
    # 打标数据为left
    data_item_info = pd.read_csv(folder_core + "tianchi_fresh_comp_train_item.csv")
    data_item_info = data_item_info[['item_id', 'item_category']]
    data_item_info = data_item_info.drop_duplicates(['item_id', 'item_category'])

    left = pd.merge(left, data_item_info, how='left', on='item_id')

    merge = pd.merge(right, left, how='right', on='item_category')
    merge = merge.drop('item_category', axis=1)

    return merge


if __name__ == "__main__":
    # 左侧数据（打标数据）
    left = pd.read_csv(folder_core + "model\\" + file_left + ".csv")
    # 右侧数据（添加上的数据）
    right = pd.read_csv(file_right, header=None)

    # 指定添加数据列名
    right.columns = right_columns

    # 合并
    # merge = merge_by_ui(left, right)
    # merge = merge_by_i(left, right)
    merge = merge_by_c(left, right)
    # merge = merge_by_uc(left, right)
    # merge = merge_by_u(left, right)

    print(merge.head())

    # 保存合并数据
    merge.to_csv(folder_core + "model\\" + file_left + folder_right2[3:] + ".csv", index=False)
