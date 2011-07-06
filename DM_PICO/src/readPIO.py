#!/usr/bin/python
import re
import random
import nltk
import csv


myRe = '((^Title: |^Abstract: )(.*))'
p = re.compile(myRe)

#filesInput = ['pure-doc-dx.txt', 'pure-doc-tx.txt']
#filesInput = ['intervention.txt', 'patient.txt', 'outcome.txt']
#filesInput = ['intervention.txt', 'patient.txt']
#filesInput = ['intervention.txt', 'outcome.txt']
filesInput = ['patient.txt', 'outcome.txt']


documents = []
listMyWords = []
dirMain = ''
outputPercentageFilenameBase = 'outputPer'


for fileOne in filesInput:
    outputFileNameDiff = fileOne[0:3]
    outputPercentageFilenameBase = outputPercentageFilenameBase + '-'+ outputFileNameDiff
    PubmedFile= dirMain+fileOne
    with open(PubmedFile) as fTxtOrg:
        listDocOrg = fTxtOrg.readlines()
    print 'len(listDocOrg): ', len(listDocOrg)
#    exit()
#    with open(dirMain+'output'+fileOne[8:11]+'.csv', 'wb') as outf:
    with open(dirMain+'output-'+outputFileNameDiff+'.csv', 'wb') as outf:
        for myString in listDocOrg:
            print myString
#            myResult = p.search(myString)
#            if myResult <> None:
#                myData = re.sub('^Title: |^Abstract: ','',myResult.group())
#                outf.write(myData)
            listMyWords.extend(myString.split())
#                documents.append((myData.split(),fileOne[9:11]))
            documents.append((myString.split(),outputFileNameDiff))
random.shuffle(documents)
#print len(documents), myData.split()
print 'len(listMyWords): ', len(listMyWords)
#exit()

all_words = nltk.FreqDist(listMyWords)
print 'len(all_words): ', len(all_words)
#print 'type(all_words): ', type(all_words), len(all_words)
word_features = all_words.keys()[:len(all_words)/10]
print 'word_features: ', len(word_features), type(word_features), word_features
#exit()

def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
#        features['contains(%s)' % word] = (word in document_words)
        features[word] = (word in document_words)
    return features


favorDiagnostic = ['intervention', 'risk', 'therapy', 'disease', 'participants', 'effects', 'subjects', 'patient', 'response', 'outcomes', 'events','outcome', 'findings', 'performance', 'statistically', 'evaluation', 'population']
print '\ndocument_features(favorDiagnostic): ', document_features(favorDiagnostic)


featuresets = [(document_features(d), c) for (d,c) in documents]
sizeTest = len(documents)/10
print '\nlen(documents): ', len(documents), '\nsizeTraining:', len(documents)-sizeTest,'\nsizeTesting: ', sizeTest

train_set, test_set = featuresets[sizeTest:], featuresets[:sizeTest]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print 'nltk.classify.accuracy(classifier, test_set): ', nltk.classify.accuracy(classifier, test_set), '\n'


cpdist = classifier._feature_probdist
print 'classifier.most_informative_features(10):', classifier.most_informative_features(10)

with open(dirMain+outputPercentageFilenameBase+'.csv', 'wb') as outf:
    outcsv = csv.writer(outf)
    for fname, fval in classifier.most_informative_features(len(word_features)):
        def labelprob(l):
            return cpdist[l,fname].prob(fval)
        
        labels = sorted([l for l in classifier._labels if 
                fval in cpdist[l,fname].samples()], 
            key=labelprob)
        if len(labels) == 1:
            continue
        l0 = labels[0]
        l1 = labels[-1]
        if cpdist[l0,fname].prob(fval) == 0:
            ratio = 'INF'
        else:
            ratio = '%8.1f' % (cpdist[l1,fname].prob(fval) / cpdist[l0,fname].prob(fval))
    
        if cpdist[l0,fname].prob(fval) == 0:
            ratio1 = 'INF'
        else:
    #        ratio = '%8.1f' % (cpdist[l1,fname].prob(fval) / cpdist[l0,fname].prob(fval))
            ratio1 = '%8.2f' % (cpdist[l1,fname].prob(fval) / (cpdist[l1,fname].prob(fval)+cpdist[l0,fname].prob(fval)))
    
        if cpdist[l0,fname].prob(fval) == 0:
            ratio2 = 'INF'
        else:
            ratio2 = '%8.2f' % ( cpdist[l0,fname].prob(fval) / (cpdist[l1,fname].prob(fval) + cpdist[l0,fname].prob(fval)))
    
    #    print '%24s = %-14r %6s : %-6s = %s : 1.0' % (fname, fval, l1[:6], l0[:6], ratio)
        print '%24s = %-14r %6s : %-6s = %s : 1.0 : %s : %s' % (fname, fval, l1[:6], l0[:6], ratio, ratio1, ratio2)
#        outf.write(fname, fval, l1[:6], l0[:6], ratio, ratio1, ratio2)
#        outf.write(fname, fval)
        outcsv.writerow((fname, fval, l1[:6], l0[:6], ratio, '1', ratio1, ratio2))
exit()
#0.81
classifier.show_most_informative_features(n=10)
def show_most_informative_features22(self, n=10):
    # Determine the most relevant features, and display them.
    
    cpdist = self._feature_probdist
    print 'Most Informative Features'
    
    for fname, fval in self.most_informative_features(n):
        def labelprob(l):
            return cpdist[l,fname].prob(fval)
        
        labels = sorted([l for l in self._labels if 
                fval in cpdist[l,fname].samples()], 
            key=labelprob)
        if len(labels) == 1:
            continue
        l0 = labels[0]
        l1 = labels[-1]
        if cpdist[l0,fname].prob(fval) == 0:
            ratio = 'INF'
        else:
            ratio = '%8.1f' % (cpdist[l1,fname].prob(fval) / 
                cpdist[l0,fname].prob(fval))
        print '%24s = %-14r %6s : %-6s = %s : 1.0' % (fname, fval, l1[:6], l0[:6], ratio)

show_most_informative_features22(n=10)
exit()
qq = classifier.most_informative_features(10)
print qq
classifier.probdist(test_set)
