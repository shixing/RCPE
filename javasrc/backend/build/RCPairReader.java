package build;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;

import main.MainProcess;
import net.sf.json.JSON;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;
import net.sf.json.JSONSerializer;
import bean.RCPair;

public class RCPairReader {
	//String fileName = "result.sentence.json.txt";

	public ArrayList<RCPair> readRCPairs() throws Exception {
		ArrayList<RCPair> rcPairs = new ArrayList<RCPair>();
		BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(MainProcess.rcFile), "UTF-8"));
		String line = "";
		while ((line = reader.readLine()) != null) {
			JSON json = JSONSerializer.toJSON(line);
			JSONObject jo = JSONObject.fromObject(json);
			RCPair rcPair = new RCPair();
			rcPair.review_id = jo.getString("id");
			JSONArray rcsPairs =jo.getJSONArray("sen_pairs"); 
			rcsPairs = rcsPairs.getJSONArray(0);
			JSONArray rs = rcsPairs.getJSONArray(0);
			JSONArray cs = rcsPairs.getJSONArray(1);
			String reas = "";
			for(int i = 0; i < rs.size(); ++i){
				reas += rs.getJSONArray(i).getString(0) + " ";
			}
			rcPair.reason = reas.trim();
			String cons = "";
			for(int i = 0; i < cs.size(); ++i){
				cons += cs.getJSONArray(i).getString(0) + " ";
			}
			rcPair.consequence = cons;
			rcPairs.add(rcPair);
		}
		reader.close();
		return rcPairs;
	}

	public static void main(String[] args) {
		RCPairReader reader = new RCPairReader();
		try {
			System.out.println(reader.readRCPairs());
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
