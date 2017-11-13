package gp_u_v1;

import java.io.IOException;
import java.util.Iterator;

import com.aliyun.odps.data.Record;
import com.aliyun.odps.mapred.ReducerBase;

import utils.Config;
import utils.Utils;

/*

1. ��Ϊ������4��
2. �����ʣ�3��
	1. ���������
	2. �ղع�����
	3. �ӹ��ﳵ������
3. ƽ������4��
	1. ƽ��ÿ�������
	2. ƽ��ÿ���ղ���
	3. ƽ��ÿ�칺�ﳵ��
	4. ƽ��ÿ�칺����
*/

public class Reducer extends ReducerBase {
	private Record result;
	
	private Utils utils = Utils.getInstance();

	@Override
	public void setup(TaskContext context) throws IOException {
		result = context.createOutputRecord();
	}

	@Override
	public void reduce(Record key, Iterator<Record> values, TaskContext context) throws IOException {

		// ��Ϊ����
		int[] btCounters = { 0, 0, 0, 0 };
		String[] btCounterNames = { "ubtc1", "ubtc2", "ubtc3", "ubtc4" };

		// ǰһ�����Ϊ����
		int[] btOneCounters = { 0, 0, 0, 0 };
		String[] btOneCounterNames = { "ubtoc1", "ubtoc2", "ubtoc3", "ubtoc4" };
		// ������
		String[] buyRateNames = { "ubr1", "ubr2", "ubr3" };
		// ƽ����������17�죩
		String[] btAverageNames = { "ubta1", "ubta2", "ubta3", "ubta4" };

		while (values.hasNext()) {
			Record val = values.next();

			int bt = Math.toIntExact(val.getBigint("behavior_type"));
			int date = Math.toIntExact(val.getBigint("date"));

			btCounters[bt - 1]++;

			if (date == Config.getLabelDate() - 1) {
				btOneCounters[bt - 1]++;
			}
		}

		// д��
		// key: user_id
		result.setString("user_id", key.getString("user_id"));
		
		for (int i = 0; i < btCounters.length; i++) {
			// ��Ϊ����
			result.setBigint(btCounterNames[i], (long) btCounters[i]);
			// ǰһ����Ϊ����
			result.setBigint(btOneCounterNames[i], (long) btOneCounters[i]);
			// ƽ��ÿ�����Ϊ��
			result.setDouble(btAverageNames[i], (double) btCounters[i] / Config.FEATURE_EXTRACTION_SLOT);
			// ������
			if (i < 3) {
				result.setDouble(buyRateNames[i], utils.getRate(btCounters[i], btCounters[3], 1));
			}

		}

		context.write(result);

	}

	@Override
	public void cleanup(TaskContext context) throws IOException {
	}

}
