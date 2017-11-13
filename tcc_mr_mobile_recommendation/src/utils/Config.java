package utils;

/**
 * 程序参数
 * 
 * @author Colin
 *
 */

public class Config {

	/**
	 * 打标日
	 * 
	 * 训练1: 28
	 * 验证1: 29
	 * 
	 * 训练2: 29
	 * 测试2: 30
	 * 
	 * （训练，验证），（训练，测试）分开
	 */

	/**
	 * MR模式
	 */
//	public static final boolean MODE_OFFLINE = true;
	 public static final boolean MODE_OFFLINE = false;

//	 public static final boolean MODE_TRAIN = true;
	public static final boolean MODE_TRAIN = false;

	// 提取特征日期段
	public static final int FEATURE_EXTRACTION_SLOT = 23;

	public static int getLabelDate() {
		
		return 27;
		
//		if (MODE_OFFLINE) {
//			if (MODE_TRAIN) {
//				return 28;
//			} else {
//				return 29;
//			}
//		} else {
//			if (MODE_TRAIN) {
//				return 29;
//			} else {
//				return 30;
//			}
//		}
	}
}
