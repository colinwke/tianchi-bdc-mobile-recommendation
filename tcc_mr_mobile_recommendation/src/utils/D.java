package utils;

import java.text.SimpleDateFormat;
import java.util.Date;

public class D {

	public static void p(String s) {
		System.out.print(s);
	}

	public static void pl(String s) {
		System.out.println(s);
	}

	public static void log(String str) {
		SimpleDateFormat df = new SimpleDateFormat("MM-dd HH:mm:ss"); // 设置日期格式

		System.out.println("LOG: " + df.format(new Date()) + " || " + str);
	}

	public static void log() {
		log("");
	}
	
	private static int counter = 0;
	
	public static void initCounter() {
		counter = 0;
	}
	
	public static void printCounter(String s) {
		counter++;
		if (counter < 6) {
			System.out.println("DEBUG: counter print ||" + s);
		}
	}
}
