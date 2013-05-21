/**
 * May 18, 2013
 * @Author Ai He
 */
package main;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import org.apache.lucene.search.BooleanClause.Occur;
import retrieve.BizRetriever;
import retrieve.RCRetriever;
import bean.Business;
import bean.IndexField;
import bean.RCPair;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

/**
 * May 18, 2013
 * 
 * @Author Ai He
 */
public class RequestReceiver {

	//int port = 12345;
	int socketBufSize = 1024 * 1024;

	void start() throws Exception {
		ServerSocket server = new ServerSocket(MainProcess.port);
		while (true) {
			Socket client = server.accept();
			client.setReceiveBufferSize(socketBufSize);
			client.setSendBufferSize(socketBufSize);
			CreateServer newServer = new CreateServer(client);
			newServer.start();
		}
	}
}

class CreateServer extends Thread {
	Socket client;
	PrintWriter out;
	BufferedReader in;
	public CreateServer(Socket s) throws Exception {
		client = s;
		out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(client.getOutputStream(), "UTF-8")));
		in = new BufferedReader(new InputStreamReader(client.getInputStream(), "UTF-8"));
	}

	public void run() {
		try {
			StringBuilder sb = new StringBuilder();
			String line;
			while (true) {
				line = in.readLine();
				if (line == null || line.equals("###")) {
					break;
				}
				sb.append(line);
			}
			System.out.println(sb.toString());
			String res = sb.toString().trim();
			JSONObject jsonObj;
			try {
				jsonObj = JSONObject.fromObject(res);
			} catch (Exception e) {
				return;
			}
			if (jsonObj.containsKey("business")) {
				jsonObj = jsonObj.getJSONObject("business");
				ArrayList<String> flds = new ArrayList<>();
				ArrayList<String> fldsR = new ArrayList<>();
				flds.add(IndexField.FULL_ADDRESS);
				flds.add(IndexField.CITY);
				flds.add(IndexField.NAME);
				ArrayList<String> vals = new ArrayList<>();
				ArrayList<Occur> flags = new ArrayList<>();
				for (int i = 0; i < flds.size(); i++) {
					JSONArray arr = null;
					if (jsonObj.has(flds.get(i))) {
						arr = jsonObj.getJSONArray(flds.get(i));
						fldsR.add(flds.get(i));
					}
					if (arr != null && !arr.isEmpty()) {
						vals.add(arr.getString(0));
						if (arr.get(1).equals("must")) {
							flags.add(Occur.MUST);
						} else if (arr.get(1).equals("mustnot")) {
							flags.add(Occur.MUST_NOT);
						} else {
							flags.add(Occur.SHOULD);
						}
					}
				}
				ArrayList<Business> buzs = BizRetriever.getObject().search(fldsR, vals, flags, MainProcess.returnNum);
				for (Business buz : buzs) {
					JSONObject jo = buz.toJSONObject();
					out.println(jo.toString());
				}
			}else if(jsonObj.containsKey("rcpair")){
				jsonObj = jsonObj.getJSONObject("rcpair");
				ArrayList<String> flds = new ArrayList<>();
				ArrayList<String> fldsR = new ArrayList<>();
				flds.add(IndexField.REVIEW_ID);
				flds.add(IndexField.REASON);
				flds.add(IndexField.CONSEQUENCE);
				ArrayList<String> vals = new ArrayList<>();
				ArrayList<Occur> flags = new ArrayList<>();
				for (int i = 0; i < flds.size(); i++) {
					JSONArray arr = null;
					if (jsonObj.has(flds.get(i))) {
						arr = jsonObj.getJSONArray(flds.get(i));
						fldsR.add(flds.get(i));
					}
					if (arr != null && !arr.isEmpty()) {
						vals.add(arr.getString(0));
						if (arr.get(1).equals("must")) {
							flags.add(Occur.MUST);
						} else if (arr.get(1).equals("mustnot")) {
							flags.add(Occur.MUST_NOT);
						} else {
							flags.add(Occur.SHOULD);
						}
					}
				}
				ArrayList<RCPair> rcPairs = RCRetriever.getObject().search(fldsR, vals, flags, MainProcess.returnNum);
				for (RCPair rcPair : rcPairs) {
					JSONObject jo = rcPair.toJSONObject();
					out.println(jo.toString());
				}
			}
			out.flush();
			out.close();
			in.close();
			client.close();

		} catch (Exception e) {
			e.printStackTrace();
			try {
				if (out != null)
					out.close();
			} catch (Exception e1) {
				e1.printStackTrace();
			}
			try {
				if (in != null)
					in.close();
			} catch (Exception e1) {
				e1.printStackTrace();
			}
			try {
				client.close();
			} catch (Exception e1) {
				e1.printStackTrace();
			}
		} finally {
			try {
				if (out != null)
					out.close();
			} catch (Exception e1) {
				e1.printStackTrace();
			}
			try {
				if (in != null)
					in.close();
			} catch (Exception e1) {
				e1.printStackTrace();
			}
			try {
				client.close();
			} catch (Exception e1) {
				e1.printStackTrace();
			}
		}
	}
}
