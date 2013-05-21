package bean;

import net.sf.json.JSONObject;

public class RCPair {
	public String review_id;
	public String reason;
	public String consequence;

	public JSONObject toJSONObject() {
		JSONObject jo = new JSONObject();
		jo.accumulate(IndexField.REVIEW_ID, review_id);
		jo.accumulate(IndexField.REASON, reason);
		jo.accumulate(IndexField.CONSEQUENCE, consequence);
		return jo;
	}

	@Override
	public String toString() {
		return "RCPair [review_id=" + review_id + ", reason=" + reason + ", consequence="
				+ consequence + "]";
	}
	
	
}
