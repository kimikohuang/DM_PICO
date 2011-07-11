#!/usr/bin/python
'''
Input:
    'intervention.txt'
    , 'patient.txt'
    , 'outcome.txt'
Output:
    typeTextPreprocess+'Percentage' + '-'+ filesInput[4:7]
'''
import os
import re
import random
import nltk
import csv
import shutil
import xpermutations # http://code.activestate.com/recipes/190465-generator-for-permutations-combinations-selections/
from crossValidation import k_fold_cross_validation


def document_features(document):
    document_words = set(document)
    features = {}
    for word in listWordFeatures:
#        features['contains(%s)' % word] = (word in document_words)
        features[word] = (word in document_words)
    return features

myRe = '((^Title: |^Abstract: )(.*))'
p = re.compile(myRe)

listMyType = ['stp-', 'wnl-', 'ptr-']
typeTextPreprocess = 'stp-'
#typeTextPreprocess = 'wnl-'
#typeTextPreprocess = 'ptr-'

#filesInput = ['pure-doc-dx.txt', 'pure-doc-tx.txt']
#filesInput = ['intervention.txt', 'patient.txt', 'outcome.txt']
listFilesInput = ['intervention.txt', 'patient.txt', 'outcome.txt']
print "Unique Combinations of 2 letters from :",listFilesInput
#for uc in xuniqueCombinations(['l','o','v','e'],2): print ''.join(uc)



#listFilesInputCombinations = [ [typeTextPreprocess+'intervention.txt', typeTextPreprocess+'patient.txt']
#                  ,[typeTextPreprocess+'intervention.txt', typeTextPreprocess+'outcome.txt']
#                  ,[typeTextPreprocess+'patient.txt', typeTextPreprocess+'outcome.txt']
#                  ]
#filesInput = [typeTextPreprocess+'intervention.txt', typeTextPreprocess+'patient.txt']
#filesInput = [typeTextPreprocess+'intervention.txt', typeTextPreprocess+'outcome.txt']
#filesInput = [typeTextPreprocess+'patient.txt', typeTextPreprocess+'outcome.txt']


dirMain = ''
dirInput = 'Output1/'
dirOutput = 'Output2/'

#for typeTextPreprocess in listMyType:
dirCwd = os.getcwd()+'/'
if os.path.isdir(dirCwd+dirOutput):
    try:
#            shutil.rmtree(LDASubDataDir, ignore_errors, onerror)
        shutil.rmtree(dirCwd+dirOutput)
    except:
        raise
os.mkdir(dirCwd+dirOutput)

for fileOne in listFilesInput:
    outputFileNameDiff = fileOne[0:3]
    print 'outputFileNameDiff: ', outputFileNameDiff

    listMyWords = []
    listDoc = []

    with open(dirMain+dirOutput+typeTextPreprocess+outputFileNameDiff+'.csv', 'wb') as outf:
        filePioTxt= dirMain+dirInput+typeTextPreprocess+fileOne
        with open(filePioTxt) as fTxtOrg:
            listDocOrg = fTxtOrg.readlines()
        print 'len(listDocOrg): ', len(listDocOrg)

        for rowOfListDocOrg in listDocOrg:
    #                print 'rowOfListDocOrg: ', rowOfListDocOrg
    #            myResult = p.search(rowOfListDocOrg)
    #            if myResult <> None:
    #                myData = re.sub('^Title: |^Abstract: ','',myResult.group())
    #                outf.write(myData)
            outf.write(rowOfListDocOrg)
            listMyWords.extend(rowOfListDocOrg.split())
    #                listDoc.append((myData.split(),fileOne[9:11]))
            print '(rowOfListDocOrg.split(),outputFileNameDiff): ', (outputFileNameDiff, rowOfListDocOrg.split())
            listDoc.append((rowOfListDocOrg.split(),outputFileNameDiff))

#exit()

listFilesInputCombinations = []
for uc in xpermutations.xuniqueCombinations(listFilesInput,2):
    listFilesInputCombinations.append(uc)
#    print ' '.join(uc)
print 'listFilesInputCombinations: ', listFilesInputCombinations
#exit()

