import random
import nltk
from nltk.corpus import movie_reviews
documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]
print documents[0]
exit()
random.shuffle(documents)


all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = all_words.keys()[:2000]

def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

print "movie_reviews.words('pos/cv957_8737.txt'):", movie_reviews.words('pos/cv957_8737.txt')
print document_features(movie_reviews.words('pos/cv957_8737.txt'))


featuresets = [(document_features(d), c) for (d,c) in documents]
train_set, test_set = featuresets[100:], featuresets[:100]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print nltk.classify.accuracy(classifier, test_set)
#0.81
classifier.show_most_informative_features(50)

