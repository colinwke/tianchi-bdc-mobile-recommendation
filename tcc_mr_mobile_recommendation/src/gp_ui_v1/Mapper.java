package gp_ui_v1;

import java.io.IOException;

import com.aliyun.odps.data.Record;
import com.aliyun.odps.mapred.MapperBase;

import utils.Config;
import utils.D;

public class Mapper extends MapperBase {
	private Record key;
	private Record value;

	@Override
	public void setup(TaskContext context) throws IOException {
		key = context.createMapOutputKeyRecord();
		value = context.createMapOutputValueRecord();

		D.log("mapper running...");
	}

	@Override
	public void map(long recordNum, Record record, TaskContext context) throws IOException {

		/**
		 * 仅在提取特征日期段中提取特征
		 * offline:
		 * 训练集提取特征：1-16，打标17
		 * 验证集提取特征：2-17，打标18
		 * 
		 * online:
		 * 训练集提取特征：2-17，打标18
		 * 测试集提取特征：3-18，打标19
		 */

		// 获取时间
		int date = Math.toIntExact(record.getBigint("date"));

		if ((Config.getLabelDate() - Config.FEATURE_EXTRACTION_SLOT) <= date && date <= (Config.getLabelDate() - 1)) {
			// key
			key.setString("user_id", record.getString("user_id"));
			key.setString("item_id", record.getString("item_id"));
			// value
			value.setBigint("behavior_type", record.getBigint("behavior_type"));
			value.setBigint("date", (long) date);
			value.setBigint("hour", record.getBigint("hour"));

			context.write(key, value);
		}
	}

	@Override
	public void cleanup(TaskContext context) throws IOException {
		D.log("mapper end.");
	}

}
