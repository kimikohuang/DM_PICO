#!/usr/bin/python
"""
Filename:
    readMedline.py
input
    # Filename: writeConfigObj.py
        config['InputFileLocation'] = "/home/kimiko/Downloads"  
        config['InputFilename'] = "pubmed_result(11).txt"
output
    fileNamePubmedTA = global_DirMain+'pubmed_result_TiAb_org.txt'
    fNameP = global_DirMain+'fNameP.txt'
    filename = 'fName_'+strEachKey
    pubmed_result_TiAb_org.txt
    pubmed_result_TiAb_org.csv
"""

#from lxml import objectify

import os
import sys
import datetime
from multiprocessing import Process
#import mGetDicCorpus
from configobj import ConfigObj
import csv
import logging
#import genMlBigram
import shutil
import nltk


config = ConfigObj('scirev.cfg')

myLevel = int(config['level'])

logging.basicConfig(level=myLevel)

LOG_FILENAME = '/home/kimiko/git/DM_PICO/DM_PICO/src/example.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)

#logging.basicConfig(level='logging.DEBUG')

logging.debug("sys.argv[0]: "+sys.argv[0])

#LEVELS = {'debug': logging.DEBUG,    10
#          'info': logging.INFO,    20
#          'warning': logging.WARNING,
#          'error': logging.ERROR,
#          'critical': logging.CRITICAL}
#logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(level=myLevel)



global_DirMain =''


