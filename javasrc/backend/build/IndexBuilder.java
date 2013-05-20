/**
 * May 18, 2013
 * @Author Ai He
 */
package build;

import java.io.IOException;
import java.util.ArrayList;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.index.CorruptIndexException;
import org.apache.lucene.index.IndexWriter;
import bean.IndexField;
import bean.RCPair;

/**
 * May 18, 2013
 * @Author Ai He
 */
public class IndexBuilder {
	private IndexWriter indexWriter;

	/**
	 * 
	 * @param indexPath
	 *            : the path storing the index files
	 * @param create
	 *            : create new index files
	 * @return
	 * @throws Exception
	 */
	public IndexBuilder(String indexPath, boolean create) throws Exception {
		System.out.println("create: " + create);
		indexWriter = new IndexWriter(indexPath, new StandardAnalyzer(), create, IndexWriter.MaxFieldLength.LIMITED);
	}

	public void close() {
		try {
			indexWriter.optimize();
		} catch (IOException e) {
			e.printStackTrace();
		}
		try {
			indexWriter.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	/**
	 * 
	 * @param docid
	 *            the id of document to be indexed
	 * @param flds
	 *            : the list of field names to be indexed
	 * @param vals
	 *            : the list of values for fields in [flds]
	 * @throws CorruptIndexException
	 * @throws IOException
	 */
	public void index(String docid, ArrayList<String> flds, ArrayList<String> vals) throws CorruptIndexException,
			IOException {
		Document doc = new Document();

		doc.add(new Field(IndexField.BUSINESS_ID, docid, Field.Store.YES, Field.Index.NOT_ANALYZED));
		for (int i = 0; i < flds.size(); i++) {
			doc.add(new Field(flds.get(i), vals.get(i), Field.Store.YES, Field.Index.ANALYZED));
		}
		indexWriter.addDocument(doc);
	}

	/**
	 * 
	 * @param docid
	 *            : the id of document to be indexed
	 * @param flds
	 *            : a list of field names
	 * @param contents
	 *            : a list of contents for the fields
	 * @throws CorruptIndexException
	 * @throws IOException
	 */
	public void index(String docid, String[] flds, String[] contents) throws CorruptIndexException, IOException {
		Document doc = new Document();
		doc.add(new Field(IndexField.BUSINESS_ID, docid, Field.Store.YES, Field.Index.NOT_ANALYZED));

		for (int i = 0; i < flds.length; i++) {
			doc.add(new Field(flds[i], contents[i], Field.Store.YES, Field.Index.ANALYZED));
		}
		indexWriter.addDocument(doc);
	}

	public static void main(String args[]) throws Exception {
//		IndexBuilder builder = new IndexBuilder("bizidx/", true);
//		BusinessReader reader = new BusinessReader();
//		ArrayList<Business> bs = reader.readBusinesses();
//		for(Business b : bs){
//			ArrayList<String> flds = new ArrayList<>();
//			flds.add(IndexField.FULL_ADDRESS);
//			flds.add(IndexField.CITY);
//			flds.add(IndexField.NAME);
//			ArrayList<String> vals = new ArrayList<>();
//			vals.add(b.full_address);
//			vals.add(b.city);
//			vals.add(b.name);
//			builder.index(b.business_id, flds, vals);
//		}
//		builder.close();
		IndexBuilder builder = new IndexBuilder("rcidx/", true);
		RCPairReader reader = new RCPairReader();
		ArrayList<RCPair> rcs = reader.readRCPairs();
		for(RCPair rc : rcs){
			ArrayList<String> flds = new ArrayList<>();
			flds.add(IndexField.REVIEW_ID);
			flds.add(IndexField.REASON);
			flds.add(IndexField.CONSEQUENCE);
			ArrayList<String> vals = new ArrayList<>();
			vals.add(rc.review_id);
			vals.add(rc.reason);
			vals.add(rc.consequence);
			builder.index(rc.review_id, flds, vals);
		}
		builder.close();
	}
}
