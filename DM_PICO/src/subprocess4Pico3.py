#!/usr/bin/python
'''
subprocess4Pico.py
Input:
    './labelNaiveBayes/(wnl|stp)-(\d)-(int|out|pat)-(Test|Train)-.csv'
Output:
    './Output3_Divide0.31/(wnl|stp)-(\d)-Per-(int|out|pat)-(Nin|Nou|Npa|int|out|pat).csv'
    typeTextPreprocess+'Percentage' + '-'+ filesInput[4:7]
    Output3_Divide2
    test git branch
'''

#import writeConfigObj

#writeConfigObj.fwriteConfigObj()

import logging
from configobj import ConfigObj
import os
import re
import nltk
import csv
import shutil
import xpermutations # http://code.activestate.com/recipes/190465-generator-for-permutations-combinations-selections/
from multiprocessing import Process
import collections
import sys

config = ConfigObj('scirev.cfg')

#level = int(config['level'])
myLevel = int(config['level'])

logging.basicConfig(level=myLevel)

logging.info("sys.argv[0]: "+sys.argv[0])

config = ConfigObj('scirev.cfg')

#flagForceRefetchPubmed = int(config['flagForceRefetchPubmed'])
numFold = int(config['numFold'])
if not(numFold): 
    logging.error("can't find numFold. Please run writeConfigObj frist! ")
else:
    logging.debug("numFold: "+str(numFold))
    
flagComplements = int(config['flagComplements'])
logging.info("flagComplements = " + str(flagComplements))

wordFeatureRatioStart10times = int(config['wordFeatureRatioStart10times'])
wordFeatureRatioStop10times = int(config['wordFeatureRatioStop10times'])
wordFeatureRatioStep10times = int(config['wordFeatureRatioStep10times'])

#flagComplements = True
#flagComplements = False

#wordFeatureRatioStart10times = 21 # default = 3
#wordFeatureRatioStop10times = 27 # default =10 not include
#wordFeatureRatioStep10times = 5 # default =10


#dirMain = ''
#dirMain = os.path.expanduser('~')+'/' # '/home/kimiko'
dirMain = os.path.expanduser('~')+'/' + 'Data/TestDir/' # '/home/kimiko'

dirInputTrainingSet = 'Output2_TrainingSet/'
dirInputTestingSet = 'Output2_TestingSet/'
dirOutput_accuracy = 'Output3_accuracy/'
#dirInputTrainingSet = 'Output2Train/'

#dirMain = os.getcwd()+'/'

#listFilesInputFilenameStem = ['int', 'out', 'pat']
dirInput = 'Output1/'
listFilesInputFilenameStem = []
#    ListInputFilenameTxt = ['intervention.txt', 'patient.txt', 'outcome.txt']

#listFilesInputFilenameStem = ['int', 'out']

#    listMyType = ['stp-', 'wnl-', 'ptr-']
#typeTextPreprocess = ''
#typeTextPreprocess = 'stp-'
#typeTextPreprocess = 'wnl-'
#typeTextPreprocess = 'ptr-'
typeTextPreprocess = config['typeTextPreprocess']

global_list_Word_features = []
global_ratioWordFeature = 0.0
global_dirOutput = ''
global_listDocTrain = []
global_listFilesInputPair = []




def document_features(document):
    document_words = set(document)
#    document_words = document
    features = {}
    for word in global_list_Word_features:
#        features['contains(%s)' % word] = (word in document_words)
        features[word] = (word in document_words)
#    print global_list_Word_features
#    print features
    return features


def document_features_index(document):
    document_words = set(document)
    features = {}
#    for word in global_list_Word_features:
    for idxArgWordFeatures in range(len(global_list_Word_features)):
#        features['contains(%s)' % word] = (word in document_words)
#        features[word] = (word in document_words)
#        features[idxArgWordFeatures] = (global_list_Word_features[idxArgWordFeatures] in document_words)
        features[global_list_Word_features[idxArgWordFeatures]] = (global_list_Word_features[idxArgWordFeatures] in document_words)
#        print 'idxArgWordFeatures: ', idxArgWordFeatures, 'global_list_Word_features[idxArgWordFeatures]:', global_list_Word_features[idxArgWordFeatures], 'features[global_list_Word_features[idxArgWordFeatures]]: ', features[global_list_Word_features[idxArgWordFeatures]]
    return features


#def fSubprocess(fileNamePubmedTA, PubmedFile, flagNeedAbstract):
def fSubprocess(idxCrossValidation):
    global global_listDocTrain
    global global_list_Word_features
    global global_listFilesInputPair
    global global_dirOutput
    global global_ratioWordFeature
#for idxCrossValidation in range(0,numFold):
#            print idxCrossValidation
    
