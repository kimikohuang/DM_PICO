#!/usr/bin/python
import re
import csv
import logging

PubmedFile= '/home/kimiko/Downloads/clinical query/_pure-doc-set/'+'pure-doc-dx (copy).txt'

flagTi = False
myTI = ''
flagAb = False
myAB = ''
flagHasTi = False
flagHasAb = False
strYear = ''
strOneRecord = ''

#PubmedFile = csv.writer(open(fileNamePubmedTA, 'rb'), quoting=csv.QUOTE_MINIMAL)

myRe = '((^Title: |^Abstract: )(.*))'
p = re.compile(myRe)

# http://www.chinesepython.org/pythonfoundry/marrpydoc/python5.htm
#r'John.*:'
#re.sub("Marr", "Maher", s)
#p = re.compile(r'^Title: .*'
#r"(Abstract: .*)"
#)
#exit()
with open(PubmedFile) as fTxtOrg:
#        with open(DirMain+os.path.basename(dfile)[0:4]+'W'+os.path.basename(dfile)[5:-4]+'.txt') as fTxtOrg:
    listDocOrg = fTxtOrg.readlines()
#    myString = fTxtOrg.readline()
#    listDocOrg = fTxtOrg.readline()
#   print '\n', myRe, myString, p.findall(myString)
#    print 'len(listDocOrg): ', len(listDocOrg)
#aList = theta.readlines()
#if len(aList) == 0 :
#    numTopics = len(aList)
#print len(aList)
#sum = numpy.fromstring(aList[0],sep=' ') - numpy.fromstring(aList[0],sep=' ')
for myString in listDocOrg[0:100]:
#for myString in listDocOrg:
    myResult = p.search(myString)
    if myResult <> None:
#        print "Not found."
#    else:
#        print 'myResult: ', re.sub('^Title: |^Abstract: ','',myResult.group()
        print 'myResult: ', re.sub('^Title: |^Abstract: ','',myResult.group())

with open('/home/kimiko/output.csv', 'wb') as outf:
#    outcsv = csv.writer(outf)
#    outcsv = csv.writer(outf)
#    for myRow in data:
#        print type(myRow), myRow[0], myRow
#        outcsv.writerow([myRow[0], myRow[1]])
##            outcsv.writerows(dataArray(data, 0, 'unitnames'))
#    for myString in listDocOrg[0:100]:
    for myString in listDocOrg:
        myResult = p.search(myString)
        if myResult <> None:
    #        print "Not found."
    #    else:
    #        print 'myResult: ', re.sub('^Title: |^Abstract: ','',myResult.group()
            myData = re.sub('^Title: |^Abstract: ','',myResult.group())
            print 'myResult: ', myData
#            outcsv.writerow([myData, 'dx'])
#            outcsv.writerow([myData])
            outf.write(myData)
            print myData.split()

        
#         print myResult.group('tl')
#    myFound = p.findall(myString)
#    if len(myFound) > 0:
#        print '\nmyRe: ', myRe, '\nmyString: ', myString, 'myListDocOrg: ', myFound
#    m = p.match(myString)
#    print 'm = p.match(myString): ',
#    print 'p.search(myString).group() :', p.search(myString).group() 


#logging.debug('len(listDocOrg): ' + str(len(listDocOrg)))
exit()


#myString = 'model-00050.tassign'
myString = listDocOrg
print myString
exit()

#myString = 'Mon'
#myRe = '(^model-(final|\d{5}).\w+$)'
#myRe = '(^model-(final|\d{5}).(others|phi|tassign|theta|twords)$)'
#myRe = '(Mon|Tue|Wed|Thu|Fri|Sat|Sun)'

print '\n', myRe, myString, p.findall(myString)
print p.search(myString).group() 
m = p.match(myString)



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
