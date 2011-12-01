#!/usr/bin/python
'''
Input:
    'intervention.csv'
    , 'patient.csv'
    , 'outcome.csv'
Output:
    /Output1/(stp|wnl)-intervention.txt
    /Output1/(stp|wnl)-patient.txt
    /Output1/(stp|wnl)-outcome.txt
'''

import csv, codecs, cStringIO
import nltk
import os
import shutil
from configobj import ConfigObj
import logging
import sys

config = ConfigObj('scirev.cfg')

myLevel = int(config['level'])

logging.basicConfig(level=myLevel)

#LOG_FILENAME = '/home/kimiko/git/DM_PICO/DM_PICO/src/example.log'
#logging.basicConfig(filename=LOG_FILENAME,level=myLevel)
#logging.basicConfig(level=myLevel, filename=LOG_FILENAME)

#logging.basicConfig(level='logging.DEBUG')

logging.debug("sys.argv[0]: "+sys.argv[0])


#portfolio = csv.reader(open('/home/kimiko/output.csv', "rb"))
#portfolio = csv.reader(open('intervention.xls', "rb"), dialect='excel')
#names = []
def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')



def fReadExcel():
    dirCwd = os.getcwd()+'/'
#    dirInputExcel = 'Data/'
    dirInputExcel = '/home/kimiko/Downloads/'
    pathOutputBasename = 'Output1/'
    pathOutputDirname = os.path.expanduser('~')+'/'+pathOutputBasename
    logging.info('pathOutputDirname: '+ pathOutputDirname)
#    exit() 
    
    ListInputFilename = ['intervention.csv', 'patient.csv', 'outcome.csv']
#    ListInputFilename = ['intervention.xls', 'patient.xls', 'outcome.xls']
    myStopwords = nltk.corpus.stopwords.words('english')
    ListNormalMethod = ['stpwRemoved', 'wnl', 'porter', 'lancaster']
    
    listMyType = ['stp-', 'wnl-', 'ptr-']

#    myType = 'stp-'
    myType = 'wnl-'
    #myType = 'ptr-'
    
    if 'wnl' in ListNormalMethod:
        wnl = nltk.WordNetLemmatizer()
    if 'porter' in ListNormalMethod:
        myPorterStemmer = nltk.PorterStemmer()
    if 'lancaster' in ListNormalMethod:
        myLancasterStemmer = nltk.LancasterStemmer()
        
    #for myType in listMyType:
#    pathOutputDirname
#    if os.path.isdir(dirCwd+pathOutputBasename):
#        try:
#    #            shutil.rmtree(LDASubDataDir, ignore_errors, onerror)
#            shutil.rmtree(dirCwd+pathOutputBasename)
#        except:
#            raise
#    os.mkdir(dirCwd+pathOutputBasename)
    
    if os.path.isdir(pathOutputDirname):
        try:
    #            shutil.rmtree(LDASubDataDir, ignore_errors, onerror)
            shutil.rmtree(pathOutputDirname)
        except:
            raise
    os.mkdir(pathOutputDirname)
    
    for fileOne in ListInputFilename:
        flagFirsRow = True
#        PubmedFile= dirCwd+dirInputExcel+fileOne
        PubmedFile= dirInputExcel+fileOne
#        print 'PubmedFile: ', PubmedFile
        logging.info('PubmedFile: '+ PubmedFile)
    #    exit()
        
        iteObj = unicode_csv_reader(open(PubmedFile, "rb"), dialect='excel')
    #    print 'type(iteObj): ', type(iteObj)
    #    exit()
        
        
            
    #    with open('wnl-'+PubmedFile[0:-4]+'.txt', 'w') as training:
#        print "dirCwd+pathOutputBasename+myType+fileOne[0:-4]+'.txt': ", dirCwd+pathOutputBasename+myType+fileOne[0:-4]+'.txt'
#        print "pathOutputDirname+myType+fileOne[0:-4]+'.txt': ", pathOutputDirname+myType+fileOne[0:-4]+'.txt'
        logging.info("pathOutputDirname+myType+fileOne[0:-4]+'.txt': "+ pathOutputDirname+myType+fileOne[0:-4]+'.txt')
#        exit()
#        pathOutputDirname
#        with open(dirCwd+pathOutputBasename+myType+fileOne[0:-4]+'.txt', 'w') as training:
        with open(pathOutputDirname+myType+fileOne[0:-4]+'.txt', 'w') as training:
            for row in iteObj: # http://love-python.blogspot.com/2008/02/read-csv-file-in-python.html
            #    names.append((data[0], data[1]))
            #    print ', '.join(row)
    #            myTmpData = ' '.join([row[2].lower(),row[4].lower()])
                myTmpData = ' '.join([row[0].lower(),row[4].lower()])
                listTokens = nltk.wordpunct_tokenize(myTmpData)
                
                listTokensNotDigital = [w for w in listTokens if (not w.isalpha())]
                listTokensStped = [w for w in listTokens if w.isalpha() and (w.lower() not in myStopwords)]
    
    
    #            if 'stpwRemoved' in ListNormalMethod:
    #                listContent = listTokensStped
    #            if 'wnl' in ListNormalMethod:
                if myType == 'stp-':
                    listContent = listTokensStped
                elif myType == 'wnl-':
                    listContent = [wnl.lemmatize(t) for t in listTokensStped]
                elif myType == 'ptr-':            
    #            if 'porter' in ListNormalMethod:
                    listContent = [myPorterStemmer.stem(t) for t in listTokensStped]
                
                myWriteData = ' '.join(listContent)
#                print 'myWriteData: ', myWriteData
                logging.debug('myWriteData: '+ myWriteData)
    #            print row[2], row[4]
    #            print listTokens
    #            training.write('%d\n' % numberAllyear)
                if not flagFirsRow:
    #                training.write(myTmpData+'\n')
                    training.write(myWriteData+'\n')
                    
                flagFirsRow = False
    
    #print names

if __name__ == "__main__":
    fReadExcel()
