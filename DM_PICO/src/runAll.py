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

import logging
import writeConfigObj
import sys
from configobj import ConfigObj
import readExcel
import mergePioTestFiles
#import readPIO5
#import pioNaiveBayes
#import subprocess4Pico
import subprocess4Pico3

logging.basicConfig(level=logging.DEBUG)

#print sys.argv[0]
logging.debug("sys.argv[0]: "+sys.argv[0])

writeConfigObj.fwriteConfigObj()

config = ConfigObj('scirev.cfg')

numFold = int(config['numFold'])
logging.debug("config.filename: "+sys.argv[0])

readExcel.fReadExcel()
mergePioTestFiles.fCreadeCrossValidationFiles(numFold)
#pioNaiveBayes.fNaiveBayesTraining(numFold)
#subprocess4Pico.fNaiveBayesTraining(numFold)
subprocess4Pico3.fNaiveBayesTraining(numFold)







