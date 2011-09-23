#!/usr/bin/python
# Filename: aXml2input.py
"""
input
    ris_format_file.txt
output
    fName(P|I|O).txt
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

logging.basicConfig(level=logging.DEBUG)

def fSubprocess(fileNamePubmedTA, PubmedFile, flagNeedAbstract):

#    PubmedFile   = DirMain + 'pubmed_result.txt'
    #print 'os.path.abspath(PubmedFile): ', os.path.abspath(PubmedFile)
    #print 'os.path.basename(PubmedFile): ', os.path.basename(PubmedFile)
    #print 'os.path.dirname(PubmedFile): ', os.path.dirname(PubmedFile)
    #exit()
#    print 'fileNamePubmedTA: ', fileNamePubmedTA
#    exit()
    
    

#    with open(DirMain+os.path.basename(dfile)[0:4]+'O'+os.path.basename(dfile)[5:-4]+'.Pmid') as fTxtOrg:
    with open(PubmedFile) as fTxtOrg:
#        with open(DirMain+os.path.basename(dfile)[0:4]+'W'+os.path.basename(dfile)[5:-4]+'.txt') as fTxtOrg:
        listDocOrg = fTxtOrg.readlines()
#    print 'len(listDocOrg): ', len(listDocOrg)
    logging.debug('len(listDocOrg): ' + str(len(listDocOrg)))
    
#    with open(fileNamePubmedTA, 'w') as PubmedFileTA:
#        flagTi = False
#        myTI = ''
#        flagAb = False
#        myAB = ''
#        flagHasTi = False
#        flagHasAb = False
#        strYear = ''
#        strOneRecord = ''
#        for oneRow in listDocOrg:
#            print 'oneRow:', oneRow
#            if oneRow[0:4] == "PMID":
#                pmid = oneRow[6:-1]
#                print "PMID:", pmid
#            elif oneRow[0:2] == "DP":
#                strYear =  oneRow[6:10]
#                print "DP:", strYear
#            elif oneRow[0:2] == "TI":
#                myTI =  oneRow[6:-1]
#                flagTi = True
#            elif flagTi and oneRow[0:6] == "      ":
#                myTI = myTI + ' ' + oneRow[6:-1]
#                print 'myTiAfter:', myTI
#            elif flagTi:
#                flagTi = False
#                strOneRecord = myTI
#                print 'strOneRecord:', strOneRecord
#            elif oneRow[0:2] == "AB":
#                myAB =  oneRow[6:-1]
#                flagHasAb = True 
#                flagAb = True
#            elif flagAb and oneRow[0:6] == "      ":
#                myAB = myAB + ' ' + oneRow[6:-1]
#                print 'myAbAfter:', myAB
#            elif flagAb:
#                strOneRecord = strOneRecord + ' ' + myAB
#                PubmedFileTA.write(strYear + ',' + pmid + ',' + strOneRecord.encode("utf-8") + '\n')
#                flagAb = False
#                strOneRecord = ''
#                myTI = ''
#                myAB = ''
#                
#    with open(fileNamePubmedTA, 'w') as PubmedFileTA:
    flagTi = False
    myTI = ''
    flagAb = False
    myAB = ''
    flagHasTi = False
    flagHasAb = False
    strYear = ''
    strOneRecord = ''
    myCsvWriter = csv.writer(open(fileNamePubmedTA, 'wb'), quoting=csv.QUOTE_MINIMAL)
    for oneRow in listDocOrg:
        logging.debug('oneRow: ' + oneRow)
        if oneRow[0:4] == "PMID":
            pmid = oneRow[6:-1]
#            print "PMID:", pmid
            logging.debug("PMID:" + pmid)
        elif oneRow[0:2] == "DP":
            strYear =  oneRow[6:10]
            print "DP:", strYear
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
            logging.debug('myAbAfter: ' + myAB)
        elif flagAb:
            strOneRecord = strOneRecord + ' ' + myAB
#            PubmedFileTA.write(strYear + ',' + pmid + ',' + strOneRecord.encode("utf-8") + '\n')
            
            myCsvWriter.writerow([strYear, pmid, strOneRecord.encode("utf-8")])
#            myCsvWriter.writerow(['Spam'] * 5 + ['Baked Beans'])
            flagAb = False
            strOneRecord = ''
            myTI = ''
            myAB = ''
#            elif (not flagNeedAbstract):
#                PubmedFileTA.write(strYear + ',' + pmid + ',' + strOneRecord.encode("utf-8") + '\n')
#                flagAb = False
#                strOneRecord = ''
#                myTI = ''
#                myAB = ''
                
                

#    fileNamePubmedTA = listDocOrg.replace("\n\s\s\s\s\s\s", "\s")
    

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

def fText2input():   
    
#    print sys.argv[0]
    DirMain ='DrLiu/'
    logging.debug(sys.argv[0])
#    PubmedFile   = DirMain + 'a2.txt'
    PubmedFile   = DirMain + 'a_org.txt'
    print PubmedFile

    listPICO = ['P','I','O']
    ListNormalMethod = ['stpwRemoved', 'wnl', 'porter', 'lancaster']
    
    myStopwords = nltk.corpus.stopwords.words('english')

    #listMyType = ['stp-', 'wnl-', 'ptr-']
    #listMyType = ['stp-', 'wnl-']
    listMyType = ['wnl-']
    
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
    
#    fileNamePubmedTA = DirMain+'pubmed_result_TiAb_org.txt'
#    fNameP = DirMain+'fNameP.txt'
    fNameP = DirMain+'fNameP.txt'
    logging.debug('fNameP Start: '+ fNameP)
    myCsvWriterP = csv.writer(open(fNameP, 'wb'), quoting=csv.QUOTE_MINIMAL)

    fNameI = DirMain+'fNameI.txt'
    logging.debug('fNameI Start: '+ fNameI)
    myCsvWriterI = csv.writer(open(fNameI, 'wb'), quoting=csv.QUOTE_MINIMAL)

    fNameO = DirMain+'fNameO.txt'
    logging.debug('fNameO Start: '+ fNameP)
    myCsvWriterO = csv.writer(open(fNameO, 'wb'), quoting=csv.QUOTE_MINIMAL)

    flagLabel = False
    myTI = ''
    flagAb = False
    myAB = ''
    flagHasTi = False
    flagHasAb = False
    strYear = ''
    strOneRecord = ''
    
    with open(fNameP, 'w') as myCsvWriterP:
        with open(fNameI, 'w') as myCsvWriterI:
            with open(fNameO, 'w') as myCsvWriterO:
        
                for oneRow in listDocOrg:
            #        logging.debug('oneRow: ' + oneRow)
            #        if oneRow[0:4] == "Accession Number:":
                    if oneRow[0:18] == "Accession Number: ":
                        flagHasAb = False
                        pmid = oneRow[18:-2]
            #            print "PMID:", pmid
                        logging.debug("PMID: " + pmid)
                        strOneRecord = pmid                        
                        continue
                    elif oneRow[0:10] == "Abstract: ":
                        flagHasAb = True
                        strAbstract =  oneRow[10:-1]
            #            print "DP:", strYear
                        logging.debug("Abstract: " + strAbstract)
                        strOneRecord = pmid + ' ' + strAbstract
#                        strOneRecord = pmid + strAbstract
                        logging.debug("strOneRecord: " + strOneRecord)
            
                        continue
                    elif flagHasAb and oneRow[0:7] == "Label: ":
                        myLabel =  oneRow[7:-1]
                        if myLabel.find('/') > -1:
                            print 'myLabel.find("/") > -1:', myLabel.find("/")
                            myLabel = myLabel[0:myLabel.find('/')-1]
                        
            #            print "DP:", strYear
                        logging.debug("myLabel: " + myLabel)
                        
#                        myTmpData = ' '.join([row[0].lower(),row[4].lower()])
                        myTmpData = strOneRecord
                        listTokens = nltk.wordpunct_tokenize(myTmpData.lower())
                        
        #                listTokensNotDigital = [w for w in listTokens if (not w.isalpha())]
        #                listTokensStped = [w for w in listTokens if w.isalpha() and (w.lower() not in myStopwords)]
        #                if myType == 'stp-':
        #                    listContent = listTokensStped
        #                elif myType == 'wnl-':
        #                    listContent = [wnl.lemmatize(t) for t in listTokensStped]
        #                elif myType == 'ptr-':            
        #    #            if 'porter' in ListNormalMethod:
        #                    listContent = [myPorterStemmer.stem(t) for t in listTokensStped]
                        listContent = listTokens
                        
                        if 'stp-' in  listMyType:
                            listContent = [w for w in listTokens if w.isalpha() and (w.lower() not in myStopwords)]
                            
                        if 'wnl-' in  listMyType:
                            listContent = [wnl.lemmatize(t) for t in listContent]
                            logging.debug("'wnl-' in  listMyType: "+' '.join(listContent))
                            
#                        if myType == 'ptr-':            
#            #            if 'porter' in ListNormalMethod:
#                            listContent = [myPorterStemmer.stem(t) for t in listContent]
                        
                        listWriteData = ' '.join(listContent)
        #                print 'listWriteData: ', listWriteData
                        logging.debug("listWriteData: "+listWriteData)
            #            print row[2], row[4]
            #            print listTokens
            #            training.write('%d\n' % numberAllyear)
#                        if not flagFirsRow:
#            #                training.write(myTmpData+'\n')
#                            training.write(listWriteData+'\n')        
                            
                        for onePICO in listPICO:
                            if onePICO in myLabel:
                                if onePICO == 'P':
                                    logging.debug("onePICO=P")
            #                        myCsvWriterP.writerow([pmid, strOneRecord.encode("utf-8")])
            #                        myCsvWriterP.writerow([pmid, strAbstract])
            #                        myCsvWriterP.writerow([pmid])
#                                    myCsvWriterP.writerow([strOneRecord.encode("utf-8")])
#                                    myCsvWriterP.write(listWriteData+'\n')
#                                    myCsvWriterP.write(strOneRecord.encode("utf-8")+'\n')
                                    myCsvWriterP.write(listWriteData.encode("utf-8")+'\n')
                                elif onePICO == 'I':
                                    logging.debug("onePICO=I")
#                                    myCsvWriterI.writerow([pmid, strOneRecord.encode("utf-8")])
#                                    myCsvWriterI.write(strOneRecord.encode("utf-8")+'\n')
                                    myCsvWriterI.write(listWriteData.encode("utf-8")+'\n')
                                elif onePICO == 'O':
                                    logging.debug("onePICO=O")
#                                    myCsvWriterO.writerow([pmid, strOneRecord.encode("utf-8")])
#                                    myCsvWriterO.write(strOneRecord.encode("utf-8")+'\n')
                                    myCsvWriterO.write(listWriteData.encode("utf-8")+'\n')
                        continue
                            
                            
                            
#            exit()
#            
#            flagLabel = True
#        elif flagLabel and oneRow[0:6] == "      ":
#            myTI = myTI + ' ' + oneRow[6:-1]
##            print 'myTiAfter:', myTI
#            logging.debug('myTiAfter: ' + myTI)
#        elif flagLabel:
#            flagLabel = False
#            strOneRecord = myTI
##            print 'strOneRecord:', strOneRecord
#            logging.debug('strOneRecord: ' + strOneRecord)
#        elif oneRow[0:2] == "AB":
#            myAB =  oneRow[6:-1]
#            flagHasAb = True 
#            flagAb = True
#        elif flagAb and oneRow[0:6] == "      ":
#            myAB = myAB + ' ' + oneRow[6:-1]
#            logging.debug('myAbAfter: ' + myAB)
#        elif flagAb:
#            strOneRecord = strOneRecord + ' ' + myAB
##            PubmedFileTA.write(strYear + ',' + pmid + ',' + strOneRecord.encode("utf-8") + '\n')
#            
#            myCsvWriter.writerow(['Spam'] * 5 + ['Baked Beans'])
            flagAb = False
            strOneRecord = ''
            myTI = ''
            myAB = ''

    
    exit()
    
    config = ConfigObj('scirev.cfg')
    
    if len(sys.argv) < 2:  
        strDefaultKeyword = config['strDefaultKeyword']
    #    print "Input DirMain!"
    #    
    #    exit()
    else:
        strDefaultKeyword = sys.argv[1]
        
#    DirnameMedia = config['dirname']['dirnameMedia']
#    DirnameHome = config['dirname']['dirnameHome']
    
    #    config['DirMain'][sys.argv[1]]
    
    DirMain  = config['dirname'][config['DirMain'][strDefaultKeyword][0]]+config['DirMain'][strDefaultKeyword][1]
    intYearCycle = int(config['DirMain'][strDefaultKeyword][2])
    intStartYear = int(config['DirMain'][strDefaultKeyword][3])
    intEndYear = int(config['DirMain'][strDefaultKeyword][4])
    ListNormalMethod = config['ListNormalMethod']
    
    print config
    print 'intYearCycle: ', intYearCycle, type(intYearCycle)
    print 'intStartYear: ', intStartYear, type(intStartYear)
    print 'intEndYear: ', intEndYear, type(intEndYear)
    print 'ListNormalMethod: ', ListNormalMethod
    #    exit()
    
    
    
    #    ListNormalMethod = ['orgTxt', 'wnl']
        ##ListNormalMethod = ['orgTxt', 'stpwRemoved', 'wnl']
        ##ListNormalMethod = ['stpwRemoved', 'porter', 'lancaster', 'wnl']
        ##for NormalizingTextMethod in ListNormalMethod:
        ##    print 'ListNormalMethod: '+NormalizingTextMethod+' start!'
        #
    
        
#    print "Start, DirMain: ", DirMain
    logging.debug("Start, DirMain: "+ DirMain)
    #    exit()
    
#    PubmedFile   = DirMain + 'pubmed_result.txt'
    PubmedFile   = DirMain + strDefaultKeyword + "_papers.txt"
    ##print 'os.path.abspath(PubmedFile): ', os.path.abspath(PubmedFile)
    ##print 'os.path.basename(PubmedFile): ', os.path.basename(PubmedFile)
    ##print 'os.path.dirname(PubmedFile): ', os.path.dirname(PubmedFile)
    ##exit()
    #
    #
    #
    #PubmedArticleSet = objectify.parse(PubmedFile).getroot()
    #
    #print len(PubmedArticleSet.PubmedArticle[:])
    #
    #
    #myStopwords = nltk.corpus.stopwords.words('english')
    #    
    #if 'wnl' in ListNormalMethod:
    #    wnl = nltk.WordNetLemmatizer()
    #if 'porter' in ListNormalMethod:
    #    myPorterStemmer = nltk.PorterStemmer()
    #if 'lancaster' in ListNormalMethod:
    #    myLancasterStemmer = nltk.LancasterStemmer()
    #
    #fileNamePubmedTA = DirMain+os.path.basename(PubmedFile)[0:len(os.path.basename(PubmedFile))-4:1]+'_TiAb.txt'
    
    
    logging.debug('\n-----------------------------------------------------')
    #parent_conn, child_conn = Pipe()
    #p = Process(target=fSubprocess, args=(child_conn,))
#    fileNamePubmedTA = DirMain+'pubmed_result_TiAb.txt'
#    fileNamePubmedTA = DirMain+'pubmed_result_TiAb_org.txt'
    fileNamePubmedTA = DirMain+'pubmed_result_TiAb_org.txt'
    logging.debug('fileNamePubmedTA Start: '+ fileNamePubmedTA)
#    print 'fileNamePubmedTA Start: ', fileNamePubmedTA
#    ----------------------------
#    |        | forceY | forceN |
#    ----------------------------
#    | ExistY |   Do   |    x   |
#    | ExitN  |   Do   |    Do  | 
#    ----------------------------
    flagForceRegeneratePubmed_result_TiAb = int(config['flagForceRegeneratePubmed_result_TiAb'])
    if (not flagForceRegeneratePubmed_result_TiAb) and os.path.isfile(fileNamePubmedTA):
        logging.debug('PubmedFileTA already exist!')
    else:
        flagNeedAbstract = int(config['flagNeedAbstract'])
        p = Process(target=fSubprocess, args=(fileNamePubmedTA,PubmedFile,flagNeedAbstract,))
        p.start()
        #dicCorpus = parent_conn.recv()
        #print parent_conn.recv()   # prints "[42, None, 'hello']"
        p.join()
    #    exit()
        logging.debug('PubmedFileTA: '+fileNamePubmedTA+' OK!')
    
#    genMlBigram.gen_ML_Bigram(fileNamePubmedTA, fileNamePubmedTA[0:-4]+'_org'+fileNamePubmedTA[-4:])
    flagBigram = int(config['flagBigram']) # 1 or 0
    logging.debug('flagBigram: '+str(flagBigram))
    if flagBigram:
        logging.debug('if flagBigram:')
        genMlBigram.gen_ML_Bigram(fileNamePubmedTA, fileNamePubmedTA[0:-8]+fileNamePubmedTA[-4:])
    else:
        logging.debug(' if flagBigram: else: \n'+fileNamePubmedTA+'\n'+fileNamePubmedTA[0:-8]+fileNamePubmedTA[-4:])
        shutil.copy2(fileNamePubmedTA,fileNamePubmedTA[0:-8]+fileNamePubmedTA[-4:])
#    exit()
    
    #dicCorpus = getDicCorpus(ListNormalMethod, intStartYear, intEndYear)
    dicCorpus = mGetDicCorpus.getDicCorpus(DirMain, ListNormalMethod, intYearCycle, intStartYear, intEndYear)
    
    for NormalizingTextMethod in ListNormalMethod:
        NormalizingTextMethodFlag = NormalizingTextMethod[0:1].upper()
        logging.debug('NormalizingTextMethodFlag: '+NormalizingTextMethodFlag)
    
        File4LdaStd = DirMain + 'year'+NormalizingTextMethodFlag+'.txt'
        with open(File4LdaStd, 'w') as training:
            with open(File4LdaStd[0:-3]+"Pmid", 'w') as trainingPmid:        
                
                #for year in dicCorpus.keys():
                numberAllyear = 0
                for strYearSet in sorted(dicCorpus)[::-1]:
        #            lDocuments = dicCorpus[strYearSet][ListNormalMethod[0][0:1].upper()]
                    lDocuments = dicCorpus[strYearSet][NormalizingTextMethodFlag]
                    numberAllyear += len(lDocuments)

                logging.debug('lenDocuments4YearSet: '+ str(numberAllyear))

                csvWriter = csv.writer(open(DirMain + 'pubmed_Info_'+NormalizingTextMethodFlag+'.csv', "wb"))
                csvWriter.writerow(['SUM', numberAllyear])
                
                training.write('%d\n' % numberAllyear)
    #            trainingPmid.write('%d\n' % numberAllyear)
            #    for year in dicCorpus.keys():
            
    #            print 'sorted(dicCorpus)[::-1]: ', sorted(dicCorpus)[::-1]
                accumulateDoc = 0
                for strYearSet in sorted(dicCorpus)[::-1]:
        #            for myMethod, myContent in dicCorpus[strYearSet].items():
        #            for myMethod, myContent in dicCorpus[strYearSet][NormalizingTextMethodFlag]:
        
        #            fileNameYear = '%syear%s%s0.txt' % (DirMain, NormalizingTextMethodFlag, strYearSet)
                    fileNameYear = '%syear%s%s.txt' % (DirMain, NormalizingTextMethodFlag, strYearSet)
                    lDocuments = dicCorpus[strYearSet][NormalizingTextMethodFlag]
        #            print'strYearSet: '+ strYearSet+ ' lDocuments: '+lDocuments
        
                    lenDocuments4YearSet = len(lDocuments)
                    accumulateDoc = accumulateDoc + lenDocuments4YearSet
#                    print strYearSet, '-', lenDocuments4YearSet
                    logging.debug(strYearSet + '-' + str(lenDocuments4YearSet))
                    csvWriter.writerow([strYearSet, lenDocuments4YearSet, (numberAllyear-accumulateDoc)>lenDocuments4YearSet])
    #                with open(fileNameYear, 'w') as YearFile:
        
    #                with open(fileNameYear[0:-3]+'Pmid', 'w') as YearFilePmid:
    #                        YearFile.write('%d\n' % lenDocuments4YearSet)         # for yearW2010.txt
    #                    YearFilePmid.write('%d\n' % lenDocuments4YearSet)
    #                   training.write('%d  %syear%s%s0.txt\n' % (lenDocuments4YearSet, DirMain, NormalizingTextMethodFlag, strYearSet))
                    for document in lDocuments:
    #                            print document
                        line = ' '.join(document[1:]) + '\n'
    #                            print line
    #                    YearFile.write(line.encode("utf-8"))    # for yearW2010.txt
                        training.write(line)
    
    #                        line = ' '.join(document) + '\n'
    #                        YearFilePmid.write(line.encode("utf-8"))    # yearO1972.Pmid
    #                        trainingPmid.write(line.encode("utf-8"))    # yearO.Pmid
    #                    YearFile.write(document.encode("utf-8"))
    #                    training.write(document.encode("utf-8"))
    
    logging.debug('ListNormalMethod: '+NormalizingTextMethod+' OK!')
#    print sys.argv[0]
    logging.debug(sys.argv[0])
#    print DirMain, 'OK!'
    logging.debug(DirMain + 'OK!')

if __name__ == "__main__":
    fText2input()