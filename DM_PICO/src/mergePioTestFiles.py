#!/usr/bin/python
'''
Filename:
    mergePioTestFiles.py
Input:
    /Output1/stp-intervention.txt
    /Output1/stp-patient.txt
    /Output1/stp-outcome.txt
Output:
    '(stp-(int|out|pat).csv)'
    '(/Output2/stp-(\d)-Per-(int|out|pat)-(Test|Train)-.txt)'
'''

import sys
import logging
from configobj import ConfigObj
import os
import re
import random
import nltk
import csv
import shutil
import xpermutations # http://code.activestate.com/recipes/190465-generator-for-permutations-combinations-selections/
from crossValidation import k_fold_cross_validation


config = ConfigObj('scirev.cfg')

myLevel = int(config['level'])

logging.basicConfig(level=myLevel)

flagLogToFile = int(config['flagLogToFile']) # 1 or 0

if flagLogToFile:
    LOG_FILENAME = '/home/kimiko/git/DM_PICO/DM_PICO/src/example.log'
    logging.basicConfig(filename=LOG_FILENAME)

logging.info("sys.argv[0]: "+sys.argv[0])


#flagForceRefetchPubmed = int(config['flagForceRefetchPubmed'])
numFold = int(config['numFold'])
logging.info("numFold: "+str(numFold))

if not(numFold): 
    numFold = 3
    logging.debug("numFold: "+str(numFold))

def document_features(document, argListWordFeatures):
#def document_features(document, listWordFeatures):
    document_words = set(document)
    features = {}
#    for word in listWordFeatures:
    for word in argListWordFeatures:
#        features['contains(%s)' % word] = (word in document_words)
        features[word] = (word in document_words)
    return features


def fCreadeCrossValidationFiles(numFold):

    
#    numFold = 10
    
    listMyType = ['stp-', 'wnl-', 'ptr-']
    #typeTextPreprocess = 'stp-'
    typeTextPreprocess = 'wnl-'
    #typeTextPreprocess = 'ptr-'
    
    myRe = '((^Title: |^Abstract: )(.*))'
    p = re.compile(myRe)



#    dirMain = ''
#    dirMain = os.path.expanduser('~')+'/' # '/home/kimiko'
    dirMain = os.path.expanduser('~')+'/' + 'Data/TestDir/' # '/home/kimiko'    
    logging.info("dirMain = os.path.expanduser('~')+'/': " + dirMain)

    dirInput = 'Output1/'
    dirOutputTest = 'Output2_TestingSet/'
    logging.info("dirOutputTest: " + dirOutputTest)
    
    dirOutputMergeFile = 'Output2_Merge/'
    dirOutputTrain = 'Output2_TrainingSet/'
    
    
    #filesInput = ['pure-doc-dx.txt', 'pure-doc-tx.txt']
    #filesInput = ['intervention.txt', 'patient.txt', 'outcome.txt']
    ListInputFilenameTxt = []
#    ListInputFilenameTxt = ['intervention.txt', 'patient.txt', 'outcome.txt']
    ListInputFilenameTxtTmp = os.listdir(dirMain + dirInput)
    for itemOfListInputFilenameTxtTmp in ListInputFilenameTxtTmp:
        statinfo = os.stat(dirMain + dirInput + itemOfListInputFilenameTxtTmp)
        if statinfo.st_size > numFold*1500:
            ListInputFilenameTxt.append(itemOfListInputFilenameTxtTmp)
        else:
            os.remove(dirMain + dirInput + itemOfListInputFilenameTxtTmp)
        
#    ListInputFilenameTxt = os.listdir(dirMain + dirInput)
    
#    print "Unique Combinations of 2 letters from :",ListInputFil?enameTxt
    logging.info("Unique Combinations of 2 letters from: " + ', '.join(ListInputFilenameTxt))
#    exit()
    #for uc in xuniqueCombinations(['l','o','v','e'],2): print ''.join(uc)
    
    
    
    #listFilesInputCombinations = [ [typeTextPreprocess+'intervention.txt', typeTextPreprocess+'patient.txt']
    #                  ,[typeTextPreprocess+'intervention.txt', typeTextPreprocess+'outcome.txt']
    #                  ,[typeTextPreprocess+'patient.txt', typeTextPreprocess+'outcome.txt']
    #                  ]
    #filesInput = [typeTextPreprocess+'intervention.txt', typeTextPreprocess+'patient.txt']
    #filesInput = [typeTextPreprocess+'intervention.txt', typeTextPreprocess+'outcome.txt']
    #filesInput = [typeTextPreprocess+'patient.txt', typeTextPreprocess+'outcome.txt']
    
    
    
    #for typeTextPreprocess in listMyType:
#    dirMain = os.getcwd()+'/'
    logging.info("dirMain + dirOutputTest: " + dirMain + dirOutputTest)
    if os.path.isdir(dirMain + dirOutputTest):
        try:
            shutil.rmtree(dirMain+dirOutputTest)
