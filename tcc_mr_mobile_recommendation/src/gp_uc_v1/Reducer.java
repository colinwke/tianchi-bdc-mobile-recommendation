package gp_uc_v1;

import java.io.IOException;
import java.util.Iterator;

import com.aliyun.odps.data.Record;
import com.aliyun.odps.mapred.ReducerBase;

import utils.Config;
import utils.D;

public class Reducer extends ReducerBase {
	private Record result;

	@Override
	public void setup(TaskContext context) throws IOException {
		result = context.createOutputRecord();

		D.log("reducer running...");
		D.initCounter();
	}

	@Override
	public void reduce(Record key, Iterator<Record> values, TaskContext context) throws IOException {

		// ȫʱ����Ϊ����
		int[] btAllCounters = { 0, 0, 0, 0 };
		String[] btAllCounterNames = { "ucbtac1", "ucbtac2", "ucbtac3", "ucbtac4" };
		// ǰһ�����Ϊ����
		int[] btOneCounters = { 0, 0, 0, 0 };
		String[] btOneCounterNames = { "ucbtoc1", "ucbtoc2", "ucbtoc3", "ucbtoc4" };
		// ǰһ�콻�������Сʱ
		int lhour = -1;
		// ǰһ�����󽻻�
		int lbt = -1;

		while (values.hasNext()) {
			Record val = values.next();

			// ͳ��ȫʱ����Ϊ
			int bt = Math.toIntExact(val.getBigint("behavior_type"));
			btAllCounters[bt - 1]++;

			// ͳ��ǰһ����Ϣ
			// ��ȡʱ��
			int date = Math.toIntExact(val.getBigint("date"));
			int hour = Math.toIntExact(val.getBigint("hour"));

			// �����ǰһ��ļ�¼
			if (date == (Config.getLabelDate() - 1)) {
				// ǰһ����Ϊ����ͳ��
				btOneCounters[bt - 1]++;
				// ǰһ����󽻻���Сʱ
				if (hour > lhour) {
					lhour = hour;
				}
				// ǰһ�콻���������Ϊ
				if (bt > lbt) {
					lbt = bt;
				}
			}

		}

		// д��keyֵ
		result.setString("user_id", key.getString("user_id"));
		result.setString("item_category", key.getString("item_category"));

		// д����Ϊ����ֵ
		for (int i = 0; i < btAllCounters.length; ++i) {
			// ȫʱ����Ϊ����
			result.setBigint(btAllCounterNames[i], (long) btAllCounters[i]);
			// ǰһ����Ϊ����
			result.setBigint(btOneCounterNames[i], (long) btOneCounters[i]);
		}

		// ��󽻻�Сʱ
		result.setBigint("uclhour", (long) lhour);
		// ��󽻻���Ϊ
		result.setBigint("uclbt", (long) lbt);

		context.write(result);
	}

	@Override
	public void cleanup(TaskContext context) throws IOException {
		D.log("reducer end.");
	}

}