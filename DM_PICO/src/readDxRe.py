#!/usr/bin/python
import re
import random
import nltk


myRe = '((^Title: |^Abstract: )(.*))'
p = re.compile(myRe)

filesInput = ['pure-doc-dx (copy).txt', 'pure-doc-tx (copy).txt']

documents = []
listMyWords = []
dirMain = '/home/kimiko/Downloads/clinical query/_pure-doc-set/'

for fileOne in filesInput:
    PubmedFile= dirMain+fileOne
    with open(PubmedFile) as fTxtOrg:
        listDocOrg = fTxtOrg.readlines()
    with open(dirMain+'output'+fileOne[8:11]+'.csv', 'wb') as outf:
        for myString in listDocOrg:
            myResult = p.search(myString)
            if myResult <> None:
                myData = re.sub('^Title: |^Abstract: ','',myResult.group())
                outf.write(myData)
                listMyWords.extend(myData.split())
                documents.append((myData.split(),fileOne[9:11]))
random.shuffle(documents)
#print len(documents), myData.split()
print 'len(listMyWords): ', len(listMyWords)
#exit()

all_words = nltk.FreqDist(listMyWords)
print 'len(all_words): ', len(all_words)
#print 'type(all_words): ', type(all_words), len(all_words)
word_features = all_words.keys()[:len(all_words)/10]
#print 'word_features: ', type(word_features), word_features
#exit()

def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


favorDiagnostic = ['intervention', 'risk', 'therapy', 'disease', 'participants', 'effects', 'subjects', 'patient', 'response', 'outcomes', 'events','outcome', 'findings', 'performance', 'statistically', 'evaluation', 'population']
print '\ndocument_features(favorDiagnostic): ', document_features(favorDiagnostic)


featuresets = [(document_features(d), c) for (d,c) in documents]
sizeTest = len(documents)/10
print '\nsizeTest: ', sizeTest

train_set, test_set = featuresets[sizeTest:], featuresets[:sizeTest]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print 'nltk.classify.accuracy(classifier, test_set): ', nltk.classify.accuracy(classifier, test_set), '\n'

#0.81
classifier.show_most_informative_features(10)