#            listFilesInputFilenameStem = [typeTextPreprocess+str(idxCrossValidation)+'-int-Train-.csv', typeTextPreprocess+str(idxCrossValidation)+'-out-Train-.csv', typeTextPreprocess+str(idxCrossValidation)+'-pat-Train-.csv']
#            listFilesInputFilenameStem = [typeTextPreprocess+str(idxCrossValidation)+'-int', typeTextPreprocess+str(idxCrossValidation)+'-out', typeTextPreprocess+str(idxCrossValidation)+'-pat']
#            listFilesInputFilenameStem = [str(idxCrossValidation)+'-int', str(idxCrossValidation)+'-out', str(idxCrossValidation)+'-pat']
#    listFilesInputTrain = ['stp-'+str(idxCrossValidation)+'-Per-int-Test-.txt', 'stp-'+str(idxCrossValidation)+'-Per-out-Test-.txt', 'stp-'+str(idxCrossValidation)+'-Per-pat-Test-.txt']
#            listFilesInputTest = [typeTextPreprocess+str(idxCrossValidation)+'-int-Test-.csv', typeTextPreprocess+str(idxCrossValidation)+'-out-Test-.csv', typeTextPreprocess+str(idxCrossValidation)+'-pat-Test-.csv']
#            listFilesInputTrain = [typeTextPreprocess+str(idxCrossValidation)+'-int-Train-.csv', typeTextPreprocess+str(idxCrossValidation)+'-out-Train-.csv', typeTextPreprocess+str(idxCrossValidation)+'-pat-Train-.csv']

#exit()
    
#    listFilesInputTrain = ['stp-0-Per-int-Test-.txt', 'stp-0-Per-out-Test-.txt', 'stp-0-Per-pat-Test-.txt']
#            print "Unique Combinations of 2 letters from :",listFilesInputTrain
    
    global_listDocTrain = []
    listDocTest = []
    listDocTestPmid = []
    
    listMyWordsTrain = []
    listMyWordsTest = []

#    outputPercentageFilenameMiddle = 'Per'
    outputPercentageFilenameMiddle = ''
    
#    print 'global_listFilesInputPair: ', global_listFilesInputPair
    logging.info(['global_listFilesInputPair: ', global_listFilesInputPair])
    # global_listFilesInputPair:  [['pat'], ['int', 'out']]
#    exit()
    outputFileNameDiff = global_listFilesInputPair[0][0][0:3]
    logging.info("outputFileNameDiff = " + outputFileNameDiff)
    for listFilePair0 in global_listFilesInputPair:
#        outputFileNameDiff = listFilePair0[0][0:3]
#        outputFileNameDiff = ''
#        labelNaiveBayes = outputFileNameDiff
        if len(listFilePair0) == 1:
            labelNaiveBayes = listFilePair0[0][0:3]
            labelPos = labelNaiveBayes
        else:
            labelNaiveBayes = 'N'+outputFileNameDiff[0:2]
            logging.debug('labelNaiveBayes: ' + labelNaiveBayes) 
            labelNeg = labelNaiveBayes

#        outputPercentageFilenameMiddle = outputPercentageFilenameMiddle + '-'+ labelNaiveBayes
        outputPercentageFilenameMiddle = outputPercentageFilenameMiddle + '-'+ labelNaiveBayes
        logging.info('outputPercentageFilenameMiddle = ' + outputPercentageFilenameMiddle)
        for fileOne in listFilePair0:
                
#            fileOne = listFilePair0[0]
#            outputFileNameDiff = outputFileNameDiff+fileOne[0:3]
#            outputFileNameDiff = fileOne[0:3]
#            print 'fileOne: ', fileOne, 'outputFileNameDiff: ', outputFileNameDiff
    #        exit()
    
    #        outputFileNameDiff = fileOne[0:3]
    #        print 'outputFileNameDiff: ', outputFileNameDiff
        #    exit()
#            outputPercentageFilenameMiddle = outputPercentageFilenameMiddle + '-'+ outputFileNameDiff
    #            fileOneTrain= dirMain+dirInputTrainingSet+typeTextPreprocess+fileOne
    #                    fileOneTrain= dirMain+dirInputTrainingSet+fileOne+'-Train-.csv'
    
            fileOneTrain= dirMain+dirInputTrainingSet+typeTextPreprocess+str(idxCrossValidation)+'-'+fileOne+'-Train-.csv'
            with open(fileOneTrain) as fTxtOrgTrain:
                listDocOrgTrain = fTxtOrgTrain.readlines()
