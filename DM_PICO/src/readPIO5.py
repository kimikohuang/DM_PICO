#!/usr/bin/python
'''
Input:
    'intervention.txt'
    , 'patient.txt'
    , 'outcome.txt'
Output:
    typeTextPreprocess+'Percentage' + '-'+ filesInput[4:7]
    Output3_Divide2
'''
import os
import re
import random
import nltk
import csv
import shutil
import xpermutations # http://code.activestate.com/recipes/190465-generator-for-permutations-combinations-selections/


def document_features(document, argWord_features):
    document_words = set(document)
    features = {}
    for word in argWord_features:
#        features['contains(%s)' % word] = (word in document_words)
        features[word] = (word in document_words)
    return features


def fNaiveBayesTraining():
    
    numFold = 10
    
    wordFeatureDivideNumStart = 10 # default = 3
    wordFeatureDivideNumStop = 5 # default =10 not include
    wordFeatureDivideNumStep = -2 # default =10
    
#    listMyType = ['stp-', 'wnl-', 'ptr-']
    #typeTextPreprocess = ''
    #typeTextPreprocess = 'stp-'
    typeTextPreprocess = 'wnl-'
    #typeTextPreprocess = 'ptr-'
    
    
    myRe = '((^Title: |^Abstract: )(.*))'
    p = re.compile(myRe)
    
    #filesInput = ['pure-doc-dx.txt', 'pure-doc-tx.txt']
    #filesInput = ['intervention.txt', 'patient.txt', 'outcome.txt']
    
    #for uc in xuniqueCombinations(['l','o','v','e'],2): print ''.join(uc)
    
    
    
    #listFilesInputCombinations = [ [typeTextPreprocess+'intervention.txt', typeTextPreprocess+'patient.txt']
    #                  ,[typeTextPreprocess+'intervention.txt', typeTextPreprocess+'outcome.txt']
    #                  ,[typeTextPreprocess+'patient.txt', typeTextPreprocess+'outcome.txt']
    #                  ]
    #filesInput = [typeTextPreprocess+'intervention.txt', typeTextPreprocess+'patient.txt']
    #filesInput = [typeTextPreprocess+'intervention.txt', typeTextPreprocess+'outcome.txt']
    #filesInput = [typeTextPreprocess+'patient.txt', typeTextPreprocess+'outcome.txt']
    
    
    dirMain = ''
    dirInput = 'Output2_TrainingSet/'
    #dirInput = 'Output2Train/'
    
    
    for wordFeatureDivideNum in range(wordFeatureDivideNumStart,wordFeatureDivideNumStop, wordFeatureDivideNumStep):
    #    print 'wordFeatureDivideNum: ', wordFeatureDivideNum
        
        dirOutput = 'Output3_Divide'+str(wordFeatureDivideNum)+'/'
        
        #for typeTextPreprocess in listMyType:
        dirCwd = os.getcwd()+'/'
        if os.path.isdir(dirCwd+dirOutput):
            try:
        #            shutil.rmtree(LDASubDataDir, ignore_errors, onerror)
                shutil.rmtree(dirCwd+dirOutput)
            except:
                raise
        os.mkdir(dirCwd+dirOutput)
        
        
        for idxCrossValidation in range(0,numFold):
            print idxCrossValidation
            
        #    listFilesInput = ['stp-'+str(idxCrossValidation)+'-Per-int-Test-.txt', 'stp-'+str(idxCrossValidation)+'-Per-out-Test-.txt', 'stp-'+str(idxCrossValidation)+'-Per-pat-Test-.txt']
