package utils;

/**
 * �������
 * 
 * @author Colin
 *
 */

public class Config {

	/**
	 * �����
	 * 
	 * ѵ��1: 28
	 * ��֤1: 29
	 * 
	 * ѵ��2: 29
	 * ����2: 30
	 * 
	 * ��ѵ������֤������ѵ�������ԣ��ֿ�
	 */

	/**
	 * MRģʽ
	 */
//	public static final boolean MODE_OFFLINE = true;
	 public static final boolean MODE_OFFLINE = false;

//	 public static final boolean MODE_TRAIN = true;
	public static final boolean MODE_TRAIN = false;

	// ��ȡ�������ڶ�
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
