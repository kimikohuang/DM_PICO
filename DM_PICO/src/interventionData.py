
import csv

data = [('melanogaster', 'True'), ('flies', 'True'), ('fly', 'True'), ('diagnostic', 'True'), ('patients', 'True'), ('specificity', 'True'), ('samples', 'True'), ('clinical', 'True'), ('predictive', 'True'), ('detection', 'True'), ('value', 'True'), ('blood', 'True'), ('chromosome', 'True'), ('sensitivity', 'True'), ('adult', 'True'), ('ratio', 'True'), ('signaling', 'True'), ('mutants', 'True'), ('mutant', 'True'), ('neurons', 'True'), ('loss', 'True'), ('developmental', 'True'), ('stem', 'True'), ('standard', 'True'), ('genetic', 'True'), ('antibodies', 'True'), ('cases', 'True'), ('pathway', 'True'), ('performed', 'True'), ('regulation', 'True'), ('mutations', 'True'), ('processes', 'True'), ('positive', 'True'), ('respectively', 'True'), ('conserved', 'True'), ('body', 'True'), ('conclusion', 'True'), ('disease', 'True'), ('formation', 'True'), ('human', 'True'), ('developed', 'True'), ('assay', 'True'), ('elements', 'True'), ('growth', 'True'), ('genes', 'True'), ('mechanisms', 'True'), ('method', 'True'), ('pathways', 'True'), ('required', 'True'), ('compared', 'True'), ('total', 'True'), ('acid', 'True'), ('groups', 'True'), ('performance', 'True'), ('negative', 'True'), ('demonstrated', 'True'), ('cellular', 'True'), ('essential', 'True'), ('selection', 'True'), ('reported', 'True'), ('imaging', 'True'), ('potential', 'True'), ('proteins', 'True'), ('genome', 'True'), ('substrate', 'True'), ('transcription', 'True'), ('mechanism', 'True'), ('methods', 'True'), ('functions', 'True'), ('expression', 'True'), ('strains', 'True'), ('role', 'True'), ('group', 'True'), ('gene', 'True'), ('reduced', 'True'), ('treatment', 'True'), ('high', 'True'), ('interactions', 'True'), ('cells', 'True'), ('pattern', 'True'), ('evolution', 'True'), ('function', 'True'), ('cancer', 'True'), ('study', 'True'), ('differentiation', 'True'), ('activation', 'True'), ('differences', 'True'), ('protein', 'True'), ('low', 'True'), ('model', 'True'), ('multiple', 'True'), ('rate', 'True'), ('involved', 'True'), ('based', 'True'), ('significant', 'True'), ('development', 'True'), ('motor', 'True'), ('higher', 'True'), ('determined', 'True'), ('variation', 'True'), ('system', 'True'), ('effects', 'True'), ('functional', 'True'), ('evidence', 'True'), ('detected', 'True'), ('specificity', 'False'), ('cell', 'True'), ('rapid', 'True'), ('site', 'True'), ('distinct', 'True'), ('known', 'True'), ('vivo', 'True'), ('process', 'True'), ('family', 'True'), ('expressed', 'True'), ('assays', 'True'), ('patterns', 'True'), ('domain', 'True'), ('demonstrate', 'True'), ('enzyme', 'True'), ('three', 'True'), ('test', 'True'), ('response', 'True'), ('infection', 'True'), ('control', 'True'), ('approach', 'True'), ('analysis', 'True'), ('virus', 'True'), ('receptor', 'True'), ('time', 'True'), ('investigated', 'True'), ('tested', 'True'), ('background', 'True'), ('lines', 'True'), ('presence', 'True'), ('contrast', 'True'), ('complex', 'True'), ('factor', 'True'), ('melanogaster', 'False'), ('addition', 'True'), ('regions', 'True'), ('suggest', 'True'), ('sequences', 'True'), ('activity', 'True'), ('sensitivity', 'False'), ('normal', 'True'), ('study', 'False'), ('large', 'True'), ('range', 'True'), ('revealed', 'True'), ('increased', 'True'), ('first', 'True'), ('including', 'True'), ('identify', 'True'), ('small', 'True'), ('patients', 'False'), ('cells', 'False'), ('genes', 'False'), ('effect', 'True'), ('region', 'True'), ('provide', 'True'), ('associated', 'True'), ('gene', 'False'), ('expression', 'False'), ('molecular', 'True'), ('well', 'True'), ('number', 'True'), ('increase', 'True'), ('one', 'True'), ('genetic', 'False'), ('respectively', 'False'), ('protein', 'False'), ('findings', 'True'), ('identified', 'True'), ('role', 'False'), ('changes', 'True'), ('information', 'True'), ('factors', 'True'), ('detection', 'False'), ('brain', 'True'), ('flies', 'False'), ('cell', 'False'), ('function', 'False'), ('proteins', 'False'), ('diagnosis', 'False'), ('sites', 'True'), ('high', 'False'), ('different', 'True'), ('pathway', 'False'), ('species', 'True'), ('clinical', 'False'), ('diagnostic', 'False'), ('fly', 'False'), ('compared', 'False'), ('tissue', 'True'), ('development', 'False'), ('highly', 'True'), ('human', 'False'), ('major', 'True'), ('signaling', 'False')]

def getUniqueValues(seq):
    "Return sorted list of unique values in sequence"
    values = list(set(seq))
    values.sort()
    return values

def dataArray(data2d, rowIterField=0, rowLabel='', defaultVal=''):
    # get all unique unit and test labels
    rowLabels = getUniqueValues(key[rowIterField] for key in data2d)
    colLabels = getUniqueValues(key[1-rowIterField] for key in data2d)

    # create key-tuple maker
    if rowIterField==0:
        key = lambda row,col: (row, col)
    else:
        key = lambda row,col: (col, row)

    # header row
    yield [rowLabel] + colLabels
    for row in rowLabels:
        # data rows
        yield [row] + [data2d.get(key(row,col), defaultVal) for col in colLabels]

def main():
    with open('/home/kimiko/output.csv', 'wb') as outf:
        outcsv = csv.writer(outf)
        for myRow in data:
            print type(myRow), myRow[0], myRow
            outcsv.writerow([myRow[0], myRow[1]])
#            outcsv.writerows(dataArray(data, 0, 'unitnames'))

if __name__=="__main__":
    main()