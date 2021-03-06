package gp_u_v1;

import java.io.IOException;
import java.util.Iterator;

import com.aliyun.odps.data.Record;
import com.aliyun.odps.mapred.ReducerBase;

import utils.Config;
import utils.Utils;

/*

1. 行为计数（4）
2. 购买率（3）
	1. 浏览购买率
	2. 收藏购买率
	3. 加购物车购买率
3. 平均数（4）
	1. 平均每天浏览数
	2. 平均每天收藏数
	3. 平均每天购物车数
	4. 平均每天购买数
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

		// 行为计数
		int[] btCounters = { 0, 0, 0, 0 };
		String[] btCounterNames = { "ubtc1", "ubtc2", "ubtc3", "ubtc4" };

		// 前一天的行为计数
		int[] btOneCounters = { 0, 0, 0, 0 };
		String[] btOneCounterNames = { "ubtoc1", "ubtoc2", "ubtoc3", "ubtoc4" };
		// 购买率
		String[] buyRateNames = { "ubr1", "ubr2", "ubr3" };
		// 平均购买数（17天）
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

		// 写入
		// key: user_id
		result.setString("user_id", key.getString("user_id"));
		
		for (int i = 0; i < btCounters.length; i++) {
			// 行为计数
			result.setBigint(btCounterNames[i], (long) btCounters[i]);
			// 前一天行为计数
			result.setBigint(btOneCounterNames[i], (long) btOneCounters[i]);
			// 平均每天各行为数
			result.setDouble(btAverageNames[i], (double) btCounters[i] / Config.FEATURE_EXTRACTION_SLOT);
			// 购买率
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
