package utils;

public class TabelColumnUtils {

	public static void main(String[] args) {
		String s = "user_id:STRING,item_id:STRING,uibtac1:BIGINT,uibtac2:BIGINT,uibtac3:BIGINT,uibtac4:BIGINT,uibtoc1:BIGINT,uibtoc2:BIGINT,uibtoc3:BIGINT,uibtoc4:BIGINT,lbt:BIGINT,lhour:BIGINT";

		String[] r = { ":STRING", ":BIGINT", ":DOUBLE" };

		for (int i = 0; i < r.length; ++i) {
			s = s.replaceAll(r[i], "");
		}

		System.out.println(s);
	}

}
