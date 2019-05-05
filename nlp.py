import nltk
nltk.download('punkt')
from nltk.tokenize import RegexpTokenizer
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Word2vec():

    def __init__(self): 
        filename = 'trained-models/GoogleNews-vectors-negative300.bin'
        self.model = KeyedVectors.load_word2vec_format(filename, binary=True, limit=100000) #500000

    def compare_sentences(self, sentence1, sentence2):
        #print(sentence1)
        #split sentences into only words
        tokenizer = RegexpTokenizer(r'\w+')
        tokenized_sen1 = tokenizer.tokenize(sentence1)
        tokenized_sen2 = tokenizer.tokenize(sentence2)

        #convert words to vectors and add them together for both sentences
        sentence_vec1 = list()
        for token in tokenized_sen1:
            #print(token)
            try:
                word_vec1 = self.model[token]
                sentence_vec1.append(word_vec1)
            except KeyError:
                pass
                #print(token + " not in model")
        
        sentence_vec2 = list()
        for token in tokenized_sen2:
            try:
                word_vec2 = self.model[token]
                sentence_vec2.append(word_vec2)
            except KeyError:
                pass
                #print(token + " not in model")
            
        
        summed_sentence1 = np.sum(sentence_vec1, axis=0)
        summed_sentence2 = np.sum(sentence_vec2, axis=0)
            
        # return cosine similarity between sentence vectors
        similarity = cosine_similarity([summed_sentence1],[summed_sentence2])
        #print(sentence1 + " and " + sentence2 + ": " + str(similarity))
        #print("change + receipt:")
        #print(cosine_similarity([self.model["change"]],[self.model["receipt"]]))
        #print("change + change:")
        #print(cosine_similarity([self.model["change"]],[self.model["change"]]))
        return similarity
        