#                print 'len(listDocOrgTrain): ', len(listDocOrgTrain), listDocOrgTrain
                logging.debug('len(listDocOrgTrain): ' + str(len(listDocOrgTrain)) + ', listDocOrgTrain: ' + " ".join(listDocOrgTrain))


            logging.debug('fileOneTest = ' + dirMain+dirInputTestingSet+typeTextPreprocess+str(idxCrossValidation)+'-'+fileOne+'-Test-.csv')
            fileOneTest= dirMain+dirInputTestingSet+typeTextPreprocess+str(idxCrossValidation)+'-'+fileOne+'-Test-.csv'
            with open(fileOneTest) as fTxtOrgTest:
                listDocOrgTest = fTxtOrgTest.readlines()
    #                    print 'len(listDocOrgText): ', len(listDocOrgTrain), listDocOrgTrain
            
#            print 'fileOneTrain: ', fileOneTrain, 'fileOneTest: ', fileOneTest
            
    
            for rowOfListDocOrgTrain in listDocOrgTrain:
    #                print 'rowOfListDocOrgTrain: ', rowOfListDocOrgTrain
    #            myResult = p.search(rowOfListDocOrgTrain)
    #            if myResult <> None:
    #                myData = re.sub('^Title: |^Abstract: ','',myResult.group())
                listMyWordsTrain.extend(rowOfListDocOrgTrain.split()[1:-1])
    #                global_listDocTrain.append((myData.split(),fileOne[9:11]))
    #                        print '(rowOfListDocOrgTrain.split(),outputFileNameDiff): ', (outputFileNameDiff, rowOfListDocOrgTrain.split())
#                labelNaiveBayes = outputFileNameDiff
                global_listDocTrain.append((rowOfListDocOrgTrain.split()[1:-1], labelNaiveBayes))
    #               (for fileOne in global_listFilesInputPair:) END
    
            for rowOfListDocOrgTest in listDocOrgTest:
                listMyWordsTest.extend(rowOfListDocOrgTest.split()[1:-1])
#                listDocTest.append((rowOfListDocOrgTest.split(), outputFileNameDiff))
                listDocTest.append((rowOfListDocOrgTest.split()[1:-1], labelNaiveBayes))
                listDocTestPmid.append((rowOfListDocOrgTest.split()[0], labelNaiveBayes))


#    print 'type(global_listDocTrain): ', type(global_listDocTrain), 'len(global_listDocTrain): ', len(global_listDocTrain)
#    print 'global_listDocTrain[0]: ', global_listDocTrain[0]
#    print 'global_listDocTrain[1]: ', global_listDocTrain[-1]
#        random.shuffle(global_listDocTrain)
#        print 'len(listMyWordsTrain): ', len(listMyWordsTrain)
#exit()
    # End: for listFilePair0 in global_listFilesInputPair:
    
    allWordsTrain = nltk.FreqDist(listMyWordsTrain)
#                allWordsTest = nltk.FreqDist(listMyWordsTest)
#    print 'type(allWordsTrain): ', type(allWordsTrain), 'len(allWordsTrain): ', len(allWordsTrain)
    logging.debug('type(allWordsTrain): ' + str(type(allWordsTrain)) + 'len(allWordsTrain): ' + str(len(allWordsTrain)))
    
#        global_list_Word_features = allWordsTrain.keys()[:len(allWordsTrain)/10]
    global_list_Word_features = allWordsTrain.keys()[:int(len(allWordsTrain)*global_ratioWordFeature)]
#    print 'allWordsTrain.keys()[-50:-1]: ', allWordsTrain.keys()[0:10], allWordsTrain.keys()[-1332:-1132]
#    print 'allWordsTrain.keys()[-50:-1]: ', allWordsTrain.values()[-1332:-1132]
#    print 'allWordsTrain.keys()[-50:-1]: ', allWordsTrain.hapaxes()
#                word_features_Test = allWordsTrain.keys()[:len(allWordsTest)]
#    print 'global_ratioWordFeature: ', global_ratioWordFeature, 'global_list_Word_features: ', len(global_list_Word_features), type(global_list_Word_features), global_list_Word_features
    logging.debug('global_ratioWordFeature: ' + str(global_ratioWordFeature) + ', global_list_Word_features: ' + str(len(global_list_Word_features)) + str(type(global_list_Word_features)))
    logging.debug(" ".join(global_list_Word_features))
    # global_list_Word_features:  1985 <type 'list'> ['patient', 'group', 'rate', 'day', 'n', 'treatment', 'using', 'outcome', 'week', 'clinical',
