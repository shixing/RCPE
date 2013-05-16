package app;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.List;

import org.dom4j.Document;
import org.dom4j.DocumentException;
import org.dom4j.Element;
import org.dom4j.io.SAXReader;

public class Final {
	
	public static HashMap<String, String> id2Content = new HashMap<String, String>();
	public static String content = "content_rea";
	/**
	 * @param args
	 * @throws DocumentException 
	 * @throws IOException 
	 * @throws ClassNotFoundException 
	 */
	public static void main(String[] args) throws DocumentException, IOException {
		SAXReader reader = new SAXReader();
		Document document = reader.read("parameter.xml");
		Element root = document.getRootElement();
		List<Element> eles = root.elements();
		try {
			Main.termweight = eles.get(0).attributeValue("termweight");
			if(!(Main.termweight.equals("idf") || Main.termweight.equals("logentropy"))) throw new Exception();
			Main.dimension = Integer.parseInt(eles.get(1).attributeValue("dimension"));
			Main.minfrequency = Integer.parseInt(eles.get(2).attributeValue("minfrequency"));
			Main.numRunsForOverlap = Integer.parseInt(eles.get(3).attributeValue("numRunsForOverlap"));
			Main.ngram = eles.get(4).attributeValue("ngram");
			if(!(Main.ngram.equals("1") || Main.ngram.equals("2") || Main.ngram.equals("2-3"))) throw new Exception();
			Main.posTag = Boolean.parseBoolean(eles.get(5).attributeValue("posTag"));
		} catch (Exception e) {
			System.err.println("paramter.xml input wrong, use the default values");
			System.exit(-1);
		}
		
//		ParseFiles2 parseFiles2 = new ParseFiles2();
//		parseFiles2.parseFile();
//		Preprocess preprocess = new Preprocess();
//		preprocess.process();
		
		for (int i = 1; i <= 5; ++i) {
			content = "content_star" + i;
			id2Content = new HashMap<String, String>();
			File[] content_2 = new File(content + "/" + content.substring(content.indexOf('_') + 1)
					+ "/raw").listFiles();
			for (File f : content_2) {
				File ff = new File(f, "index.txt");
				BufferedReader r = new BufferedReader(new InputStreamReader(
						new FileInputStream(ff), "utf-8"));
				String line = "";
				String content = "";
				while ((line = r.readLine()) != null) {
					content += line + "\n";
				}
				r.close();
				id2Content.put(f.getName(), content);
			}
			LSAProcess lsaProcess = new LSAProcess();
			lsaProcess.buildIndex();
			lsaProcess.lsa();
			lsaProcess.cluster();
		}
		
		content = "content_star";
		id2Content = new HashMap<String, String>();
		File[] content_2 = new File(content + "/" + content.substring(content.indexOf('_') + 1)
				+ "/raw").listFiles();
		for (File f : content_2) {
			File ff = new File(f, "index.txt");
			BufferedReader r = new BufferedReader(new InputStreamReader(
					new FileInputStream(ff), "utf-8"));
			String line = "";
			String content = "";
			while ((line = r.readLine()) != null) {
				content += line + "\n";
			}
			r.close();
			id2Content.put(f.getName(), content);
		}
		LSAProcess lsaProcess = new LSAProcess();
		lsaProcess.buildIndex();
		lsaProcess.lsa();
		lsaProcess.cluster();
	}
}
