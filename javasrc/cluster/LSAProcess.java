package app;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FilenameFilter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.util.Arrays;
import java.util.Date;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Hashtable;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;
import javax.sound.midi.SysexMessage;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.shingle.ShingleAnalyzerWrapper;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriter.MaxFieldLength;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.search.NGramPhraseQuery;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;
import org.dom4j.Document;
import org.dom4j.DocumentHelper;
import org.dom4j.Element;
import pitt.search.lucene.FilePositionDoc;
import pitt.search.lucene.IndexFilePositions;
import pitt.search.lucene.PorterAnalyzer;
import pitt.search.semanticvectors.BuildIndex;
import pitt.search.semanticvectors.CloseableVectorStore;
import pitt.search.semanticvectors.ClusterResults;
import pitt.search.semanticvectors.ClusterVectorStore;
import pitt.search.semanticvectors.CompareTerms;
import pitt.search.semanticvectors.CompoundVectorBuilder;
import pitt.search.semanticvectors.DocVectors;
import pitt.search.semanticvectors.FlagConfig;
import pitt.search.semanticvectors.IncrementalDocVectors;
import pitt.search.semanticvectors.IncrementalTermVectors;
import pitt.search.semanticvectors.LSA;
import pitt.search.semanticvectors.LuceneUtils;
import pitt.search.semanticvectors.ObjectVector;
import pitt.search.semanticvectors.Search;
import pitt.search.semanticvectors.SearchResult;
import pitt.search.semanticvectors.TermVectorsFromLucene;
import pitt.search.semanticvectors.VectorStore;
import pitt.search.semanticvectors.VectorStoreReader;
import pitt.search.semanticvectors.VectorStoreReaderLucene;
import pitt.search.semanticvectors.VectorStoreWriter;
import pitt.search.semanticvectors.VerbatimLogger;
import pitt.search.semanticvectors.vectors.Vector;

public class LSAProcess {
	
	private static HashSet<String> stopSet = new HashSet<String>();
	static{
		getStopSet();
	}

 	void lsa() throws IllegalArgumentException, IOException {
 		File index = new File("index");
 		File vector = new File("vector");
 		if(!vector.exists()){
 			vector.mkdirs();
 		}
 		File[] namesDir = index.listFiles(new FilenameFilter() {
			
			@Override
			public boolean accept(File dir, String name) {
				
				return name.equals(Final.content.substring(Final.content.indexOf('_') + 1));
			}
		});
		for (File name : namesDir){
			if(name.getName().startsWith(".")) continue;
			File file = new File(vector.getAbsolutePath() + "/" + name.getName() + "/");
			if(!file.exists()){
				file.mkdirs();
			}
			String cmd = "-luceneindexpath";
			cmd += " " + name.getAbsolutePath() + "/positional_index/";
			cmd += " -dimension " + Main.dimension;
//			cmd += " -dimension 250 -minfrequency 3";
			cmd += " -minfrequency " + Main.minfrequency;
			cmd += " -termweight " + Main.termweight;
			cmd += " -porterstemmer";
			cmd += " " + vector.getAbsolutePath() + "/" + name.getName() + "/"; 
			cmd += " " + vector.getAbsolutePath() + "/" + name.getName() + "/";
			String[] args = cmd.split("\\s+");
			build(args);
		}
	}

