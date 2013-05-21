/**
 * May 18, 2013
 * @Author Ai He
 */
package test;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

/**
 * May 18, 2013
 * 
 * @Author Ai He
 */
public class Test {

	/**
	 * May 18, 2013
	 * 
	 * @Author Ai He
	 * @param args
	 */
	public static void main(String[] args) {
		JSONObject jo = new JSONObject();
		jo.accumulate("name", "tax service");
		jo.accumulate("state", "CA");
		Socket client = null;
		try {
			client = new Socket("localhost", 12345);
			client.setReceiveBufferSize(1024 * 1024);
			PrintWriter out = new PrintWriter(new OutputStreamWriter(client.getOutputStream(), "UTF-8"));
			BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream(), "UTF-8"));
			out.println(jo.toString());
			out.println("###");
			out.flush();

			String line;
			JSONArray array = new JSONArray();
			while (true) {
				line = in.readLine();
				if (line == null)
					break;
				JSONObject joR = JSONObject.fromObject(line);
				array.add(joR);
			}
			System.out.println(array);
		} catch (Exception e) {
			e.printStackTrace(System.out);
		} finally {
			try {
				client.close();
			} catch (IOException e) {

				e.printStackTrace();
			}
		}
	}
}
