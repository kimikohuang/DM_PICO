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
    dirData = 'Data/'
    dirOutput = 'Output1/'
    filesInput = ['intervention.csv', 'patient.csv', 'outcome.csv']
    myStopwords = nltk.corpus.stopwords.words('english')
    ListNormalMethod = ['stpwRemoved', 'wnl', 'porter', 'lancaster']
    
    listMyType = ['stp-', 'wnl-', 'ptr-']
    
    #myType = 'stp-'
    myType = 'wnl-'
    #myType = 'ptr-'
    
    if 'wnl' in ListNormalMethod:
        wnl = nltk.WordNetLemmatizer()
    if 'porter' in ListNormalMethod:
        myPorterStemmer = nltk.PorterStemmer()
    if 'lancaster' in ListNormalMethod:
        myLancasterStemmer = nltk.LancasterStemmer()
        
    #for myType in listMyType:
    
    if os.path.isdir(dirCwd+dirOutput):
        try:
    #            shutil.rmtree(LDASubDataDir, ignore_errors, onerror)
            shutil.rmtree(dirCwd+dirOutput)
        except:
            raise
    os.mkdir(dirCwd+dirOutput)
    
    for fileOne in filesInput:
        flagFirsRow = True
        PubmedFile= dirCwd+dirData+fileOne
        print 'PubmedFile: ', PubmedFile
    #    exit()
        
        iteObj = unicode_csv_reader(open(PubmedFile, "rb"), dialect='excel')
    #    print 'type(iteObj): ', type(iteObj)
    #    exit()
        
        
            
    #    with open('wnl-'+PubmedFile[0:-4]+'.txt', 'w') as training:
        print "dirCwd+dirOutput+myType+fileOne[0:-4]+'.txt': ", dirCwd+dirOutput+myType+fileOne[0:-4]+'.txt'
    #    exit()
        with open(dirCwd+dirOutput+myType+fileOne[0:-4]+'.txt', 'w') as training:
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
                print 'myWriteData: ', myWriteData
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