	private void build(String[] args) {
		FlagConfig flagConfig = null;
		try {
			flagConfig = FlagConfig.getFlagConfig(args);
			args = flagConfig.remainingArgs;
		} catch (IllegalArgumentException e) {
			throw e;
		}

		if (flagConfig.luceneindexpath().isEmpty()) {
			throw (new IllegalArgumentException("-luceneindexpath must be set."));
		}

		String luceneIndex = flagConfig.luceneindexpath();
		String termFile = args[1] + "termvectors.bin";
		String docFile = args[0] + "docvectors.bin";

		try {
			TermVectorsFromLucene vecStore;
			if (!flagConfig.initialtermvectors().isEmpty()) {
				vecStore = TermVectorsFromLucene.createTermBasedRRIVectors(flagConfig);
			} else {
				vecStore = TermVectorsFromLucene.createTermVectorsFromLucene(flagConfig, null);
			}

			// Create doc vectors and write vectors to disk.
			switch (flagConfig.docindexing()) {
			case INCREMENTAL:
				VectorStoreWriter.writeVectors(termFile, flagConfig, vecStore);
				IncrementalDocVectors.createIncrementalDocVectors(vecStore, flagConfig,
						luceneIndex, "incremental_" + docFile);
				IncrementalTermVectors itermVectors = null;

				for (int i = 1; i < flagConfig.trainingcycles(); ++i) {
					itermVectors = new IncrementalTermVectors(flagConfig, luceneIndex, docFile);

					VectorStoreWriter.writeVectors(
							"incremental_termvectors" + flagConfig.trainingcycles() + ".bin",
							flagConfig, itermVectors);

					if (i == flagConfig.trainingcycles() - 1)
						docFile = "docvectors" + flagConfig.trainingcycles() + ".bin";

					IncrementalDocVectors.createIncrementalDocVectors(itermVectors, flagConfig,
							luceneIndex, "incremental_" + docFile);
					break;
				}
			case INMEMORY:
				DocVectors docVectors = new DocVectors(vecStore, flagConfig);
				for (int i = 1; i < flagConfig.trainingcycles(); ++i) {
//					VerbatimLogger.info("\nRetraining with learned document vectors ...");
					vecStore = TermVectorsFromLucene.createTermVectorsFromLucene(flagConfig,
							docVectors);
					docVectors = new DocVectors(vecStore, flagConfig);
				}
				// At end of training, convert document vectors from ID keys to
				// pathname keys.
				VectorStore writeableDocVectors = docVectors.makeWriteableVectorStore();

				if (flagConfig.trainingcycles() > 1) {
					termFile = "termvectors" + flagConfig.trainingcycles() + ".bin";
					docFile = "docvectors" + flagConfig.trainingcycles() + ".bin";
				}
//				VerbatimLogger.info("Writing term vectors to " + termFile + "\n");
				VectorStoreWriter.writeVectors(termFile, flagConfig, vecStore);
//				VerbatimLogger.info("Writing doc vectors to " + docFile + "\n");
				VectorStoreWriter.writeVectors(docFile, flagConfig, writeableDocVectors);
				break;
			case NONE:
				// Write term vectors to disk even if there are no docvectors to
				// output.
//				VerbatimLogger.info("Writing term vectors to " + termFile + "\n");
				VectorStoreWriter.writeVectors(termFile, flagConfig, vecStore);
				break;
			default:
				throw new IllegalStateException("No procedure defined for -docindexing "
						+ flagConfig.docindexing());
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	private static void getStopSet() {
		try {
			String line = "";
			BufferedReader bfr = new BufferedReader(new InputStreamReader(new FileInputStream("stop.txt"), "utf-8"));
			while((line = bfr.readLine()) != null){
				stopSet.add(line.trim());
			}
			bfr.close();
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
	}

	@SuppressWarnings({ "resource", "deprecation" })
	void buildIndex() {
		File[] names = new File(/*"contents"*/Final.content).listFiles();

		for (File name : names) {
			String indexPath = name.getAbsolutePath().replace(/*"contents"*/Final.content, "index");
			File indexDir = new File(indexPath);
			if(indexDir.exists()){
				Util.deleteDir(indexDir);
			}
			String path = indexDir + "/positional_index";
			File INDEX_DIR = new File(path);
			String cmd = name.getAbsolutePath() + "/raw/";
			String[] args = cmd.split("\\s+");

			FlagConfig flagConfig = null;
			if (args.length > 0) {
				flagConfig = FlagConfig.getFlagConfig(args);
				// Allow for the specification of a directory to write the index
				// to.
				if (flagConfig.luceneindexpath().length() > 0)
					INDEX_DIR = new File(flagConfig.luceneindexpath() + INDEX_DIR.getName());
			}
			if (INDEX_DIR.exists()) {
				System.out.println(INDEX_DIR.getAbsolutePath());
				System.out.println("Cannot save index to '" + INDEX_DIR
						+ "' directory, please delete it first");
				System.exit(1);
			}
			try {
				IndexWriter writer;
				if (flagConfig.porterstemmer()) {
					// Create IndexWriter using porter stemmer without any
					// stopword list.
					ShingleAnalyzerWrapper shingleAnalyzerWrapper = new ShingleAnalyzerWrapper(new PorterAnalyzer(), 2, 2);
					IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_30, shingleAnalyzerWrapper);
					writer = new IndexWriter(FSDirectory.open(INDEX_DIR), config);
				} else {
					// Create IndexWriter using StandardAnalyzer without any
					// stopword list.
					ShingleAnalyzerWrapper shingleAnalyzerWrapper = null;
					IndexWriterConfig config = null;
					if(Main.ngram.equals("2-3")){
						shingleAnalyzerWrapper = new ShingleAnalyzerWrapper(
								new StandardAnalyzer(Version.LUCENE_30, stopSet), 2, 3);
						config = new IndexWriterConfig(Version.LUCENE_30, shingleAnalyzerWrapper);
					}else if(Main.ngram.equals("2")){
						shingleAnalyzerWrapper = new ShingleAnalyzerWrapper(
								new StandardAnalyzer(Version.LUCENE_30, stopSet), 2, 2);
						config = new IndexWriterConfig(Version.LUCENE_30, shingleAnalyzerWrapper);
					}else {
						config = new IndexWriterConfig(Version.LUCENE_30,
								new StandardAnalyzer(Version.LUCENE_30, stopSet));
					}
					writer = new IndexWriter(FSDirectory.open(INDEX_DIR), config);
					
				}

				final File docDir = new File(flagConfig.remainingArgs[0]);
				if (!docDir.exists() || !docDir.canRead()) {
					throw new IOException("Document directory '" + docDir.getAbsolutePath()
							+ "' does not exist or is not readable, please check the path");
				}

				Date start = new Date();

				System.out.println("Indexing to directory '" + INDEX_DIR + "'...");
				indexDocs(writer, docDir);
				System.out.println("Optimizing...");
				writer.optimize();
				writer.close();

				Date end = new Date();
				System.out.println(end.getTime() - start.getTime() + " total milliseconds");

			} catch (IOException e) {
				System.out.println(" caught a " + e.getClass() + "\n with message: "
						+ e.getMessage());
			}

		}

	}

	void indexDocs(IndexWriter writer, File file) throws IOException {
		// Do not try to index files that cannot be read.
		if (file.canRead()) {
			if (file.isDirectory()) {
				String[] files = file.list();
				// An IO error could occur.
				if (files != null) {
					for (int i = 0; i < files.length; i++) {
						// Skip dot files.
						if (!files[i].startsWith(".")) {
							indexDocs(writer, new File(file, files[i]));
						}
					}
				}
			} else {
				System.out.println("adding " + file);
				try {
					// Use FilePositionDoc rather than FileDoc such that term
					// positions are indexed also.
					writer.addDocument(FilePositionDoc.Document(file)); 
					 
				}
				// At least on windows, some temporary files raise this
				// exception with an "access denied" message. Checking if the
				// file can be read doesn't help
				catch (FileNotFoundException fnfe) {
					fnfe.printStackTrace();
				}
			}
		}
	}

	
	void compare(String doc1, String doc2) throws IOException {
		String cmd = "-luceneindexpath index/Abby_Watkins/positional_index/ -queryvectorfile docvectors.bin";
		cmd += " " + doc1 + " " + doc2;
		String[] args = cmd.split("\\s+");
		CompareTerms.main(args);
	}
	
	void cluster() throws IOException{
		HashMap<String, Integer> numClusterMap = new HashMap<String, Integer>();
		numClusterMap.put(Final.content.substring(Final.content.indexOf('_') + 1), 15);
		File vector = new File("vector");
		File[] namesDir = vector.listFiles(new FilenameFilter() {
			
			@Override
			public boolean accept(File dir, String name) {
				
				return name.equals(Final.content.substring(Final.content.indexOf('_') + 1));
			}
		});
		for(File name : namesDir){
			int numCluster = numClusterMap.get(name.getName());
			String cmd = "-numclusters " + numCluster + " "+ name.getAbsolutePath() + "/docvectors.bin";
			String args [] = cmd.split("\\s+");
			int numRunsForOverlap = Main.numRunsForOverlap;
	
		    FlagConfig flagConfig = FlagConfig.getFlagConfig(args);
		    args = flagConfig.remainingArgs;
			if (args.length != 1) {
				System.out.println("Wrong number of arguments.");
				// usage();
				return;
			}
	
		    CloseableVectorStore vecReader;
			try {
				vecReader = VectorStoreReader.openVectorStore(args[0], flagConfig);
			} catch (IOException e) {
				System.err.println("Failed to open vector store from file: '" + args[0] + "'");
				System.err.println(e.getMessage());
				throw new IllegalArgumentException("Failed to parse arguments for ClusterVectorStore");
			}
	
		    // Allocate vector memory and read vectors from store.
			System.out.println("Reading vectors into memory ...");
			int numVectors = vecReader.getNumVectors();
			ObjectVector[] resultsVectors = new ObjectVector[numVectors];
			Enumeration<ObjectVector> vecEnum = vecReader.getAllVectors();
			int offset = 0;
			while (vecEnum.hasMoreElements()) {
				resultsVectors[offset] = vecEnum.nextElement();
				++offset;
			}
		    vecReader.close();
	
		    Hashtable<String, int[]> mainOverlapResults = null;
		    ClusterResults.Clusters clusters = null;
			for (int runNumber = 0; runNumber < numRunsForOverlap; ++runNumber) {
				// Perform clustering and print out results.
				System.out.println("Clustering vectors ..." + (numRunsForOverlap - runNumber));
				clusters = ClusterResults.kMeansCluster(resultsVectors, flagConfig);
	
				Hashtable<String, int[]> newOverlapResults = ClusterVectorStore.clusterOverlapMeasure(
						clusters.clusterMappings, resultsVectors);
	
				if (mainOverlapResults == null) {
					mainOverlapResults = newOverlapResults;
				} else {
					mergeTables(newOverlapResults, mainOverlapResults);
				}
			}
			
			Document document = DocumentHelper.createDocument();
			Element root = document.addElement("clustering");
			root.addAttribute("name", name.getName().replace('_', ' '));
			File resultDir = new File("result");
			if(!resultDir.exists()){
				resultDir.mkdirs();
			}
			StringBuffer buffer = new StringBuffer();
			for (int i = 0; i < numCluster; ++i) {
				System.out.println("Cluster " + i);
//				buffer.append("Cluster " + i + "\n");
				Element entity = root.addElement("entity");
				entity.addAttribute("id", i + "");
				boolean atLeastOne = false;
				for (int j = 0; j < clusters.clusterMappings.length; ++j) {
					if (clusters.clusterMappings[j] == i) {
						atLeastOne = true;
						System.out.println(resultsVectors[j].getObject());
//						buffer.append(resultsVectors[j].getObject() + "\n");
						String rank = resultsVectors[j].getObject().toString();
						rank = rank.substring(rank.indexOf("raw/") + 4, rank.indexOf("/index.txt"));
						while(rank.startsWith("0") && !rank.equals("0")) rank = rank.substring(1);
						Element ele = entity.addElement("doc");
						ele.addAttribute("rank", rank);
						ele.addText(Final.id2Content.get(rank));
					}
				}
				if(!atLeastOne){
					root.remove(entity);
				}
				System.out.println("*********");
			}
			
			Util.WriteOutXML(document, resultDir.getAbsolutePath() + "/" + name.getName() + ".clust.xml");
		}
	}
	
	private static void mergeTables(Hashtable<String, int[]> newTable,
			Hashtable<String, int[]> mainTable) {
		for (String key : mainTable.keySet()) {
			int[] values = mainTable.get(key);
			int[] newValues = newTable.get(key);
			for (int i = 0; i < mainTable.get(key).length; ++i) {
				values[i] += newValues[i];
			}
		}
	}

	public static void main(String[] args) throws IllegalArgumentException, IOException {
		
	}
}
