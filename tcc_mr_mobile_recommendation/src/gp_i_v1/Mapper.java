package gp_i_v1;

import java.io.IOException;

import com.aliyun.odps.data.Record;
import com.aliyun.odps.mapred.MapperBase;

import utils.Config;

public class Mapper extends MapperBase {
	private Record key;
	private Record value;

	@Override
	public void setup(TaskContext context) throws IOException {
		key = context.createMapOutputKeyRecord();
		value = context.createMapOutputValueRecord();
	}

	@Override
	public void map(long recordNum, Record record, TaskContext context) throws IOException {

		// 获取时间
		int date = Math.toIntExact(record.getBigint("date"));

		if ((Config.getLabelDate() - Config.FEATURE_EXTRACTION_SLOT) <= date && date <= (Config.getLabelDate() - 1)) {
			// key: item id
			key.setString("item_id", record.getString("item_id"));

			// value: behavior type and time
			value.setBigint("behavior_type", record.getBigint("behavior_type"));
			value.setBigint("date", (long) date);

			context.write(key, value);
		}
	}

	@Override
	public void cleanup(TaskContext context) throws IOException {
	}

}