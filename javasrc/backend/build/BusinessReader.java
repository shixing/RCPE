/**
 * May 18, 2013
 * @Author Ai He
 */
package build;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import bean.Business;
import main.MainProcess;
import net.sf.json.JSON;
import net.sf.json.JSONObject;
import net.sf.json.JSONSerializer;

/**
 * May 18, 2013
 * 
 * @Author Ai He
 */
public class BusinessReader {
	//String fileName = "yelp_academic_dataset_business.json";

	public ArrayList<Business> readBusinesses() throws Exception {
		ArrayList<Business> businesses = new ArrayList<Business>();
		BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(MainProcess.bizFile), "UTF-8"));
		String line = "";
		while ((line = reader.readLine()) != null) {
			JSON json = JSONSerializer.toJSON(line);
			JSONObject jo = JSONObject.fromObject(json);
			Business business = new Business();
			business.business_id = jo.getString("business_id");
			business.city = jo.getString("city");
			business.full_address = jo.getString("full_address");
			business.name = jo.getString("name");
//			System.out.println(business);
			businesses.add(business);
		}
		reader.close();
		return businesses;
	}

	public static void main(String[] args) {
		BusinessReader reader = new BusinessReader();
		try {
			reader.readBusinesses();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
