"""
特征合并
"""

import pandas as pd
from core.path_config import file_item

# ---------------------------------------------------
# 程序配置
# ---------------------------------------------------

file_base = "tr_27"

file_u = "out_gp_u_v1"
file_i = "out_gp_i_v1"
file_c = "out_gp_c_v1"
file_ui = "out_gp_ui_v1"
file_uc = "out_gp_uc_v1"

columns_u = "user_id:STRING,ubtc1:BIGINT,ubtc2:BIGINT,ubtc3:BIGINT,ubtc4:BIGINT,ubtoc1:BIGINT,ubtoc2:BIGINT,ubtoc3:BIGINT,ubtoc4:BIGINT,ubta1:DOUBLE,ubta2:DOUBLE,ubta3:DOUBLE,ubta4:DOUBLE,ubr1:DOUBLE,ubr2:DOUBLE,ubr3:DOUBLE"
columns_i = "item_id:STRING,ibtc1:BIGINT,ibtc2:BIGINT,ibtc3:BIGINT,ibtc4:BIGINT,ibtoc1:BIGINT,ibtoc2:BIGINT,ibtoc3:BIGINT,ibtoc4:BIGINT,ibta1:DOUBLE,ibta2:DOUBLE,ibta3:DOUBLE,ibta4:DOUBLE,ibr1:DOUBLE,ibr2:DOUBLE,ibr3:DOUBLE"
columns_c = "item_category:STRING,cbtc1:BIGINT,cbtc2:BIGINT,cbtc3:BIGINT,cbtc4:BIGINT,cbtoc1:BIGINT,cbtoc2:BIGINT,cbtoc3:BIGINT,cbtoc4:BIGINT,cbta1:DOUBLE,cbta2:DOUBLE,cbta3:DOUBLE,cbta4:DOUBLE,cbr1:DOUBLE,cbr2:DOUBLE,cbr3:DOUBLE"
columns_ui = "user_id:STRING,item_id:STRING,uibtac1:BIGINT,uibtac2:BIGINT,uibtac3:BIGINT,uibtac4:BIGINT,uibtoc1:BIGINT,uibtoc2:BIGINT,uibtoc3:BIGINT,uibtoc4:BIGINT,lbt:BIGINT,lhour:BIGINT"
columns_uc = "user_id:STRING,item_category:STRING,ucbtac1:BIGINT,ucbtac2:BIGINT,ucbtac3:BIGINT,ucbtac4:BIGINT,ucbtoc1:BIGINT,ucbtoc2:BIGINT,ucbtoc3:BIGINT,ucbtoc4:BIGINT,uclbt:BIGINT,uclhour:BIGINT"

folder_file = "D:\\ProgramFilesDev\\eclipse\\projects\\tcc_mobile_recommendation\\tcc_mr_mobile_recommendation\\warehouse\\example_project\\__tables__\\"
file_base_mr = "\\R_000000"


def add_columns(data, columns):
    # 格式化列名
    replace_old = [":STRING", ":BIGINT", ":DOUBLE"]
    for i in replace_old:
        columns = columns.replace(i, "")
    columns = columns.split(',')
    data.columns = columns

    return data


# ==  merge  ======================================================

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


# ==================================================================
if __name__ == "__main__":
    ts = TimeStamp()
    # 读取交互记录
    left = pd.read_csv(folder_core + "model\\" + file_base + ".csv")

    # 合并数据构造
    right_u = pd.read_csv(folder_file + file_u + file_base_mr, header=None)
    right_i = pd.read_csv(folder_file + file_i + file_base_mr, header=None)
    right_c = pd.read_csv(folder_file + file_c + file_base_mr, header=None)
    right_ui = pd.read_csv(folder_file + file_ui + file_base_mr, header=None)
    right_uc = pd.read_csv(folder_file + file_uc + file_base_mr, header=None)

    ts.cat("load data success!")

    right_u = add_columns(right_u, columns_u)
    right_i = add_columns(right_i, columns_i)
    right_c = add_columns(right_c, columns_c)
    right_ui = add_columns(right_ui, columns_ui)
    right_uc = add_columns(right_uc, columns_uc)

    # 开始合并
    left = merge_by_u(left, right_u)
    left = merge_by_i(left, right_i)
    left = merge_by_c(left, right_c)
    left = merge_by_ui(left, right_ui)
    left = merge_by_uc(left, right_uc)

    ts.cat("merge data success!")

    # 保存
    left.to_csv(folder_core + "model\\" + file_base + "_u_i_c_ui_uc.csv", index=False)

    ts.end()
