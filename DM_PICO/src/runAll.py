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
import readMedline
import mergePioTestFiles
#import readPIO5
#import pioNaiveBayes
#import subprocess4Pico
import subprocess4Pico3

#writeConfigObj.fwriteConfigObj()
config = ConfigObj('scirev.cfg')

myLevel = int(config['level'])

logging.basicConfig(level=myLevel)

logging.info("config.filename: "+sys.argv[0])

numFold = int(config['numFold'])

InputFileFormat = config['InputFileFormat'] # = 'readMedline' # readExcel, readMedline
logging.info('InputFileFormat = ' + InputFileFormat)


if InputFileFormat == 'readExcel':
    readExcel.fReadExcel()
elif InputFileFormat == 'readMedline':
    readMedline.fReadMedline()

mergePioTestFiles.fCreadeCrossValidationFiles(numFold)
subprocess4Pico3.fNaiveBayesTraining(numFold)





