tcc mobile recommendation
阿里移动推荐算法 简单实现

赛题主页: https://tianchi.aliyun.com/getStart/introduction.htm?raceId=231522

主要包含两种实现方法：
1. 规则 线上F1: 9.86%
2. 模型 线上F1: 9.31%
3. 模型 + 规则: 线上F1: 10.00%

拷贝文件：
tianchi_fresh_comp_train_item.csv
tianchi_fresh_comp_train_user.csv
到data文件夹

1. 规则

1.1 预处理 preprocess_rule
	1. 运行 data_clean 进行数据清理
	2. 运行 gp_ui_bahavior_count 进行交互记录统计
	3. 运行 offline_reference_set_generator 生成线下验证集

1.2 运行 rule_01 得到规则结果
	参数 IS_OFFLINE 为模式选择
	True: 线下验证
	False: 线上提交


2. 模型

2.1 预处理 proprecess_model
	1. 运行 data_split_v1 划分数据
		参数 IS_TRAINING 选择数据集性质
		True: 训练集（有标签）
		False: 测试集（无标签）
		参数 LABEL_TRAINING_DATE 为打标日期
		28 线下训练日期 相应生成 train_28
		29 线下验证日期 相应生成 test_29
		29 线上训练日期 相应生成 train_29
		30 线上测试日期 相应生成 test_30

2.2 使用 map/reduce 生成特征 util_model
	1. 运行 mr_data_generator 生成 map/reduce 数据文件
	== java ==
	2. eclipse 下 odps 插件的安装与配置
		https://help.aliyun.com/document_detail/27981.html?spm=5176.doc27982.6.741.TQhwfQ
	3. 新建 odps 项目，拷贝 src 和 warehouse 至项目根目录下
	4. 修改 utils 下 Config 类的 getLabelDate 方法的返回值
		（返回值为打标日期，程序根据打标日期生成相对应的特征）
	5. 运行包名以 gp_ 开头下的 Driver 类，生成对应特征
	== python == 
	6. 运行 merge_utils2 合并特征
		参数 file_base 为划分的数据集
		线下训练 train_28
		线下测试 test_29
		线上训练 trian_29
		线上测试 test_30
		参数 folder_file 为 map/reduce table路径
		（如果生成的文件 test_**_u_i_c_ui_uc.csv / train_**_u_i_c_ui_uc.csv内容没有-1，也没有缺失值（,,）为正确生成）
	7. 运行 model/frame 进行模型预测

3. 模型+规则
	1. 使用模型预测出模型结果
	2. 运行 fusion_01_model_rule 进行规则筛选
		参数 IS_OFFLINE 为模式选择
		True: 线下
		False: 线上


