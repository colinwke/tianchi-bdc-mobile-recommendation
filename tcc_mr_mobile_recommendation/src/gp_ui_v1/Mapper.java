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
		 * ������ȡ�������ڶ�����ȡ����
		 * offline:
		 * ѵ������ȡ������1-16�����17
		 * ��֤����ȡ������2-17�����18
		 * 
		 * online:
		 * ѵ������ȡ������2-17�����18
		 * ���Լ���ȡ������3-18�����19
		 */

		// ��ȡʱ��
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
