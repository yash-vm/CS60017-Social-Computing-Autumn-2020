import pandas as pd
import numpy as np
import os
import string
from string import digits
import re
import time
import itertools
#import gensim
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import MWETokenizer, word_tokenize
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import TrigramAssocMeasures
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier

def to_lower(sample):
    sample=sample.lower()
    return sample

def rem_punctuations(sample):
    sample=re.sub('''[!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~]+''', ' ', sample)
    sample=sample.split()
    return ' '.join(sample)

def rem_hyphen(sample):
    sample=re.sub('-',' ',sample)
    sample=sample.split()
    return ' '.join(sample)


def preprocess(sample):
    sample=to_lower(sample)
    sample=rem_punctuations(sample)
    sample=rem_hyphen(sample)
    sample=sample.split()
    sample=[word for word in sample if len(word)>1]
    return ' '.join(sample)
data=pd.read_csv('/home/yash/Documents/socompML/data/train.tsv',sep='\t' ) 
testdata = pd.read_csv('/home/yash/Documents/socompML/data/test.tsv',sep='\t' ) 

data.reset_index(drop=True, inplace=True)

testdata.reset_index(drop=True, inplace=True)

data.dropna(axis=0, subset=['text'], inplace=True)
testdata.dropna(axis=0, subset=['text'], inplace=True)


docs=list(data['text'].apply(preprocess))
testdocs = list(testdata['text'].apply(preprocess))



docs=np.array(docs)
testdocs = np.array(testdocs)


data.text = docs
testdata.text = testdocs
#data.to_csv('train_preprocessed.tsv', sep='\t', index=False)
#testdata.to_csv('test_preprocessed.tsv', sep='\t', index=False)





data_text = data['text']
data_hateful = data['hateful']

testdata_text = testdata['text']


tf_vectorizer = CountVectorizer(max_df=0.8, min_df = 0.0002118016) # or term frequency

X_train_tf = tf_vectorizer.fit_transform(data_text)

X_test_tf = tf_vectorizer.transform(testdata_text)



rf = RandomForestClassifier()
rf.fit(X_train_tf, data_hateful)

y_pred = rf.predict(X_test_tf)
testdata["pred"] = y_pred
prediction = pd.DataFrame([testdata.id, testdata.pred]).transpose()
prediction.to_csv('/home/yash/Documents/socompML/predictions/RF.csv', sep=',', index=False)