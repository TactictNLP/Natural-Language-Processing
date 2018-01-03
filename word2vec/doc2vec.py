# gensim modules
from gensim import utils
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec
# numpy
import numpy
# shuffle
from random import shuffle
# logging
import logging
import os.path
import sys
import pickle

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))

class LabeledLineSentence(object):
    def __init__(self, sources):
        self.sources = sources
        flipped = {}
        # make sure that keys are unique
        for key, value in sources.items():
            if value not in flipped:
                flipped[value] = [key]
            else:
                raise Exception('Non-unique prefix encountered')
    def __iter__(self):
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    yield LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no])
    def to_array(self):
        self.sentences = []
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    self.sentences.append(LabeledSentence(
                        utils.to_unicode(line).split(), [prefix + '_%s' % item_no]))
        return self.sentences
    def sentences_perm(self):
        shuffle(self.sentences)
        return self.sentences

if (os.path.isfile('doc2vec_model.d2v') and os.path.isfile('doc2vec_model.bin')):
    doc_model = Doc2Vec.load('doc2vec_model.d2v')
    #word_model
else:
    sources = {'train-unsup.txt':'TRAIN_UNS'}
    sentences = LabeledLineSentence(sources)
    model = Doc2Vec(min_count=1, window=10, size=100, sample=1e-4, negative=5, workers=7)
    model.build_vocab(sentences.to_array())  
    for epoch in range(5):
        logger.info('Epoch %d' % epoch)
        model.train(sentences.sentences_perm(),total_examples=model.corpus_count)
        print("\nthis is count :",model.corpus_count)
    
    model.wv.save_word2vec_format('doc2vec_model.bin',binary=False)
    model.save('doc2vec_model.d2v')
     
    
'''
outputfile = open("labe_file.txt","w",encoding= 'utf8')
outputfile.write(str(sentences.to_array()));
outputfile.close()
'''

    
    
    
    
