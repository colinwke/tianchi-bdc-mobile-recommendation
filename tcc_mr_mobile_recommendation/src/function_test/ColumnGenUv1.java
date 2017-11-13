package function_test;

import utils.D;

public class ColumnGenUv1 {

	public static void main(String[] args) {
		String[] btCounterNames = { "ubtc1", "ubtc2", "ubtc3", "ubtc4" };
		String[] btOneCounterNames = { "ubtoc1", "ubtoc2", "ubtoc3", "ubtoc4" };
		String[] btAverageNames = { "ubta1", "ubta2", "ubta3", "ubta4" };
		String[] buyRateNames = { "ubr1", "ubr2", "ubr3" };

		for (int i = 0; i < btCounterNames.length; ++i) {
			D.p(btCounterNames[i] + ":BIGINT,");
		}
		for (int i = 0; i < btCounterNames.length; ++i) {
			D.p(btOneCounterNames[i] + ":BIGINT,");
		}
		for (int i = 0; i < btCounterNames.length; ++i) {
			D.p(btAverageNames[i] + ":DOUBLE,");
		}
		for (int i = 0; i < buyRateNames.length; ++i) {
			D.p(buyRateNames[i] + ":DOUBLE,");
		}
	}

}