#            os.mkdir(dirMain + dirOutputTest)
        except:
            raise
    os.mkdir(dirMain + dirOutputTest)
    
    logging.info("dirMain + dirOutputMergeFile: " + dirMain + dirOutputMergeFile)
    if os.path.isdir(dirMain + dirOutputMergeFile):
        try:
            shutil.rmtree(dirMain+dirOutputMergeFile)
        except:
            raise
    os.mkdir(dirMain + dirOutputMergeFile)
    
    logging.info("dirMain + dirOutputTrain: " + dirMain + dirOutputTrain)
    if os.path.isdir(dirMain + dirOutputTrain):
        try:
            shutil.rmtree(dirMain+dirOutputTrain)
        except:
            raise
    os.mkdir(dirMain + dirOutputTrain)
#    exit()
    
    for fileOne in ListInputFilenameTxt:
#        outputFileNameDiff = fileOne[0:3]
        outputFileNameDiff = fileOne[0:-4]
#        print 'outputFileNameDiff: ', outputFileNameDiff
        logging.info('outputFileNameDiff: '+ outputFileNameDiff)
    
        listMyWords = []
        listDoc = []
        
        logging.info(dirMain+dirOutputTest+typeTextPreprocess+outputFileNameDiff+'.csv')
        with open(dirMain+dirOutputTest+typeTextPreprocess+outputFileNameDiff+'.csv', 'wb') as outf:
#            filePioTxt= dirMain+dirInput+typeTextPreprocess+fileOne
            filePioTxt= dirMain+dirInput + fileOne
            with open(filePioTxt) as fTxtOrg:
                listDocOrg = fTxtOrg.readlines()
#            print 'len(listDocOrg): ', len(listDocOrg)
            logging.info('len(listDocOrg): '+ str(len(listDocOrg)))
    
            for rowOfListDocOrg in listDocOrg:
        #                print 'rowOfListDocOrg: ', rowOfListDocOrg
        #            myResult = p.search(rowOfListDocOrg)
        #            if myResult <> None:
        #                myData = re.sub('^Title: |^Abstract: ','',myResult.group())
        #                outf.write(myData)
                outf.write(rowOfListDocOrg)
                listMyWords.extend(rowOfListDocOrg.split())
        #                listDoc.append((myData.split(),fileOne[9:11]))
#                print '(rowOfListDocOrg.split(),outputFileNameDiff): ', (outputFileNameDiff, rowOfListDocOrg.split())
                logging.debug('(rowOfListDocOrg.split(),outputFileNameDiff): '+ outputFileNameDiff + " - "+ str(rowOfListDocOrg.split()))
                listDoc.append((rowOfListDocOrg.split(),outputFileNameDiff))
#            exit()
        idxCrossValidation = 0
        # def k_fold_cross_validation(X, K, randomise = False):
#        for listTrainWithDiff, listValidationWithDiff in k_fold_cross_validation(listDoc, numFold, randomize = True):
        for listTrainWithDiff, listValidationWithDiff in k_fold_cross_validation(listDoc, numFold, True):
    #        outputPercentageFilenameBase = typeTextPreprocess+str(idxCrossValidation)+'-Per'
            outputPercentageFilenameBase = typeTextPreprocess+str(idxCrossValidation)
            with open(dirMain+dirOutputMergeFile+typeTextPreprocess+'-'+str(idxCrossValidation)+'-Train-'+'.csv', 'a') as outfFullTrain:
                with open(dirMain+dirOutputMergeFile+typeTextPreprocess+'-'+str(idxCrossValidation)+'-Test-'+'.csv', 'a') as outfFullTest:
            
                    with open(dirMain+dirOutputTrain+outputPercentageFilenameBase+'-'+outputFileNameDiff+'-Train-'+'.csv', 'wb') as outf2:
                        for oneRowOfListTrainWithDiff in listTrainWithDiff:
            #                listAllDocWords.extend(oneRowOfListTrainWithDiff[0])
                            outf2.write(' '.join(oneRowOfListTrainWithDiff[0])+'\n')
                            outfFullTrain.write(' '.join(oneRowOfListTrainWithDiff[0])+'\n')
            
                    with open(dirMain+dirOutputTest+outputPercentageFilenameBase+'-'+outputFileNameDiff+'-Test-'+'.csv', 'wb') as outf3:
                        for oneRowOflistValidationWithDiff in listValidationWithDiff:
#                            print 'oneRowOflistValidationWithDiff: ', oneRowOflistValidationWithDiff
#                            print 'type(oneRowOflistValidationWithDiff): ', type(oneRowOflistValidationWithDiff)
#                            exit()
                            logging.debug('oneRowOflistValidationWithDiff: ' + str(oneRowOflistValidationWithDiff))
                            outf3.write(' '.join(oneRowOflistValidationWithDiff[0])+'\n')
                            outfFullTest.write(' '.join(oneRowOflistValidationWithDiff[0])+'\n')
            
                    idxCrossValidation = idxCrossValidation + 1 

if __name__ == "__main__":
    fCreadeCrossValidationFiles(numFold)