#                exit()
    
    
#    favorDiagnostic = ['intervention', 'risk', 'therapy', 'disease', 'participants', 'effects', 'subjects', 'patient', 'response', 'outcomes', 'events','outcome', 'findings', 'performance', 'statistically', 'evaluation', 'population']
    
    featuresetsTrain = [(document_features(d), c) for (d,c) in global_listDocTrain]
    featuresetsTest = [(document_features(d), c) for (d,c) in listDocTest]
    # featuresetsTest[0:3]:  [({'and': False, 'is': False, 'are': True, 'in': True, 'for': False, ')': False, '(': False, 'review': False, '-': False, ',': True, '.': False, 'to': False, 'patient': False, 'wa': False, 'that': False, 'with': False, 'a': False, 'on': False, 'of': False, 'study': False, 'were': False, 'the': True, 'or': False}, 'bac'), ({'and': False, 'is': True, 'are': False, 'in': False, 'for': False, ')': False, '(': False, 'review': False, '-': False, ',': False, '.': False, 'to': True, 'patient': False, 'wa': False, 'that': False, 'with': True, 'a': False, 'on': False, 'of': True, 'study': False, 'were': False, 'the': True, 'or': False}, 'bac'), ({'and': True, 'is': True, 'are': False, 'in': False, 'for': False, ')': False, '(': False, 'review': False, '-': False, ',': True, '.': False, 'to': False, 'patient': False, 'wa': False, 'that': False, 'with': False, 'a': True, 'on': False, 'of': True, 'study': False, 'were': False, 'the': False, 'or': False}, 'bac')]

#    print 'featuresetsTest[0:3]: ',featuresetsTest[0:3]
    logging.debug(["featuresetsTest[0:1] = ", featuresetsTest[0:1]])
#    exit()
#        print document_features_index(d, global_list_Word_features)
#    print '\ndocument_features(favorDiagnostic): ', document_features(favorDiagnostic)
    
#        featuresetsTrain = [(document_features_index(d), c) for (d,c) in global_listDocTrain]
#        print 'sys.getsizeof(featuresetsTrain): ', sys.getsizeof(featuresetsTrain), 'global_ratioWordFeature: ', global_ratioWordFeature
#        print '\nfeaturesets: ', len(featuresetsTrain), featuresetsTrain[0]
#        print '\nfeaturesets: ', len(featuresetsTrain), featuresetsTrain[1]
#        print '\nfeaturesets: ', len(featuresetsTrain), featuresetsTrain[-1]

#        featuresetsTest = [(document_features_index(d), c) for (d,c) in listDocTest]
#        print 'sys.getsizeof(featuresetsTest): ', sys.getsizeof(featuresetsTest), 'global_ratioWordFeature: ', global_ratioWordFeature

#        continue
    # featuresetsTrain(1/3):  360 [({'bolus': False, 'magnetic': False, 'colonoscopy': False ... }, 'int')
    # featuresetsTrain(1/2):  360 [({'bolus': False, 'ali': False, 'caused': False, 'magnetic': False ... }, 'int')
#                exit()
#                sizeTest = len(global_listDocTrain)/numFold
#                print '\nlen(global_listDocTrain): ', len(global_listDocTrain), '\nsizeTraining:', len(global_listDocTrain)-sizeTest,'\nsizeTesting: ', sizeTest
    
#                train_set, test_set = featuresetsTrain[sizeTest:], featuresetsTrain[:sizeTest]
#                classifier = nltk.NaiveBayesClassifier.train(train_set)
    classifier = nltk.NaiveBayesClassifier.train(featuresetsTrain)
#    print 'classifier.labels(): ', classifier.labels(), classifier.labels()[0], classifier.labels()[1] 
#    exit()


#                with open(dirMain+dirOutputMergeFile+typeTextPreprocess+'-'+str(idxCrossValidation)+'-Train-'+'.csv', 'a') as outfFullTrain:
    with open(dirMain+dirOutput_accuracy+typeTextPreprocess+'-accuracy.csv', 'a') as outfAccuracy:
#                    myAccruacyData = 'global_ratioWordFeature,' + str(global_ratioWordFeature) +','+ '-'.join(global_listFilesInputPair) + ',idxCrossValidation,' + str(idxCrossValidation)+',accuracy,' + str(nltk.classify.accuracy(classifier, featuresetsTest)) +'\n'
#        myAccruacyData = str(global_ratioWordFeature) +','+ '-'.join(global_listFilesInputPair) +','+ str(idxCrossValidation) +','+ str(nltk.classify.accuracy(classifier, featuresetsTest)) +'\n'
#        myAccruacyData = str(global_ratioWordFeature) +','+ '-'.join([global_listFilesInputPair[0][0], global_listFilesInputPair[1][0]]) +','+ str(idxCrossValidation) +','+ str(nltk.classify.accuracy(classifier, featuresetsTest)) +'\n'
#        myAccruacyData = str(global_ratioWordFeature) +','+ '-'.join([global_listFilesInputPair[0][0], labelNaiveBayes]) +','+ str(idxCrossValidation) +','+ str(nltk.classify.accuracy(classifier, featuresetsTest)) +'\n'
        myAccruacy = nltk.classify.accuracy(classifier, featuresetsTest)
        myAccruacyData = str(global_ratioWordFeature) +','+ '-'.join([global_listFilesInputPair[0][0], labelNaiveBayes]) +','+ str(idxCrossValidation) +','+ str(myAccruacy) +'\n'

