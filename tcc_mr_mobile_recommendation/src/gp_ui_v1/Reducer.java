package gp_ui_v1;

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

		// 全时间行为计数
		int[] btAllCounters = { 0, 0, 0, 0 };
		String[] btAllCounterNames = { "uibtac1", "uibtac2", "uibtac3", "uibtac4" };
		// 前一天的行为计数
		int[] btOneCounters = { 0, 0, 0, 0 };
		String[] btOneCounterNames = { "uibtoc1", "uibtoc2", "uibtoc3", "uibtoc4" };
		// 前一天交互的最大小时
		int lhour = -1;
		// 前一天的最大交互
		int lbt = -1;

		while (values.hasNext()) {
			Record val = values.next();

			// 统计全时间行为
			int bt = Math.toIntExact(val.getBigint("behavior_type"));
			btAllCounters[bt - 1]++;

			// 统计前一天信息
			// 获取时间
			int date = Math.toIntExact(val.getBigint("date"));
			int hour = Math.toIntExact(val.getBigint("hour"));

			// 打标日前一天的记录
			if (date == (Config.getLabelDate() - 1)) {

				D.printCounter("date: " + date + " hour: " + hour + " bt: " + bt + " lhour" + hour);
				// 前一天行为计数统计
				btOneCounters[bt - 1]++;
				// 前一天最后交互的小时
				if (hour > lhour) {
					lhour = hour;
				}
				// 前一天交互的最大行为
				if (bt > lbt) {
					lbt = bt;
				}
			}

		}

		// 写入key值
		result.setString("user_id", key.getString("user_id"));
		result.setString("item_id", key.getString("item_id"));

		// 写入行为计数值
		for (int i = 0; i < btAllCounters.length; ++i) {
			// 全时间行为计数
			result.setBigint(btAllCounterNames[i], (long) btAllCounters[i]);
			// 前一天行为计数
			result.setBigint(btOneCounterNames[i], (long) btOneCounters[i]);
		}

		// 最后交互小时
		result.setBigint("lhour", (long) lhour);
		// 最大交互行为
		result.setBigint("lbt", (long) lbt);

		context.write(result);
	}

	@Override
	public void cleanup(TaskContext context) throws IOException {
		D.log("reducer end.");
	}

}
