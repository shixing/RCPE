/**
 * May 18, 2013
 * @Author Ai He
 */
package bean;

import net.sf.json.JSONObject;

/**
 * May 18, 2013
 * @Author Ai He
 */
public class Business {
	public String business_id;
	public String full_address;
	public String city;
	public String name;

	public JSONObject toJSONObject() {
		JSONObject jo = new JSONObject();
		jo.accumulate(IndexField.BUSINESS_ID, business_id);
		jo.accumulate(IndexField.FULL_ADDRESS, full_address);
		jo.accumulate(IndexField.CITY, city);
		jo.accumulate(IndexField.NAME, name);
		return jo;
	}
	
}
