#!/usr/bin/python
'''
Input:
    /Output1/stp-intervention.txt
    /Output1/stp-patient.txt
    /Output1/stp-outcome.txt
Output:
    '(stp-(int|out|pat).csv)'
    '(/Output2/stp-(\d)-Per-(int|out|pat)-(Test|Train)-.txt)'
'''
import os
import re
import random
import nltk
import csv
import shutil
import xpermutations # http://code.activestate.com/recipes/190465-generator-for-permutations-combinations-selections/
from crossValidation import k_fold_cross_validation


def document_features(document, argListWordFeatures):
#def document_features(document, listWordFeatures):
    document_words = set(document)
    features = {}
#    for word in listWordFeatures:
    for word in argListWordFeatures:
#        features['contains(%s)' % word] = (word in document_words)
        features[word] = (word in document_words)
    return features


def fCreadeCrossValidationFiles(numFold=10):
    
#    numFold = 10
    
    listMyType = ['stp-', 'wnl-', 'ptr-']
    #typeTextPreprocess = 'stp-'
    typeTextPreprocess = 'wnl-'
    #typeTextPreprocess = 'ptr-'
    
    myRe = '((^Title: |^Abstract: )(.*))'
    p = re.compile(myRe)
    
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
    dirOutput = 'Output2_TestingSet/'
    dirOutputMergeFile = 'Output2_Merge/'
    dirOutputTrain = 'Output2_TrainingSet/'
    
    
    #for typeTextPreprocess in listMyType:
    dirCwd = os.getcwd()+'/'
    if os.path.isdir(dirCwd+dirOutput):
        try:
    #            shutil.rmtree(LDASubDataDir, ignore_errors, onerror)
            shutil.rmtree(dirCwd+dirOutput)
        except:
            raise
    os.mkdir(dirCwd+dirOutput)
    
    if os.path.isdir(dirCwd+dirOutputMergeFile):
        try:
    #            shutil.rmtree(LDASubDataDir, ignore_errors, onerror)
            shutil.rmtree(dirCwd+dirOutputMergeFile)
        except:
            raise
    os.mkdir(dirCwd+dirOutputMergeFile)
    
    if os.path.isdir(dirCwd+dirOutputTrain):
        try:
    #            shutil.rmtree(LDASubDataDir, ignore_errors, onerror)
            shutil.rmtree(dirCwd+dirOutputTrain)
        except:
            raise
    os.mkdir(dirCwd+dirOutputTrain)
    
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
        idxCrossValidation = 0
        for listTrainWithDiff, listValidationWithDiff in k_fold_cross_validation(listDoc, numFold, randomize = True):
    #        outputPercentageFilenameBase = typeTextPreprocess+str(idxCrossValidation)+'-Per'
            outputPercentageFilenameBase = typeTextPreprocess+str(idxCrossValidation)
            with open(dirMain+dirOutputMergeFile+typeTextPreprocess+'-'+str(idxCrossValidation)+'-Train-'+'.csv', 'a') as outfFullTrain:
                with open(dirMain+dirOutputMergeFile+typeTextPreprocess+'-'+str(idxCrossValidation)+'-Test-'+'.csv', 'a') as outfFullTest:
            
                    with open(dirMain+dirOutputTrain+outputPercentageFilenameBase+'-'+outputFileNameDiff+'-Train-'+'.csv', 'wb') as outf2:
                        for oneRowOfListTrainWithDiff in listTrainWithDiff:
            #                listAllDocWords.extend(oneRowOfListTrainWithDiff[0])
                            outf2.write(' '.join(oneRowOfListTrainWithDiff[0])+'\n')
                            outfFullTrain.write(' '.join(oneRowOfListTrainWithDiff[0])+'\n')
            
                    with open(dirMain+dirOutput+outputPercentageFilenameBase+'-'+outputFileNameDiff+'-Test-'+'.csv', 'wb') as outf3:
                        for oneRowOflistValidationWithDiff in listValidationWithDiff:
                            print 'oneRowOflistValidationWithDiff: ', oneRowOflistValidationWithDiff
                            outf3.write(' '.join(oneRowOflistValidationWithDiff[0])+'\n')
                            outfFullTest.write(' '.join(oneRowOflistValidationWithDiff[0])+'\n')
            
                    idxCrossValidation = idxCrossValidation + 1 

if __name__ == "__main__":
    fCreadeCrossValidationFiles()