#        print 'myAccruacyData: ', myAccruacyData
        logging.debug('myAccruacyData: ' + myAccruacyData)            
#        logging.info('observed: ' + "type(observed) "+str(type(observed)) + " " + observed + " "  + label + " "  + listDocTestPmid[i][0] + " "  + str(observed == label))            
        

        outfAccuracy.write(myAccruacyData)
#                    exit()
#                    outfAccuracy.write(myAccruacyData)I do
#        print myAccruacyData
    


    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)
#    tmpPmidMain = ''
    flagJumpNextPmid = False
#    flagEverObservedEqualLabel = False
#    idxTrueRec = 0
#    print 'featuresetsTest: ', featuresetsTest

    for i, (feats, label) in enumerate(featuresetsTest):
#        print 'feats: ', feats
#        print 'label: ', label
#        print 'refsets[label]: ', type(refsets[label]), refsets[label]
#        exit()
        observed = classifier.classify(feats)
#        print type(observed), observed # <type 'str'> Npa

#        if True:
#        print ', listDocTestPmid[i][0]: ', listDocTestPmid[i][0], ', listDocTestPmid[i]: ', listDocTestPmid[i], ', len(listDocTestPmid[i][0]): ', len(listDocTestPmid[i][0])
#        exit()
        if len(listDocTestPmid[i][0]) <= 8:
            refsets[label].add(i)
            testsets[observed].add(i)
            logging.debug('observed: ' + observed + " label: "  + label + " "  + listDocTestPmid[i][0] + " "  + str(observed == label))            
            
#            print 'len(listDocTestPmid[i]) == 8:'
#            exit()
            
        else:
#        elif len(listDocTestPmid[i][0]) > 8:
#            print ' elif len(listDocTestPmid[i]) > 8:'
#            exit()

            if flagJumpNextPmid:
                continue
            else:
                print 'aaaaaaaa: ', listDocTestPmid[i][0], type(listDocTestPmid[i][0])
                if observed == label:
                    flagJumpNextPmid = True
                    refsets[label].add(i)
                    testsets[observed].add(i)
                    logging.debug('observed: ' + observed + " label: "  + label + " "  + listDocTestPmid[i][0] + " "  + str(observed == label))
                    continue            
                elif listDocTestPmid[i][0][9] <> 'e':
                    flagJumpNextPmid =False
                    refsets[label].add(i)
                    testsets[observed].add(i)
                    logging.debug('observed: ' + observed + " label: "  + label + " "  + listDocTestPmid[i][0] + " "  + str(observed == label))
                    continue
                else:
                    continue
                
#                
#                refsets[label].add(i)
#                testsets[observed].add(i)
#                logging.info('observed: ' + observed + " label: "  + label + " "  + listDocTestPmid[i][0] + " "  + str(observed == label))            
#                
#                print 'refsets[label].add(i):', refsets[label]
                    
#                flagJumpNextPmid = False                
#            
#            
##                flagEverObservedEqualLabel = True
#                idxTrueRec = i
#            
#            if listDocTestPmid[i][9] == 'e':
#    #                refsets[label].add(i)
#    #                testsets[observed].add(i)
#                refsets[label].add(idxTrueRec)
#                testsets[observed].add(idxTrueRec)
#               
#                flagEverObservedEqualLabel = False
#                idxTrueRec = 0
#            else:
#                continue      
#                
#            if listDocTestPmid[i][0:8] <> tmpPmidMain:
#                flagNewPmid = True
#                tmpPmidMain = listDocTestPmid[i][0:8]
#                flagJumpNextPmid = False 
#            else:
#                flagNewPmid = False
#                if flagJumpNextPmid:
#                    continue
#
#            flagEverObservedEqualLabel =  (observed == label)
#            if flagEverObservedEqualLabel:
#                flagJumpNextPmid = True
#                refsets[label].add(i)
#                testsets[observed].add(i)
#                continue
#            else:
#                flagJumpNextPmid = False
#                
#
#            if not flagJumpNextPmid:                    
#            else flagJumpNextPmid:
#                
#                continue

#        if True:
#        if False:
#        if observed <> label:
#            print 'observed: ', "type(observed)", type(observed), observed, label, listDocTestPmid[i], observed == label
#            logging.info('observed: ' + "type(observed) "+str(type(observed)) + " " + observed + " "  + label + " "  + listDocTestPmid[i][0] + " "  + str(observed == label))            
#            logging.info('observed: ' + observed + " label: "  + label + " "  + listDocTestPmid[i][0] + " "  + str(observed == label))            
#        logging.debug('fNameI Start: '+ fNameI)

