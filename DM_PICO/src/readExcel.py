import csv, codecs, cStringIO

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

filesInput = ['intervention.csv', 'patient.csv', 'outcome.csv']
dirMain = ''
for fileOne in filesInput:
    flagFirsRow = True
    PubmedFile= dirMain+fileOne
    
    qq = unicode_csv_reader(open(PubmedFile, "rb"), dialect='excel')
    
    with open(PubmedFile[0:-4]+'.txt', 'w') as training:
        for row in qq: # http://love-python.blogspot.com/2008/02/read-csv-file-in-python.html
        #    names.append((data[0], data[1]))
        #    print ', '.join(row)
            myWriteData = ', '.join([row[2],row[4]])
#            print row[2], row[4]
            print myWriteData
#            training.write('%d\n' % numberAllyear)
            if not flagFirsRow:
                training.write(myWriteData+'\n')
            flagFirsRow = False

#print names
