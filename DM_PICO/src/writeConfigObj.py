#!/usr/bin/python
# Filename: writeConfigObj.py
"""
input
    NlpClinical_papers.txt
output
    scirev.cfg
"""

from configobj import ConfigObj
import logging
import os

def fwriteConfigObj():
    config = ConfigObj()
    
    searchTerm = "PICO"
    strDefaultKeyword = ''.join(searchTerm.split())
    logging.debug("strDefaultKeyword: "+strDefaultKeyword)
    
    #LEVELS = {'debug': logging.DEBUG,
    #          'info': logging.INFO,
    #          'warning': logging.WARNING,
    #          'error': logging.ERROR,
    #          'critical': logging.CRITICAL}
    
#    config['level'] = logging.DEBUG     # 10
    config['level'] = logging.INFO      # 20
    print "config['level']: ", config['level']
    config['numFold'] = 3
    config['flagComplements'] = 1 # 1 or 0
    config['flagOnlyTrainingUsingExistingData'] = 0 # 1 or 0
    config['flagNaiveBayesTraining'] = 0 # 1 or 0
    
    
    config['wordFeatureRatioStart10times'] = 1
    config['wordFeatureRatioStop10times'] = 14
    config['wordFeatureRatioStep10times'] = 1

    config['InputFileFormat'] = 'readMedline' # readExcel, readMedline  
    
    config['InputFileLocation'] = "/home/kimiko/Downloads"  
    config['InputFilename'] = "pubmed_result(11).txt"  

#wordFeatureRatioStart10times = 21 # default = 3
#wordFeatureRatioStop10times = 27 # default =10 not include
#wordFeatureRatioStep10times = 5 # default =10

#    listMyType = ['stp-', 'wnl-', 'ptr-']
#typeTextPreprocess = ''
#typeTextPreprocess = 'stp-'
#typeTextPreprocess = 'wnl-'
#typeTextPreprocess = 'ptr-'
    config['typeTextPreprocess'] = 'wnl-'


    config['readRIS'] = {}
    config['readRIS']['flagSentenceSplitter'] = 1 # 1 or 0
    

#    config['readRIS']['dirnameHome'] = '/media/c82127d9-0751-40f8-a1df-ba42d8c58846/home/kimiko/Downloads/dLda'
    
