package utils;

public class Utils {
	private static Utils mInstance = new Utils();

	public static Utils getInstance() {
		return mInstance;
	}

	private Utils() {
	}

	public double getRate(double top, double bottom, double naPlacer) {
		if (bottom == 0) {
			bottom = naPlacer;
		}

		return top / bottom;
	}
}