#    print 'testsets: ', testsets
#    exit()
#    print 'fPrecisionRecall(classifier, testfeats): ', nltkPrecisionRecallFMeasure2.fPrecisionRecall(classifier, featuresetsTest)
    classifier.labels()[0], classifier.labels()[1] # classifier.labels()[0]:  Npa,  classifier.labels()[1]:  pat
#    print 'classifier.labels()[0]: ', classifier.labels()[0], ' classifier.labels()[1]: ', classifier.labels()[1]
#    exit()
#    print 'labelPos: ', labelPos
#    print 'refsets[labelPos], testsets[labelPos]: ', refsets[labelPos], '\n testsets[labelPos]: ',testsets[labelPos]
    posPrecision = nltk.metrics.precision(refsets[labelPos], testsets[labelPos])
    posRecall = nltk.metrics.recall(refsets[labelPos], testsets[labelPos])
    posFmeasure = nltk.metrics.f_measure(refsets[labelPos], testsets[labelPos])
    negPrecision = nltk.metrics.precision(refsets[labelNeg], testsets[labelNeg])
    negRecall = nltk.metrics.recall(refsets[labelNeg], testsets[labelNeg])
    negFmeasure = nltk.metrics.f_measure(refsets[labelNeg], testsets[labelNeg])
#    
#    print 'pos precision:', nltk.metrics.precision(refsets['pos'], testsets['pos'])
#    print 'pos recall:', nltk.metrics.recall(refsets['pos'], testsets['pos'])
#    print 'pos F-measure:', nltk.metrics.f_measure(refsets['pos'], testsets['pos'])
#    print 'neg precision:', nltk.metrics.precision(refsets['neg'], testsets['neg'])
#    print 'neg recall:', nltk.metrics.recall(refsets['neg'], testsets['neg'])
#    print 'neg F-measure:', nltk.metrics.f_measure(refsets['neg'], testsets['neg'])

    
    with open(dirMain+dirOutput_accuracy+typeTextPreprocess+'-PreRecFmea.csv', 'a') as outfPreRecFmea:
#        myPreRecFmeaData = str(global_ratioWordFeature) +','+ '-'.join([global_listFilesInputPair[0][0], labelNaiveBayes]) +','+ str(idxCrossValidation) +','+ str(nltk.classify.accuracy(classifier, featuresetsTest)) +'\n'
#        myPreRecFmeaData = str(posPrecision) +','+ str(posRecall) +','+ str(posFmeasure) +','+ str(negPrecision) +','+ str(negRecall) +','+ str(negFmeasure) +'\n'
#        myPreRecFmeaData = str(global_ratioWordFeature) +','+ '-'.join([global_listFilesInputPair[0][0], labelNaiveBayes]) +','+ str(idxCrossValidation) +','+str(posPrecision) +','+ str(posRecall) +','+ str(posFmeasure) +','+ str(negPrecision) +','+ str(negRecall) +','+ str(negFmeasure) +'\n'

        myPreRecFmeaData = \
            str(global_ratioWordFeature)\
            +','+ '-'.join([global_listFilesInputPair[0][0], labelNaiveBayes])\
            +','+ str(idxCrossValidation)\
            +', posPrecision'\
            +','+ str(posPrecision)\
            +'\n'\
            +str(global_ratioWordFeature)\
            +','+ '-'.join([global_listFilesInputPair[0][0], labelNaiveBayes])\
            +','+ str(idxCrossValidation)\
            +', posRecall'\
            +','+ str(posRecall)\
            +'\n'\
            +str(global_ratioWordFeature)\
            +','+ '-'.join([global_listFilesInputPair[0][0], labelNaiveBayes])\
            +','+ str(idxCrossValidation)\
            +', posRmeasure'\
            +','+ str(posFmeasure)\
            +'\n'\
            +str(global_ratioWordFeature)\
            +','+ '-'.join([global_listFilesInputPair[0][0], labelNaiveBayes])\
            +','+ str(idxCrossValidation)\
            +', negPrecision'\
            +','+ str(negPrecision)\
            +'\n'\
            +str(global_ratioWordFeature)\
            +','+ '-'.join([global_listFilesInputPair[0][0], labelNaiveBayes])\
            +','+ str(idxCrossValidation)\
            +', negRecall'\
            +','+ str(negRecall)\
            +'\n'\
            +str(global_ratioWordFeature)\
            +','+ '-'.join([global_listFilesInputPair[0][0], labelNaiveBayes])\
            +','+ str(idxCrossValidation)\
            +', negFmeasure'\
            +','+ str(negFmeasure)\
            +'\n'\
            +str(global_ratioWordFeature)\
            +','+ '-'.join([global_listFilesInputPair[0][0], labelNaiveBayes])\
            +','+ str(idxCrossValidation)\
            +', myAccruacy'\
            +','+ str(myAccruacy)\
            +'\n'
 
