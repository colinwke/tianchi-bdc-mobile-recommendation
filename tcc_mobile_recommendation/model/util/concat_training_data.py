"""
训练集数据连接
"""

import pandas as pd
from core.path_config import data_folder

# ==  offline  ===================================================
pieces = []
for i in range(26, 29):
    data = pd.read_csv(folder_core + "model\\41\\tr_" + str(i) + "_u_i_c_ui_uc.csv")
    pieces.append(data)
data_train = pd.concat(pieces, ignore_index=True)
data_train.to_csv(folder_core + "model\\train_offline678_.csv", index=False)

# # ==  online  ===================================================
# pieces = []
# for i in range(25, 30):
#     data = pd.read_csv(folder_core + "model\\41\\tr_" + str(i) + "_u_i_c_ui_uc.csv")
#     pieces.append(data)
# data_train = pd.concat(pieces, ignore_index=True)
# data_train.to_csv(folder_core + "model\\train_online.csv", index=False)
