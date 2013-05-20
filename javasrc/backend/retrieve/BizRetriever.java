/**
 * May 18, 2013
 * @Author Ai He
 */
package retrieve;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import org.apache.lucene.document.Document;
import org.apache.lucene.queryParser.QueryParser;
import org.apache.lucene.search.BooleanClause;
import org.apache.lucene.search.BooleanClause.Occur;
import org.apache.lucene.search.BooleanQuery;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import bean.Business;
import bean.IndexField;

/**
 * May 18, 2013
 * 
 * @Author Ai He
 */
public class BizRetriever extends Retriever{
	static BizRetriever bizRetriever = null;
	static String idxPath = "";
	
	public static void setIdxPath(String idxPath) {
		BizRetriever.idxPath = idxPath;
	}

	public static BizRetriever getObject() throws Exception{
		if(bizRetriever == null){
			bizRetriever = new BizRetriever(idxPath);
		}return bizRetriever;
	}

	public BizRetriever(String indexDir) throws Exception {
		super(indexDir);
	}

	public ArrayList<Business> search(String field, String keyword, int searchResultNum) {
		try {
			System.out.println("keyword: " + keyword);
			QueryParser qp = new QueryParser(field, _analyzer);
			Query query = qp.parse(keyword);
			System.out.println("query: " + query.toString());
			System.out.println("result number: " + searchResultNum);
			TopDocs topDocs = _isearcher.search(query, searchResultNum);
			int number = searchResultNum;
			System.out.println("hit Number: " + topDocs.totalHits);
			if (topDocs.totalHits < number) {
				number = topDocs.totalHits;
			}
			List<ScoreDoc> scoreDocs = Arrays.asList(topDocs.scoreDocs);
			Collections.sort(scoreDocs, new Comparator<ScoreDoc>() {
				@Override
				public int compare(ScoreDoc o1, ScoreDoc o2) {
					if (o1.score < o2.score) {
						return 1;
					} else if (o1.score == o2.score) {
						return 0;
					} else {
						return -1;
					}
				}
			});
			ArrayList<Business> buzs = new ArrayList<>();
			for (int i = 0; i < number; i++) {
				Document doc = _isearcher.doc(scoreDocs.get(i).doc);
				String bid = doc.get(IndexField.BUSINESS_ID);
				String full_addr = doc.get(IndexField.FULL_ADDRESS);
				String city = doc.get(IndexField.CITY);
				String name = doc.get(IndexField.NAME);
				Business buz = new Business();
				buz.business_id = bid;
				buz.city = city;
				buz.name = name;
				buz.full_address = full_addr;
				buzs.add(buz);
			}
			System.out.println("business number = " + buzs.size());
			return buzs;
		} catch (Exception e) {
			e.printStackTrace();
		}
		return null;

	}

	
	/**
	 * complex search
	 * 
	 * @param flds
	 *            : a list of fields to be queried
	 * @param keywords
	 *            : a list of keywords corresponding to flds
	 * @param flags
	 *            : flags for the fields --- Occur.MUST, Occur.SHOULD,
	 *            Occur.MUST_TO
	 * @param searchResultNum
	 *            the top N documents to be retrieved
	 * @param listDocs
	 *            : returned document objects
	 * @return
	 */
	public ArrayList<Business> search(String[] flds, String[] keywords,
			BooleanClause.Occur[] flags, int searchResultNum) {
		try {
			BooleanQuery bq = new BooleanQuery();
			for (int i = 0; i < flds.length; i++) {
				QueryParser _qp = new QueryParser(flds[i], _analyzer);
				Query query = _qp.parse(keywords[i]);
				bq.add(query, flags[i]);
			}

			System.out.println("query: " + bq.toString());

			ArrayList<Document> docs = new ArrayList<Document>();
			long t1 = System.currentTimeMillis();
			TopDocs topDocs = _isearcher.search(bq, searchResultNum);
			int number = searchResultNum;
			if (topDocs.totalHits < number)
				number = topDocs.totalHits;
			List<ScoreDoc> scoreDocs = Arrays.asList(topDocs.scoreDocs);
			Collections.sort(scoreDocs, new Comparator<ScoreDoc>() {
				@Override
				public int compare(ScoreDoc o1, ScoreDoc o2) {
					if (o1.score < o2.score) {
						return 1;
					} else if (o1.score == o2.score) {
						return 0;
					} else {
						return -1;
					}
				}
			});
			for (int i = 0; i < number; i++) {
				Document doc = _isearcher.doc(scoreDocs.get(i).doc);
				docs.add(doc);
			}
			ArrayList<Business> buzs = new ArrayList<>();
			long t2 = System.currentTimeMillis();
			for (int i = 0; i < number; i++) {
				Document doc = _isearcher.doc(scoreDocs.get(i).doc);
				String bid = doc.get(IndexField.BUSINESS_ID);
				String full_addr = doc.get(IndexField.FULL_ADDRESS);
				String city = doc.get(IndexField.CITY);
				String name = doc.get(IndexField.NAME);
				Business buz = new Business();
				buz.business_id = bid;
				buz.city = city;
				buz.name = name;
				buz.full_address = full_addr;
				buzs.add(buz);
			}
			System.out.println("cost: " + (t2 - t1) + " ms");
			System.out.println("hit: " + topDocs.totalHits);
			System.out.println("business number = " + buzs.size());

			return buzs;
		} catch (Exception e) {
			e.printStackTrace();
		}
		return null;
	}
	
	public ArrayList<Business> search(ArrayList<String> flds, ArrayList<String> keywords,
			ArrayList<Occur> flags, int searchResultNum) {
		String[] fldsS = new String[flds.size()]; 
		String[] keywordsS = new String[keywords.size()];
		BooleanClause.Occur[] flagsS = new Occur[flags.size()];
		return search(flds.toArray(fldsS), keywords.toArray(keywordsS), flags.toArray(flagsS), searchResultNum);
	}

	public static void main(String args[]) throws Exception {
		String indexpath = "./bizidx/";
		BizRetriever bizRetriever = new BizRetriever(indexpath);
		ArrayList<Business> buzs = bizRetriever.search(IndexField.NAME, "tax Service", 100);
		System.out.println(buzs);
	}
}
