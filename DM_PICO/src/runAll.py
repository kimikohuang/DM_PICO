#!/usr/bin/python
# Filename: runAll.py
"""
input
    pubmed_result.txt
    scirev.cfg
output
    a: pubmed_result_TiAb.txt
    yearO.txt
    yearW.txt
    each year set phi, theta
    3_topicTrend_800.csv
    4_topicKeyWords5_All.csv
    5_sortDoc4Topics.csv
    6_corr4Cytoscape_1.0.csv
    6_topicHighestCorr.csv
"""

import readExcel
import mergePioTestFiles
#import readPIO5
import pioNaiveBayes

numFold = 5

readExcel.fReadExcel()
mergePioTestFiles.fCreadeCrossValidationFiles(numFold)
#readPIO5.fNaiveBayesTraining(numFold)
pioNaiveBayes.fNaiveBayesTraining(numFold)
exit()

#import writeConfigObj
import sys
from configobj import ConfigObj
#import aXml2input
import bioPyEfetchPubmed
import aText2input
import bEstimation
import cInfAll
import dCorrPhiStdTKey
import eSortDoc4aTopic
import fGetNewPhi
import pgvTk
import os
import logging

writeConfigObj.fwriteConfigObj()

print sys.argv[0]
config = ConfigObj('scirev.cfg')
XmlOrText = config['XmlOrText']
strDefaultKeyword = config['strDefaultKeyword']
DirMain  = config['dirname'][config['DirMain'][strDefaultKeyword][0]]+config['DirMain'][strDefaultKeyword][1]
flagForceRefetchPubmed = int(config['flagForceRefetchPubmed'])

if XmlOrText == 'Xml':
    __import__(aXml2input)
    aXml2input.fXml2input()
elif XmlOrText == 'Text':
    logging.debug(str(flagForceRefetchPubmed) + str(not os.path.isfile(DirMain + strDefaultKeyword+"_papers.txt")) + DirMain + strDefaultKeyword+"_papers.txt")
    
    if flagForceRefetchPubmed or (not os.path.isfile(DirMain + strDefaultKeyword+"_papers.txt")):
        logging.debug("Refetch Pubmed!")
        bioPyEfetchPubmed.fbioPyEfetchPubmed()
    else:
        logging.debug(str(not flagForceRefetchPubmed))

    aText2input.fText2input()
else:
    print 'Miss XmlOrText on scirev.cfg file'

#bEstimation.fEstimation()
#cInfAll.fInfAll()
dCorrPhiStdTKey.fCorrPhiStdTkey()
eSortDoc4aTopic.fXortDoc4aTopic()
fGetNewPhi.fGetNewPhi()
pgvTk.fGraphvizTkinter()
