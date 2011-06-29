from nltk.corpus import names
import random
from nltk.classify import accuracy
from time import sleep
import nltk
import csv

def gender_features(word):
#    return {'last_letter': word[-1]}
    return {'last_letter': word}
#    return {word[-1]}


#iteObj = csv.reader(open(DirMain+'pubmed_result_TiAb.txt', "rb"))
names = []
portfolio = csv.reader(open('/home/kimiko/output.csv', "rb"))
for data in portfolio: # http://love-python.blogspot.com/2008/02/read-csv-file-in-python.html
    names.append((data[0], data[1]))

print names
#exit()
#names = ([(name, 'male') for name in names.words('male.txt')] +[(name, 'female') for name in names.words('female.txt')])

namesTmp = []
namesTmp = names
print type(namesTmp), " names1:", namesTmp

random.shuffle(names)

print type(names), " \nnames2:", len(names), names
#exit()


#featuresets = [(gender_features(n), g) for (n,g) in names]
featuresets = [(gender_features(n), g) for (n,g) in names]
print "featuresets:", len(featuresets), featuresets

#train_set, test_set = featuresets[500:], featuresets[:500]
#print "train_set:", train_set
#print "test_set:", test_set

from nltk.classify import apply_features
#train_set = apply_features(gender_features, names[500:])
#test_set = apply_features(gender_features, names[:500])
train_set = apply_features(gender_features, names[len(featuresets)/10:])
test_set = apply_features(gender_features, names[:len(featuresets)/10])


classifier = nltk.NaiveBayesClassifier.train(train_set)
print "classifier:", classifier.show_most_informative_features(50)
print "sorted(classifier.labels()):", sorted(classifier.labels()) # http://docs.huihoo.com/nltk/0.9.5/guides/classify.html


print "Neo:", classifier.classify(gender_features('Neo'))
print "Trinity:", classifier.classify(gender_features('Trinity'))
print "ay:", classifier.classify(gender_features('Ay'))
print "bby:", classifier.classify(gender_features('Bby'))

print nltk.classify.accuracy(classifier, test_set)

#classifierDT = nltk.DecisionTreeClassifier.train(train_set, entropy_cutoff=0,support_cutoff=0)
#print sorted(classifierDT.labels())
#print classifierDT.batch_classify(test_set)
#print nltk.classify.accuracy(classifierDT, test_set)