for filesInput in listFilesInputCombinations:    
    listDocOf2files = []
    listMyWordsOf2files = []
    
    outputPercentageFilenameBase = typeTextPreprocess+'Percentage'
    
    for fileOne in filesInput:
        outputFileNameDiff = fileOne[0:3]
        print 'outputFileNameDiff: ', outputFileNameDiff
    #    exit()
        outputPercentageFilenameBase = outputPercentageFilenameBase + '-'+ outputFileNameDiff
        filePioTxt= dirMain+dirInput+typeTextPreprocess+fileOne
        with open(filePioTxt) as fTxtOrg:
            listDocOrg = fTxtOrg.readlines()
        print 'len(listDocOrg): ', len(listDocOrg)
    #    exit()
    #    with open(dirMain+'output'+typeTextPreprocess+fileOne[8:11]+'.csv', 'wb') as outf:
    #    with open(dirMain+typeTextPreprocess+'output-'+outputFileNameDiff+'.csv', 'wb') as outf:


        for rowOfListDocOrg in listDocOrg:
            print 'rowOfListDocOrg: ', rowOfListDocOrg
#            myResult = p.search(rowOfListDocOrg)
#            if myResult <> None:
#                myData = re.sub('^Title: |^Abstract: ','',myResult.group())
            listMyWordsOf2files.extend(rowOfListDocOrg.split())
#                listDocOf2files.append((myData.split(),fileOne[9:11]))
            print '(rowOfListDocOrg.split(),outputFileNameDiff): ', (outputFileNameDiff, rowOfListDocOrg.split())
            listDocOf2files.append((rowOfListDocOrg.split(),outputFileNameDiff))
    print 'filesInput: ', filesInput, 'type(listDocOf2files): ', type(listDocOf2files)
    print 'filesInput: ', filesInput, 'listDocOf2files[0]: ', listDocOf2files[0]
    print 'filesInput: ', filesInput, 'listDocOf2files[1]: ', listDocOf2files[-1]
    


    
    numFold = 5
#    qq = k_fold_cross_validation(listDocOf2files, numFold, randomize = True)
    for training, validation in k_fold_cross_validation(listDocOf2files, numFold, randomize = True):
        for item in listDocOf2files:
            assert (item in training) ^ (item in validation)
        print '\ntraining: ', training, '\nvalidation: ', validation



#    print type(qq), qq.training[0]
    exit()

    random.shuffle(listDocOf2files)
    #print len(listDocOf2files), myData.split()
    print 'len(listMyWordsOf2files): ', len(listMyWordsOf2files), 'listMyWordsOf2files: ', listMyWordsOf2files
#    exit()
    
    
    all_words = nltk.FreqDist(listMyWordsOf2files)
    print 'len(all_words): ', len(all_words), type(all_words), 'all_words: ', all_words
    #print 'type(all_words): ', type(all_words), len(all_words)
    listWordFeatures = all_words.keys()[:len(all_words)/10]
    print 'listWordFeatures: ', len(listWordFeatures), type(listWordFeatures), 'listWordFeatures: ', listWordFeatures
#    exit()
    
    favorDiagnostic = listWordFeatures
#    favorDiagnostic = ['intervention', 'risk', 'therapy', 'disease', 'participants', 'effects', 'subjects', 'patient', 'response', 'outcomes', 'events','outcome', 'findings', 'performance', 'statistically', 'evaluation', 'population']
    print '\ndocument_features(favorDiagnostic): ', document_features(favorDiagnostic)
    
#    exit()
    
    sizeTest = len(listDocOf2files)/10
    print '\nlen(listDocOf2files): ', len(listDocOf2files), '\nsizeTraining:', len(listDocOf2files)-sizeTest,'\nsizeTesting: ', sizeTest
    
    featuresets = [(document_features(myDoc), docType) for (myDoc,docType) in listDocOf2files]
    print 'featuresets: ', type(featuresets),  featuresets
    exit()
    
    train_set, test_set = featuresets[sizeTest:], featuresets[:sizeTest]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print 'nltk.classify.accuracy(classifier, test_set): ', nltk.classify.accuracy(classifier, test_set), '\n'
    
    
    cpdist = classifier._feature_probdist
    print 'classifier.most_informative_features(10):', classifier.most_informative_features(10)
    
    with open(dirMain+dirOutput+outputPercentageFilenameBase+'.csv', 'wb') as outf:
        outcsv = csv.writer(outf)
        for fname, fval in classifier.most_informative_features(len(listWordFeatures)):
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
