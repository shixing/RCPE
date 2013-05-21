package retrieve;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.search.IndexSearcher;

public abstract class Retriever {
	IndexSearcher _isearcher = null;
	Analyzer _analyzer = null;

	public Retriever(String indexDir) throws Exception {
		_isearcher = new IndexSearcher(indexDir);
		_analyzer = new StandardAnalyzer();
	}
}