#        print 'myPreRecFmeaData: \n', myPreRecFmeaData
        logging.debug('myPreRecFmeaData: \n' + myPreRecFmeaData + ' \n')            

        outfPreRecFmea.write(myPreRecFmeaData)
        
    
    
    
    #    print 'pos F-measure:', nltk.metrics.f_measure(refsets['pos'], testsets['pos'])
    cpdist = classifier._feature_probdist
#                print 'classifier.most_informative_features(10):', classifier.most_informative_features(10)
    
#        print dirMain+global_dirOutput+str(idxCrossValidation)+outputPercentageFilenameMiddle+'.csv'
#        exit()
    logging.info('open wb = ' + dirMain+global_dirOutput+typeTextPreprocess+str(idxCrossValidation)+'-'+outputPercentageFilenameMiddle+'.csv')
    with open(dirMain+global_dirOutput+typeTextPreprocess+str(idxCrossValidation)+'-'+outputPercentageFilenameMiddle+'.csv', 'wb') as outf:
        outcsv = csv.writer(outf)
        for fname, fval in classifier.most_informative_features(len(global_list_Word_features)):
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
#                        print '%24s = %-14r %6s : %-6s = %s : 1.0 : %s : %s' % (fname, fval, l1[:6], l0[:6], ratio, ratio1, ratio2)
    #        outf.write(fname, fval, l1[:6], l0[:6], ratio, ratio1, ratio2)
    #        outf.write(fname, fval)
            outcsv.writerow((fname, fval, l1[:6], l0[:6], ratio, '1', ratio1, ratio2))
#                print 'listFilesInputCombinations: ', listFilesInputCombinations

#====================================================================================================    

def fNaiveBayesTraining(numFold=10):
    global global_list_Word_features
    global global_ratioWordFeature
    global global_dirOutput
    global global_listFilesInputPair
    
    
    
    myRe = '((^Title: |^Abstract: )(.*))'
    p = re.compile(myRe)

    listFilesInputFilenameStemTmp = os.listdir(dirMain + dirInput)
    for itemOflistFilesInputFilenameStemTmp in listFilesInputFilenameStemTmp:
        listFilesInputFilenameStem.append(itemOflistFilesInputFilenameStemTmp[0:-4])



    
    #global_listFilesInputPair = ['pure-doc-dx.txt', 'pure-doc-tx.txt']
    #global_listFilesInputPair = ['intervention.txt', 'patient.txt', 'outcome.txt']
    
    #for uc in xuniqueCombinations(['l','o','v','e'],2): print ''.join(uc)
    
    
    
    #listFilesInputCombinations = [ [typeTextPreprocess+'intervention.txt', typeTextPreprocess+'patient.txt']
    #                  ,[typeTextPreprocess+'intervention.txt', typeTextPreprocess+'outcome.txt']
    #                  ,[typeTextPreprocess+'patient.txt', typeTextPreprocess+'outcome.txt']
    #                  ]
    #global_listFilesInputPair = [typeTextPreprocess+'intervention.txt', typeTextPreprocess+'patient.txt']
    #global_listFilesInputPair = [typeTextPreprocess+'intervention.txt', typeTextPreprocess+'outcome.txt']
    #global_listFilesInputPair = [typeTextPreprocess+'patient.txt', typeTextPreprocess+'outcome.txt']
    
    
    
#    dirOutput_accuracy
    logging.info('dirMain+dirOutput_accuracy = ' + dirMain+dirOutput_accuracy)
    if os.path.isdir(dirMain+dirOutput_accuracy):
        try:
        #            shutil.rmtree(LDASubDataDir, ignore_errors, onerror)
            shutil.rmtree(dirMain+dirOutput_accuracy)
        except:
            raise
    os.mkdir(dirMain+dirOutput_accuracy)

    with open(dirMain+dirOutput_accuracy+typeTextPreprocess+'-accuracy.csv', 'a') as outfAccuracy:
        myAccruacyData = 'global_ratioWordFeature,' + 'global_listFilesInputPair,' + 'idxCrossValidation,' + 'accuracy\n'
        outfAccuracy.write(myAccruacyData)

#        print 'myAccruacyData: ', myAccruacyData
        logging.debug('myAccruacyData: ' + myAccruacyData)            
        
    
    with open(dirMain+dirOutput_accuracy+typeTextPreprocess+'-PreRecFmea.csv', 'a') as outfPreRecFmea:
