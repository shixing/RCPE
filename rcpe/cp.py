import nltk
import pickle

def trainParser():
    from nltk.corpus import conll2000
    test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
    train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])
    NPChunker = ChunkParser(train_sents)
    pickle.dump(NPChunker,open('NPChunker.pickle','w'))

def getNPChunker():
    return pickle.load(open('NPChunker.pickle','r'))
                
class ChunkParser(nltk.ChunkParserI):
    def __init__(self, train_sents):
        train_data = [[(t,c) for w,t,c in nltk.chunk.tree2conlltags(sent)] for sent in train_sents]
        self.tagger = nltk.TrigramTagger(train_data)
    def parse(self, clause):
        text = nltk.word_tokenize(clause)
        sentence = nltk.pos_tag(text)
        pos_tags = [pos for (word,pos) in sentence]
        tagged_pos_tags = self.tagger.tag(pos_tags)
        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
        conlltags = [(word, pos, chunktag) for ((word,pos),chunktag)
                     in zip(sentence, chunktags)]
        for i in xrange(len(conlltags)):
            word = conlltags[i][0]+"_"+str(i)
            conlltags[i] = (word,conlltags[i][1],conlltags[i][2])
        return nltk.chunk.util.conlltags2tree(conlltags)
