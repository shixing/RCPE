package app;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;

import org.dom4j.Document;
import org.dom4j.Element;
import org.dom4j.io.SAXReader;

public class StarsCluster {
	
	HashMap<Integer, HashSet<Element>> star2Eles = new HashMap<Integer, HashSet<Element>>();
	HashMap<String, HashSet<String>> conreaMap = new HashMap<String, HashSet<String>>();
	
	public void readConReaMap(File file) throws Throwable{
		BufferedReader r = new BufferedReader(new InputStreamReader(new FileInputStream(file), "utf-8"));
		String line = "";
		while((line = r.readLine()) != null){
			String[] strs = line.split("\\s");
			conreaMap.put(strs[0], new HashSet<String>());
			for(int i = 1; i < strs.length; ++i){
				conreaMap.get(strs[0]).add(strs[i]);
			}
		}
		r.close();
	}
	
	public Element readStars(File file) throws Throwable{
		SAXReader reader = new SAXReader();
		Document doc = reader.read(file);
		Element root = doc.getRootElement();
		List<Element> eles = root.elements();
		Element ele = null;
		for(Element e : eles){
			if(e.attributeValue("id").equals("17")){
				ele = e;
				break;
			}
		}
		return ele;
	}

	
	public void cluster(Element element){
		List<Element> eles = element.elements();
		HashMap<Integer, HashSet<Element>> star2Ele = star2Eles;
		for(Element ele : eles){
			String[] sent = ele.getTextTrim().toLowerCase().split("\\s+");
			boolean one = false;
			boolean two = false;
			boolean three = false;
			boolean four = false;
			boolean five = false;
			for(int i = 0; i < sent.length; ++i){
				if(sent[i].equals("1") || sent[i].equals("one")){
					if(i + 1 < sent.length && sent[i+1].contains("star")){
						one = true;
						break;
					}
				}
				if(sent[i].equals("2") || sent[i].equals("two")){
					if(i + 1 < sent.length && sent[i+1].contains("star")){
						two = true;
						break;
					}
				}
				if(sent[i].equals("3") || sent[i].equals("three")){
					if(i + 1 < sent.length && sent[i+1].contains("star")){
						three = true;
						break;
					}
				}
				if(sent[i].equals("4") || sent[i].equals("four")){
					if(i + 1 < sent.length && sent[i+1].contains("star")){
						four = true;
						break;
					}
				}
				if(sent[i].equals("5") || sent[i].equals("five")){
					if(i + 1 < sent.length && sent[i+1].contains("star")){
						five = true;
						break;
					}
				}
			}
			if(one){
				if(!star2Ele.containsKey(1)){
					star2Ele.put(1, new HashSet<Element>());
				}
				star2Ele.get(1).add(ele);
			}
			if(two){
				if(!star2Ele.containsKey(2)){
					star2Ele.put(2, new HashSet<Element>());
				}
				star2Ele.get(2).add(ele);
			}
			if(three){
				if(!star2Ele.containsKey(3)){
					star2Ele.put(3, new HashSet<Element>());
				}
				star2Ele.get(3).add(ele);
			}
			if(four){
				if(!star2Ele.containsKey(4)){
					star2Ele.put(4, new HashSet<Element>());
				}
				star2Ele.get(4).add(ele);
			}
			if(five){
				if(!star2Ele.containsKey(5)){
					star2Ele.put(5, new HashSet<Element>());
				}
				star2Ele.get(5).add(ele);
			}
		}
	}
	
	public void findReason() throws Throwable{
		ArrayList<Integer> sList = new ArrayList<Integer>(star2Eles.keySet());
		Collections.sort(sList);
		for(Integer i : sList){
			HashSet<Element> eles = star2Eles.get(i);
			File star1 = new File("content_star"+ i +"/star" + i +"/raw");
			star1.mkdirs();
			Util.deleteDir(star1);
			for(Element ele : eles){
				String cid = ele.attributeValue("rank");
				for(String rid : conreaMap.get(cid)){
					File s = new File(star1, rid);
					s.mkdirs();
					File idx = new File(s, "index.txt");
					File reaIdx = new File(new File("content_rea/rea/raw/" + rid), "index.txt");
					BufferedReader r = new BufferedReader(new InputStreamReader(new FileInputStream(reaIdx), "utf-8"));
					String line = "";
					String txt = "";
					while((line = r.readLine()) != null){
						txt += line + "\n";
					}
					Util.WriteOut(idx.getAbsolutePath(), txt);
					r.close();
				}
			}
		}
		File star1 = new File("content_star/star/raw");
		star1.mkdirs();
		Util.deleteDir(star1);
		for(Integer i : sList){
			HashSet<Element> eles = star2Eles.get(i);
			for(Element ele : eles){
				String cid = ele.attributeValue("rank");
				for(String rid : conreaMap.get(cid)){
					File s = new File(star1, rid);
					s.mkdirs();
					File idx = new File(s, "index.txt");
					File reaIdx = new File(new File("content_rea/rea/raw/" + rid), "index.txt");
					BufferedReader r = new BufferedReader(new InputStreamReader(new FileInputStream(reaIdx), "utf-8"));
					String line = "";
					String txt = "";
					while((line = r.readLine()) != null){
						txt += line + "\n";
					}
					Util.WriteOut(idx.getAbsolutePath(), txt);
					r.close();
				}
			}
		}
	}
	
	/**
	 * @param args
	 */
	public static void main(String[] args) throws Throwable{
		StarsCluster cluster = new StarsCluster();
		cluster.readConReaMap(new File("rcMap.txt"));
		Element element = cluster.readStars(new File("result/cons.clust.xml"));
		cluster.cluster(element);
		cluster.findReason();
	}

}
