/**
 * May 18, 2013
 * @Author Ai He
 */
package main;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

import org.dom4j.Document;
import org.dom4j.DocumentException;
import org.dom4j.Element;
import org.dom4j.io.SAXReader;
import org.xml.sax.SAXException;

import retrieve.BizRetriever;
import retrieve.RCRetriever;

import bean.Business;
import bean.IndexField;
import bean.RCPair;
import build.BusinessReader;
import build.IndexBuilder;
import build.RCPairReader;

/**
 * May 18, 2013
 * @Author Ai He
 */
public class MainProcess {
	public static String bizFile = "";
	public static String rcFile = ""; 
	static String bizIdxPath = "";
	static String rcIdxPath = "";
	static int port = 0;
	
	static{
		try {
			readConfig();
		} catch (SAXException | DocumentException e) {
			e.printStackTrace();
		}
	}
	
	static void readConfig() throws SAXException, DocumentException{
		String f = "config.xml";
		SAXReader reader = new SAXReader();
		Document document = reader.read(f);
		Element root = document.getRootElement();
		List<Element> eles = root.elements();
		try {
			bizFile = eles.get(0).attributeValue("bizFile");
			rcFile = eles.get(1).attributeValue("rcFile");
			bizIdxPath = eles.get(2).attributeValue("bizIdxPath");
			rcIdxPath = eles.get(3).attributeValue("rcIdxPath");
			port = Integer.parseInt(eles.get(4).attributeValue("port"));
		} catch (Exception e) {
			System.err.println("config.xml input wrong, use the default values");
			System.exit(-1);
		}
	}
	
	/**
	 * May 18, 2013
	 * @Author Ai He
	 * @param args
	 * @throws Exception 
	 */
	public static void main(String[] args) throws Exception {
		//String idxPath = "bizidx/";
		IndexBuilder builder = new IndexBuilder(bizIdxPath, true);
		BusinessReader reader = new BusinessReader();
		ArrayList<Business> bs = reader.readBusinesses();
		for(Business b : bs){
			ArrayList<String> flds = new ArrayList<>();
			flds.add(IndexField.FULL_ADDRESS);
			flds.add(IndexField.CITY);
			flds.add(IndexField.NAME);
			ArrayList<String> vals = new ArrayList<>();
			vals.add(b.full_address);
			vals.add(b.city);
			vals.add(b.name);
			builder.index(b.business_id, flds, vals);
		}
		builder.close();
		IndexBuilder builder2 = new IndexBuilder(rcIdxPath, true);
		RCPairReader reader2 = new RCPairReader();
		ArrayList<RCPair> rcs = reader2.readRCPairs();
		for(RCPair rc : rcs){
			ArrayList<String> flds = new ArrayList<>();
			flds.add(IndexField.REVIEW_ID);
			flds.add(IndexField.REASON);
			flds.add(IndexField.CONSEQUENCE);
			ArrayList<String> vals = new ArrayList<>();
			vals.add(rc.review_id);
			vals.add(rc.reason);
			vals.add(rc.consequence);
			builder2.index(rc.review_id, flds, vals);
		}
		builder2.close();
		RequestReceiver receiver = new RequestReceiver();
		BizRetriever.setIdxPath(bizIdxPath);
		RCRetriever.setIdxPath(rcIdxPath);
		receiver.start();
	}

}