#            listFilesInput = [typeTextPreprocess+str(idxCrossValidation)+'-int-Test-.csv', typeTextPreprocess+str(idxCrossValidation)+'-out-Test-.csv', typeTextPreprocess+str(idxCrossValidation)+'-pat-Test-.csv']
            listFilesInput = [typeTextPreprocess+str(idxCrossValidation)+'-int-Train-.csv', typeTextPreprocess+str(idxCrossValidation)+'-out-Train-.csv', typeTextPreprocess+str(idxCrossValidation)+'-pat-Train-.csv']
        
        #exit()
            
        #    listFilesInput = ['stp-0-Per-int-Test-.txt', 'stp-0-Per-out-Test-.txt', 'stp-0-Per-pat-Test-.txt']
            print "Unique Combinations of 2 letters from :",listFilesInput
            for fileOne in listFilesInput:
        #        outputFileNameDiff = fileOne[10:13]
                outputFileNameDiff = fileOne[6:9]
                
                print 'outputFileNameDiff: ', outputFileNameDiff
            
                listMyWords = []
                listDoc = []
        
        #         example from CrossValidationStep2
        #         outputPercentageFilenameBase = typeTextPreprocess+str(idxCrossValidation)+'-Per'
        
        #         filePioTxt= dirCwd+dirInput+typeTextPreprocess+fileOne
                filePioTxt= dirCwd+dirInput+fileOne
                with open(filePioTxt) as fTxtOrg:
                    listDocOrg = fTxtOrg.readlines()
                print 'len(listDocOrg): ', len(listDocOrg)
        
                for rowOfListDocOrg in listDocOrg:
            #                print 'rowOfListDocOrg: ', rowOfListDocOrg
            #            myResult = p.search(rowOfListDocOrg)
            #            if myResult <> None:
            #                myData = re.sub('^Title: |^Abstract: ','',myResult.group())
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
                listDoc = []
                listMyWords = []
                
                outputPercentageFilenameBase = 'Per'
                
                for fileOne in filesInput:
                    outputFileNameDiff = fileOne[6:9]
                    print 'outputFileNameDiff: ', outputFileNameDiff
                    
            #        outputFileNameDiff = fileOne[0:3]
            #        print 'outputFileNameDiff: ', outputFileNameDiff
                #    exit()
                    outputPercentageFilenameBase = outputPercentageFilenameBase + '-'+ outputFileNameDiff
        #            filePioTxt= dirMain+dirInput+typeTextPreprocess+fileOne
                    filePioTxt= dirMain+dirInput+fileOne
                    with open(filePioTxt) as fTxtOrg:
                        listDocOrg = fTxtOrg.readlines()
                    print 'len(listDocOrg): ', len(listDocOrg)
                #    exit()
                #    with open(dirMain+'output'+typeTextPreprocess+fileOne[8:11]+'.csv', 'wb') as outf:
                #    with open(dirMain+typeTextPreprocess+'output-'+outputFileNameDiff+'.csv', 'wb') as outf:
            
            
                    
            
                    for rowOfListDocOrg in listDocOrg:
        #                print 'rowOfListDocOrg: ', rowOfListDocOrg
            #            myResult = p.search(rowOfListDocOrg)
            #            if myResult <> None:
            #                myData = re.sub('^Title: |^Abstract: ','',myResult.group())
                        listMyWords.extend(rowOfListDocOrg.split())
            #                listDoc.append((myData.split(),fileOne[9:11]))
                        print '(rowOfListDocOrg.split(),outputFileNameDiff): ', (outputFileNameDiff, rowOfListDocOrg.split())
                        listDoc.append((rowOfListDocOrg.split(),outputFileNameDiff))
                print 'type(listDoc): ', type(listDoc)
                print 'listDoc[0]: ', listDoc[0]
                print 'listDoc[1]: ', listDoc[1]
                
                random.shuffle(listDoc)
                #print len(listDoc), myData.split()
                print 'len(listMyWords): ', len(listMyWords)
            #    exit()
                
                all_words = nltk.FreqDist(listMyWords)
                print 'len(all_words): ', len(all_words)
                #print 'type(all_words): ', type(all_words), len(all_words)
        #        word_features = all_words.keys()[:len(all_words)/10]
                word_features = all_words.keys()[:len(all_words)/wordFeatureDivideNum]
                print 'word_features: ', len(word_features), type(word_features), word_features
                #exit()
                
                
                
            #    favorDiagnostic = ['intervention', 'risk', 'therapy', 'disease', 'participants', 'effects', 'subjects', 'patient', 'response', 'outcomes', 'events','outcome', 'findings', 'performance', 'statistically', 'evaluation', 'population']
            #    print '\ndocument_features(favorDiagnostic): ', document_features(favorDiagnostic)
                
                
                featuresets = [(document_features(d, word_features), c) for (d,c) in listDoc]
#                print '\nfeaturesets: ', len(featuresets), featuresets
                # featuresets(1/3):  360 [({'bolus': False, 'magnetic': False, 'colonoscopy': False ... }, 'int')
                # featuresets(1/2):  360 [({'bolus': False, 'ali': False, 'caused': False, 'magnetic': False ... }, 'int')
#                exit()
                sizeTest = len(listDoc)/numFold
                print '\nlen(listDoc): ', len(listDoc), '\nsizeTraining:', len(listDoc)-sizeTest,'\nsizeTesting: ', sizeTest
                
                train_set, test_set = featuresets[sizeTest:], featuresets[:sizeTest]
                classifier = nltk.NaiveBayesClassifier.train(train_set)
                print 'nltk.classify.accuracy(classifier, test_set): ', nltk.classify.accuracy(classifier, test_set), '\n'
                
                
                cpdist = classifier._feature_probdist
                print 'classifier.most_informative_features(10):', classifier.most_informative_features(10)
                
        #        print dirMain+dirOutput+str(idxCrossValidation)+outputPercentageFilenameBase+'.csv'
        #        exit()
                with open(dirMain+dirOutput+typeTextPreprocess+str(idxCrossValidation)+'-'+outputPercentageFilenameBase+'.csv', 'wb') as outf:
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

if __name__ == "__main__":
    fNaiveBayesTraining()