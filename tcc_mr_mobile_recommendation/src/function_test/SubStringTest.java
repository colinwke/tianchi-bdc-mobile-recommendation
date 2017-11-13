package function_test;

import utils.D;

public class SubStringTest {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		String s = "abcdefghijklmnopqrstuvwxyz";
		String time = "2014-12-17 03";
		
		D.pl(time.substring(0, 10));
		D.pl(time.substring(11, 13));
		D.pl(time.substring(5, 7));
		D.pl(time.substring(8, 10));
	}

}