#def getYearSet(theYear, yearCycle=5, startYear=1941):
def getYearSet(theYear, yearCycle=5, startYear=1941, endYear=datetime.datetime.now().year):
    if theYear < startYear:
        return str(startYear-1)
    elif theYear > endYear:
        return str(endYear+1)
    else:
        try:
            reYearSet = endYear-((endYear-theYear)//yearCycle)*yearCycle
#            reYearSet = ((theYear-startYear)//yearCycle)*yearCycle+startYear
            return str(reYearSet)
        except:
            return False


#radiosurgery
#spine

def fReadMedline():
    global global_DirMain

    config = ConfigObj('scirev.cfg')
    flagSentenceSplitter = int(config['readRIS']['flagSentenceSplitter']) # 1 or 0
    
#    print sys.argv[0]
#    global_DirMain ='DrLiu/'
#    global_DirMain =''
    logging.debug(sys.argv[0])

    InputFileLocation = config['InputFileLocation'] # = "/home/kimiko/Downloads"  
    logging.info('InputFileLocation: '+ InputFileLocation)

    InputFilename = config['InputFilename'] # = "pubmed_result(5).txt"  
    logging.info('InputFilename: '+ InputFilename)

#    PubmedFile   = global_DirMain + 'a2.txt'
    PubmedFile   = InputFileLocation + '/' + InputFilename
    
#    print PubmedFile
    logging.info('PubmedFile: '+ PubmedFile)

    listPICO = ['P','I','O']
    ListNormalMethod = ['stpwRemoved', 'wnl', 'porter', 'lancaster']
    ListHeadings = ['background', '']
    myStopwords = nltk.corpus.stopwords.words('english')

    #listMyType = ['stp-', 'wnl-', 'ptr-']
    #listMyType = ['stp-', 'wnl-']
    listMyType = ['wnl-']
#    listMyType = []
    
    if 'wnl' in ListNormalMethod:
        wnl = nltk.WordNetLemmatizer()
    if 'porter' in ListNormalMethod:
        myPorterStemmer = nltk.PorterStemmer()
    if 'lancaster' in ListNormalMethod:
        myLancasterStemmer = nltk.LancasterStemmer()
    

    with open(PubmedFile) as fTxtOrg:
        listDocOrg = fTxtOrg.readlines()
#    print 'len(listDocOrg): ', len(listDocOrg)
    logging.debug('len(listDocOrg): ' + str(len(listDocOrg)))
    
    

    
#    fileNamePubmedTaCsv = global_DirMain+'pubmed_result_TiAb_org.txt'
#    fNameP = global_DirMain+'fNameP.txt'
    fNameP = global_DirMain+'fNameP.txt'
    logging.debug('fNameP Start: '+ fNameP)
#    myCsvWriterP = csv.writer(open(fNameP, 'wb'), quoting=csv.QUOTE_MINIMAL)

    fNameI = global_DirMain+'fNameI.txt'
    logging.debug('fNameI Start: '+ fNameI)
#    myCsvWriterI = csv.writer(open(fNameI, 'wb'), quoting=csv.QUOTE_MINIMAL)

    fNameO = global_DirMain+'fNameO.txt'
    logging.debug('fNameO Start: '+ fNameP)
#    myCsvWriterO = csv.writer(open(fNameO, 'wb'), quoting=csv.QUOTE_MINIMAL)

    myPunktSentenceTokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    fileNamePubmedTaCsv = global_DirMain+'pubmed_result_TiAb_org.csv'
    fileNamePubmedTaTxt = global_DirMain+'pubmed_result_TiAb_org.txt'

    flagTi = False
    myTI = ''
    flagAb = False
    myAB = ''
    flagHasTi = False
    flagHasAb = False
    strYear = ''
    strOneRecord = ''
    myCsvWriter = csv.writer(open(fileNamePubmedTaCsv, 'wb'), quoting=csv.QUOTE_MINIMAL)
    dicHeading = {}

    
    myFileNamePubmedTaTxt = open(fileNamePubmedTaTxt,"w")

    with open(fNameP, 'w') as myCsvWriterP:
    
        for oneRow in listDocOrg:
            
                        
#            logging.debug('oneRow: ' + oneRow)
            if oneRow[0:4] == "PMID":
                pmid = oneRow[6:-1]
    #            print "PMID:", pmid
                logging.debug("PMID:" + pmid)
            elif oneRow[0:2] == "DP":
                strYear =  oneRow[6:10]
#                print "DP:", strYear
                logging.debug("DP:" + strYear)
            elif oneRow[0:2] == "TI":
                myTI =  oneRow[6:-1]
                flagTi = True
            elif flagTi and oneRow[0:6] == "      ":
                myTI = myTI + ' ' + oneRow[6:-1]
    #            print 'myTiAfter:', myTI
                logging.debug('myTiAfter: ' + myTI)
            elif flagTi:
                flagTi = False
                strOneRecord = myTI
    #            print 'strOneRecord:', strOneRecord
                logging.debug('strOneRecord: ' + strOneRecord)
            elif oneRow[0:2] == "AB":
                myAB =  oneRow[6:-1]
                flagHasAb = True 
                flagAb = True
            elif flagAb and oneRow[0:6] == "      ":
                myAB = myAB + ' ' + oneRow[6:-1]
#                logging.debug('myAbAfter: ' + myAB)
            elif flagAb:
                strOneRecord = strOneRecord + ' ' + myAB
    #            PubmedFileTA.write(strYear + ',' + pmid + ',' + strOneRecord.encode("utf-8") + '\n')
                
    #            myCsvWriter.writerow([strYear, pmid, strOneRecord.encode("utf-8")])
                myCsvWriter.writerow([strOneRecord.encode("utf-8")])
    #            myCsvWriter.writerow(['Spam'] * 5 + ['Baked Beans'])
                flagAb = False
                myTI = ''
                myAB = ''
                
                
                
                
                strAbstract = strOneRecord.encode("utf-8")
                logging.debug('strAbstract: ' + strAbstract)
                
                
                listTokenOfAbsSentence = []
                
                if flagSentenceSplitter:
                    listAbsSentence = myPunktSentenceTokenizer.tokenize(strAbstract)
                    for rowOflistAbsSentence in listAbsSentence:
                        listTokenOfAbsSentence.append(nltk.wordpunct_tokenize(rowOflistAbsSentence.lower()))
                else:
                    listTokenOfAbsSentence.append(nltk.wordpunct_tokenize(strAbstract))
#                        print listTokenOfAbsSentence[0]
#                print 'flagSentenceSplitter: ', flagSentenceSplitter, ', len(listAbsSentence): ', len(listAbsSentence)
                logging.debug('flagSentenceSplitter: ' + str(flagSentenceSplitter))
                logging.debug('len(listAbsSentence): ' + str(len(listAbsSentence)))

                
                if flagSentenceSplitter:
                    listAbsSentence = myPunktSentenceTokenizer.tokenize(strAbstract)
#                    for rowOflistAbsSentence in listAbsSentence:
                    
                for idxOfListTokenOfAbsSentence in range(0,len(listTokenOfAbsSentence)):
                
                    listContent = listTokenOfAbsSentence[idxOfListTokenOfAbsSentence] # copy problem
                    
#                    print 'listContent: ', listContent
                    logging.debug("' '.join(listContent): " + ' '.join(listContent))
                    
                    if 'stp-' in  listMyType:
                        listContent = [w for w in listContent if w.isalpha() and (w.lower() not in myStopwords)]
                        
                    if 'wnl-' in  listMyType:
                        listContent = [wnl.lemmatize(t) for t in listContent]
                        logging.debug("'wnl-' in  listMyType: "+' '.join(listContent))
#                        myFileNamePubmedTaTxt.write(listWriteData.encode("utf-8")+'\n')
#                        myFileNamePubmedTaTxt.write(listContent.encode("utf-8")+'\n')
#                        myFileNamePubmedTaTxt.write(' '.join(listContent).encode("utf-8")+'\n')
                        myFileNamePubmedTaTxt.write(pmid+'\t'+' '.join(listContent).encode("utf-8")+'\n')
                        
                    if len(listContent) < 5 or listContent[1]<>':':
                        continue
                    
                    if listContent[2] == "background" and listContent[3] == ":":
#                        listWriteData = ' '.join(listContent[4:-1])
                        listWriteData = ' '.join(listContent[2:-1])
                    else:
#                        listWriteData = ' '.join(listContent[2:-1])
                        listWriteData = ' '.join(listContent[0:-1])
                        

#                        print 'listContent: ', listContent
                    
                    if listContent[0] not in dicHeading:
                        dicHeading[listContent[0]] = [' '.join(listContent[2:-1])]
                    else:
                        dicHeading[listContent[0]].append(' '.join(listContent[2:-1]))
                        
#                    print 'dicHeading[listContent[0]]: ', dicHeading[listContent[0]]
#                    logging.debug("'wnl-' in  listMyType: "+' '.join(listContent))
                    
                    
                        
                        
        #                print 'listWriteData: ', listWriteData
                    logging.debug("listWriteData: "+listWriteData)
        #            print row[2], row[4]
        #            print listTokens
                    
    #                    if idxOfListTokenOfAbsSentence == len(listTokenOfAbsSentence)-1:
    #                        StrIdxOfListTokenOfAbsSentence = 'e'
    #                    else:
    #                        StrIdxOfListTokenOfAbsSentence = str(idxOfListTokenOfAbsSentence)
                    StrIdxOfListTokenOfAbsSentence = str(idxOfListTokenOfAbsSentence)
                        
#                    print pmid +'_'+ StrIdxOfListTokenOfAbsSentence +' '+ listWriteData.encode("utf-8")+'\n'
#                    myCsvWriterP.write(pmid +'_'+ StrIdxOfListTokenOfAbsSentence +' '+ listWriteData.encode("utf-8")+'\n')
                    myCsvWriterP.write(listWriteData.encode("utf-8")+'\n')
                    
                
                                    
            strOneRecord = ''
            
        for strEachKey in dicHeading.keys():    
            filename = 'fName_'+strEachKey
#            print 'strEachKey: ', strEachKey, ', len(dicHeading[strEachKey]): ', len(dicHeading[strEachKey])
#            exit()
            # Create a file object:
            # in "write" mode
            FILE = open(filename,"w")
            
            # Write all the lines at once:
#            print len(dicHeading[strEachKey])

            FILE.writelines('\n'.join(dicHeading[strEachKey]))
                
            # Alternatively write them one by one:
    #        for name in namelist:
    #            FILE.write(name)
                
            FILE.close()
            
#        for strEachKey in dicHeading.keys():
#            fNameP = 'fName_'+strEachKey
#            with open(fNameP, 'w') as myCsvWriterKey:
##                myCsvWriterKey.write(listWriteData.encode("utf-8")+'\n')
#                myCsvWriterKey.write(dicHeading(strEachKey).encode("utf-8")+'\n')

    myFileNamePubmedTaTxt.close()    
if __name__ == "__main__":
    fReadMedline()