#    config['strDefaultKeyword'] = strDefaultKeyword    
#    config['searchTerm'] = searchTerm
#    config['XmlOrText'] = 'Text' # Xml or Text 
#    config['flagForceRefetchPubmed'] = 0 # 1 or 0
#    config['flagForceRegeneratePubmed_result_TiAb'] = 0 # 1 or 0
#    config['flagNeedAbstract'] = 1 # 1 or 0
#    config['flagBigram'] = 0 # 1 or 0
#    
#    
#    
#    dirnameMedia = '/media/231503b8-c5a8-4271-a235-3a4b8cdf3183/home/kimiko/Downloads/dLda2'
#    dirnameHome = '/media/c82127d9-0751-40f8-a1df-ba42d8c58846/home/kimiko/Downloads/dLda'
#    
#    config['dirname'] = {}
#    config['dirname']['dirnameMedia'] = '/media/231503b8-c5a8-4271-a235-3a4b8cdf3183/home/kimiko/Downloads/dLda2'
#    config['dirname']['dirnameHome'] = '/media/c82127d9-0751-40f8-a1df-ba42d8c58846/home/kimiko/Downloads/dLda'
#    
#    config['DirMain'] = {}
#    config['DirMain']['BreastCancer16g'] = ['dirnameMedia', '/BreastCancer16g/', 1, 1951, 2010, 221040, 1700]
#    config['DirMain']['StemCell'] = ['dirnameHome', '/StemCell/', 1, 1991, 2010, 221040, 1600]
#    config['DirMain']['Neurosurgery8t'] = ['dirnameMedia', '/Neurosurgery8t/', 1, 1961, 2010, 200766, 1400]
#    config['DirMain']['Neurosurgery16t'] = ['dirnameMedia', '/Neurosurgery16t/', 1, 1951, 2010, 200766, 1400]
#    config['DirMain']['ColonCancer16g1956'] = ['dirnameHome', '/ColonCancer16g1956/', 1, 1956, 2010, 131325, 1000]
#    config['DirMain']['ColonCancer16g'] = ['dirnameHome', '/ColonCancer16g/', 1, 1956, 2010, 131325, 1000]
#    config['DirMain']['ColonCancer32g'] = ['dirnameHome', '/ColonCancer32g/', 1, 1956, 2010, 131325, 1000]
#    config['DirMain']['Spine8t'] = ['dirnameHome', '/Spine8t/', 1, 1956, 2010, 128395, 902]
#    config['DirMain']['Traumatic16g'] = ['dirnameMedia', '/Traumatic16g/', 1, 1951, 2010, 102474, 680]
#    config['DirMain']['Traumatic16g2'] = ['dirnameMedia', '/Traumatic16g2/', 1, 1951, 2010, 102474, 680]
#    config['DirMain']['EmergencyMedicalService16g'] = ['dirnameMedia', '/EmergencyMedicalService16g/', 1, 1971, 2010, 81890, 551]
#    config['DirMain']['EmergencyMedicalService'] = ['dirnameMedia', '/EmergencyMedicalService/', 1, 1971, 2010, 83736, 551]
#    config['DirMain']['Angiogenesis32g'] = ['dirnameMedia', '/Angiogenesis32g/', 1, 1961, 2010, 0, 496]
#    config['DirMain']['PlasticSurgery16g'] = ['dirnameMedia', '/PlasticSurgery16g/', 1, 1961, 2010, 67025, 408]
#    config['DirMain']['EmergencyMedicine'] = ['dirnameMedia', '/EmergencyMedicine/', 1, 1961, 2010, 53965, 382]
#    config['DirMain']['Maxillofacial'] = ['dirnameMedia', '/Maxillofacial/', 1, 1971, 2010, 34332, 284, 5]
#    config['DirMain']['Helicobacter'] = ['dirnameHome', '/Helicobacter/', 1, 1963, 2010, 0, 272, 4]
#    config['DirMain']['Caries16g'] = ['dirnameHome', '/Caries16g/', 1, 1963, 2010, 40592, 245, 4]
#    config['DirMain']['RadiationTherapyBrain'] = ['dirnameHome', '/RadiationTherapyBrain/', 1, 1967, 2010, 40592, 180, 4]
#    config['DirMain']['Craniofacial'] = ['dirnameMedia', '/Craniofacial/', 1, 1967, 2010, 19939, 155, 4]
#    config['DirMain']['fatexercise'] = ['dirnameHome', '/fatexercise/', 1, 1971, 2010, 9518/9876, 29, 3]
#    config['DirMain']['RootCanalTreatment10g'] = ['dirnameHome', '/RootCanalTreatment10g/', 1, 1940, 2010, 4681, 91, 4]
#    config['DirMain']['antibody'] = ['dirnameMedia', '/antibody/', 1, 1981, 2010, 3764, 40, 3]
#    config['DirMain']['Oyster'] = ['dirnameMedia', '/Oyster/', 1, 1961, 2010, 0, 28]
#    config['DirMain']['Emt8t'] = ['dirnameMedia', '/Emt8t/', 1, 1941, 2010, 4681, 26, 5]
#    config['DirMain']['Emt'] = ['dirnameMedia', '/Emt/', 1, 1941, 2010, 4681, 26, 5]
#    config['DirMain']['Burns16g'] = ['dirnameHome', '/Burns16g/', 1, 1987, 2010, 0, 25, 3]
#    config['DirMain']['Burns32g'] = ['dirnameHome', '/Burns32g/', 1, 1987, 2010, 0, 25, 3]
#    config['DirMain']['Burns'] = ['dirnameHome', '/Burns/', 1, 1987, 2010, 0, 25, 3]
#    config['DirMain']['Nlp16g'] = ['dirnameHome', '/Nlp16g/', 1, 1990, 2010, 2220, 16, 3]
#    config['DirMain']['Nlp32g'] = ['dirnameHome', '/Nlp32g/', 1, 1990, 2010, 2220, 16, 3]
#    config['DirMain']['Singing'] = ['dirnameHome', '/Singing/', 1, 1981, 2010, 1571, 10, 3]
#    config['DirMain']['midlineShift'] = ['dirnameMedia', '/midlineShift/', 1, 1981, 2010, 1571, 10, 3]
#    config['DirMain']['NlpClinical'] = ['dirnameHome', '/NlpClinical/', 1, 1991, 2010, 159, 4.3, 3]
#    config['DirMain']['WieslawNowinski'] = ['dirnameHome', '/WieslawNowinski/', 1, 2001, 2011, 65, 4.3, 3]
#    config['DirMain']['PICO'] = ['dirnameMedia', '/PICO/', 1, 1941, 2010, 4681, 26, 2]
#    
#    #config['DirMain']['Helicobacter'] = ['dirnameHome', '/Helicobacter/', interval, yearStart, yearEnd, cNumber, Mb, yearWindowSize4]
#    #'congenital malformations', 434348
#    #'Congenital', 240690
#    
#    
#    config['2_estmation'] = {}
#    config['2_estmation']['intShiftYears'] = 2
#    config['2_estmation']['intWindowSizeYear'] = 4
#    config['2_estmation']['ListNormalMethod'] = ['orgTxt', 'wnl'] # ['orgTxt', 'stpwRemoved', 'wnl', 'porter', 'lancaster'] 
#    config['2_estmation']['ini_ntopics'] = 8
#    config['2_estmation']['ini_niters'] = 2001
#    config['2_estmation']['ini_twords'] = 30
#    
#    config['3_infAll'] = {}
#    config['3_infAll']['ini_niters'] = 100
#    config['3_infAll']['end_niters'] = 800 # ex: 100, 200, 400, 800 or 1600
#    
#    config['4_corrPhiStdTKey'] = {}
#    config['4_corrPhiStdTKey']['numWords'] = 10
#    
#    config['5_sortDoc4aTopic'] = {}
#    config['5_sortDoc4aTopic']['intCfgNumDocList'] = 10
#    
#    config['LDA_BINARY'] = '/home/kimiko/Workspace/Cpp/GibbsLDA/src/lda'
#    config['ListNormalMethod'] = ['orgTxt', 'wnl'] # ['orgTxt', 'wnl', 'stpwRemoved', 'porter', 'lancaster']
#    
#    config['GraphvizTkinter'] = {}
#    #config['GraphvizTkinter']['filepath'] = '/media/231503b8-c5a8-4271-a235-3a4b8cdf3183/home/kimiko/Downloads/dLda2/EmergencyMedicine/6_corr4Cytoscape_0.4.csv'
#    #config['GraphvizTkinter']['filepath'] = '/home/kimiko/Downloads/dLda/Burns16g/6_corr4Cytoscape_0.4.csv'
#    config['GraphvizTkinter']['fltCutNumShowEdgeLabel'] = 0.1
#    config['GraphvizTkinter']['intEdgeRangeMin'] = 1   # Min 0
#    config['GraphvizTkinter']['intEdgeRangeMax'] = 10   # Max 10
#    config['GraphvizTkinter']['numWords4nodeLabel'] = 10
#    config['GraphvizTkinter']['flagAddEdgeWeight'] = 1 # 1 or 0
#    config['GraphvizTkinter']['numTooltipCharacters'] = 128 # number of characters
#    config['GraphvizTkinter']['url'] = 'http://140.112.137.133/index.shtml'
    
    config.filename = 'scirev.cfg'
    logging.debug("config.filename: "+config.filename)
    config.write()


#    config.filename = config['dirname'][config['DirMain'][strDefaultKeyword][0]]+config['DirMain'][strDefaultKeyword][1]+'scirev.cfg'
#    logging.debug("config.filename: "+config.filename)

#    if not os.path.isdir(os.path.dirname(config.filename)):
#        os.path.dirname(config.filename)
#        try:
##            shutil.rmtree(LDASubDataDir, ignore_errors, onerror)
#            shutil.rmtree(LDASubDataDir)
#        except:
#            raise

#    shutil.rmtree(LDADir+os.path.basename(dfile)[0:8:1],ignore_errors[2])
#    os.makedirs(LDADir+os.path.basename(dfile)[0:8:1])
#    os.makedirs(LDASubDataDir)
#        os.mkdir(os.path.dirname(config.filename))

    
#    config.write()

if __name__ == "__main__":
    fwriteConfigObj()