#        myPreRecFmeaData = str(posPrecision) +','+ str(posRecall) +','+ str(posRmeasure) +','+ str(negPrecision) +','+ str(negRecall) +','+ str(negFmeasure) +'\n'
#        myPreRecFmeaData = 'global_ratioWordFeature,' + 'global_listFilesInputPair,' + 'idxCrossValidation,' + 'posPrecision,'+ 'posRecall,'+ 'posRmeasure,'+ 'negPrecision,'+ 'negRecall,'+ 'negFmeasure\n'
        myPreRecFmeaData = 'global_ratioWordFeature,' + 'global_listFilesInputPair,' + 'idxCrossValidation,' + 'testType,'+ 'testValue\n'
        outfPreRecFmea.write(myPreRecFmeaData)

    
#    wordFeatureRatio10times = 0.1
    for wordFeatureRatio10times in range(wordFeatureRatioStart10times,wordFeatureRatioStop10times, wordFeatureRatioStep10times):
#        print 'wordFeatureRatio10times: ', wordFeatureRatio10times
        global_ratioWordFeature = wordFeatureRatio10times/100.0
#        print 'global_ratioWordFeature: ', global_ratioWordFeature
        logging.info('global_ratioWordFeature: ' + str(global_ratioWordFeature))
        
#        continue
        
        global_dirOutput = 'Output3_Divide'+str(global_ratioWordFeature)+'/'
        
        #for typeTextPreprocess in listMyType:
        if os.path.isdir(dirMain+global_dirOutput):
            try:
        #            shutil.rmtree(LDASubDataDir, ignore_errors, onerror)
                shutil.rmtree(dirMain+global_dirOutput)
            except:
                raise
        os.mkdir(dirMain+global_dirOutput)

# ================================================================================================================
        for idxCrossValidation in range(0,numFold):
          
            listFilesInputCombinations = []
        #            for uc in xpermutations.xuniqueCombinations(listFilesInputTrain, 2):
#            for uc in xpermutations.xuniqueCombinations(listFilesInputFilenameStem, 2):
#                listFilesInputCombinations.append(uc)
        #                print type(uc), ' '.join(uc)
        #            exit()


#            flagComplements = False
#            flagComplements = True
            if flagComplements:
                for uc in xpermutations.xuniqueCombinations(listFilesInputFilenameStem, 1):
#                    listFilesInputCombinations.append([uc, list(set(listFilesInputFilenameStem).difference(uc))])
                    listRemoveUc = list(listFilesInputFilenameStem)
                    listRemoveUc.remove(uc[0])
#                    print listRemoveUc
                    
                    logging.debug([uc, listRemoveUc])
                    listFilesInputCombinations.append([uc, listRemoveUc])
                    

#                    listFilesInputCombinations.append([uc, list(listFilesInputFilenameStem).remove('intervention')])
#                    print 'uc: ', type(uc), ' '.join(uc)                    
                    
#                    print 'uc if flagComplements: ', type(uc), ' '.join(uc), ' ','set(listFilesInputFilenameStem).difference(uc): ', set(listFilesInputFilenameStem).difference(uc)
#                    logging.debug(['uc = ', uc, 'set(listFilesInputFilenameStem).difference(uc): ', set(listFilesInputFilenameStem).difference(uc)])
#                print 'listFilesInputCombinations: ', type(listFilesInputCombinations), listFilesInputCombinations
#                logging.debug(['idxCrossValidation = ', str(idxCrossValidation), 'listFilesInputCombinations', listFilesInputCombinations])
            else:
            #            for uc in xpermutations.xuniqueCombinations(listFilesInputTrain, 2):
                for uc in xpermutations.xuniqueCombinations(listFilesInputFilenameStem, 2):
#                    listFilesInputCombinations.append(uc)
                    listFilesInputCombinations.append([[uc[0]], [uc[1]]])
#                    print 'uc if flagComplements else: ', type(uc), uc
                    logging.debug(['uc if flagComplements else: ', type(uc), uc])
                print '\nlistFilesInputCombinations: ', type(listFilesInputCombinations), listFilesInputCombinations
#                exit()
#                for uc in xpermutations.xuniqueCombinations(listFilesInputFilenameStem, 2):
#            exit()            
#            print "listFilesInputCombinations = ", listFilesInputCombinations
#            listFilesInputCombinations = []
            for global_listFilesInputPair in listFilesInputCombinations:    
#                logging.info(['global_listFilesInputPair = ', global_listFilesInputPair])
                p = Process(target=fSubprocess, args=(idxCrossValidation,))
                p.start()
                #dicCorpus = parent_conn.recv()
                #print parent_conn.recv()   # prints "[42, None, 'hello']"
                p.join()
            #    exit()
        #        logging.debug('PubmedFileTA: '+fileNamePubmedTA+' OK!')

if __name__ == "__main__":
    fNaiveBayesTraining(numFold)
