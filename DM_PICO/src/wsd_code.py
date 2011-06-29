# -*- coding: utf-8 -*-
from __future__ import division
import nltk
import random
from nltk.corpus import senseval
from nltk.classify import accuracy, NaiveBayesClassifier, MaxentClassifier
from collections import defaultdict

# The following shows how the senseval corpus consists of instances, where each instance
# consists of a target word (and its tag), it position in the sentence it appeared in
# within the corpus (that position being word position, minus punctuation), and the context,
# which is the words in the sentence plus their tags.
# http://www.inf.ed.ac.uk/teaching/courses/fnlp/lectures/wsd_tutorial.html
#
# senseval.instances()[:1]
# [SensevalInstance(word='hard-a', position=20, context=[('``', '``'), ('he', 'PRP'),
# ('may', 'MD'), ('lose', 'VB'), ('all', 'DT'), ('popular', 'JJ'), ('support', 'NN'),
# (',', ','), ('but', 'CC'), ('someone', 'NN'), ('has', 'VBZ'), ('to', 'TO'),
# ('kill', 'VB'), ('him', 'PRP'), ('to', 'TO'), ('defeat', 'VB'), ('him', 'PRP'),
# ('and', 'CC'), ('that', 'DT'), ("'s", 'VBZ'), ('hard', 'JJ'), ('to', 'TO'), ('do', 'VB'),
# ('.', '.'), ("''", "''")], senses=('HARD1',))]

def senses(word):
    """
    This takes a target word from senseval-2 (find out what the possible
    are by running senseval.fileides()), and it returns the list of possible 
    senses for the word
    """
    return list(set(i.senses[0] for i in senseval.instances(word)))


    

def sense_instances(instances, sense):
    """
    This returns the list of instances in instances that have the sense sense
    """
    return [instance for instance in instances if instance.senses[0]==sense]

# >>> sense3 = sense_instances(senseval.instances('hard.pos'), 'HARD3')
# >>> sense3[:2]
# [SensevalInstance(word='hard-a', position=15,
#  context=[('my', 'PRP$'), ('companion', 'NN'), ('enjoyed', 'VBD'), ('a', 'DT'), ('healthy', 'JJ'), ('slice', 'NN'), ('of', 'IN'), ('the', 'DT'), ('chocolate', 'NN'), ('mousse', 'NN'), ('cake', 'NN'), (',', ','), ('made', 'VBN'), ('with', 'IN'), ('a', 'DT'), ('hard', 'JJ'), ('chocolate', 'NN'), ('crust', 'NN'), (',', ','), ('topping', 'VBG'), ('a', 'DT'), ('sponge', 'NN'), ('cake', 'NN'), ('with', 'IN'), ('either', 'DT'), ('strawberry', 'NN'), ('or', 'CC'), ('raspberry', 'JJ'), ('on', 'IN'), ('the', 'DT'), ('bottom', 'NN'), ('.', '.')],
#  senses=('HARD3',)),
#  SensevalInstance(word='hard-a', position=5,
#  context=[('``', '``'), ('i', 'PRP'), ('feel', 'VBP'), ('that', 'IN'), ('the', 'DT'), ('hard', 'JJ'), ('court', 'NN'), ('is', 'VBZ'), ('my', 'PRP$'), ('best', 'JJS'), ('surface', 'NN'), ('overall', 'JJ'), (',', ','), ('"', '"'), ('courier', 'NNP'), ('said', 'VBD'), ('.', '.')],
# senses=('HARD3',))]


_inst_cache = {}

STOPWORDS = ['.', ',', '?', '"', '``', "''", "'", '--', '-', ':', ';', '(',
             ')', '$', '000', '1', '2', '10,' 'I', 'i', 'a', 'about', 'after', 'all', 'also', 'an', 'any',
             'are', 'as', 'at', 'and', 'be', 'being', 'because', 'been', 'but', 'by',
             'can', "'d", 'did', 'do', "don'", 'don', 'for', 'from', 'had','has', 'have', 'he',
             'her','him', 'his', 'how', 'if', 'is', 'in', 'it', 'its', "'ll", "'m", 'me',
             'more', 'my', 'n', 'no', 'not', 'of', 'on', 'one', 'or', "'re", "'s", "s",
             'said', 'say', 'says', 'she', 'so', 'some', 'such', "'t", 'than', 'that', 'the',
             'them', 'they', 'their', 'there', 'this', 'to', 'up', 'us', "'ve", 'was', 'we', 'were',
             'what', 'when', 'where', 'which', 'who', 'will', 'with', 'years', 'you',
             'your']

NO_STOPWORDS = []

def wsd_context_features(instance, vocab, dist=3):
    features = {}
    ind = instance.position
    con = instance.context
    for i in range(max(0, ind-dist), ind):
        j = ind-i
        features['left-context-word-%s(%s)' % (j, con[i][0])] = True

    for i in range(ind+1, min(ind+dist+1, len(con))):
        j = i-ind
        features['right-context-word-%s(%s)' % (j, con[i][0])] = True

 
    features['word'] = instance.word
    features['pos'] = con[1][1]
    return features



def wsd_word_features(instance, vocab, dist=3):
    """
    Create a featureset where every key returns False unless it occurs in the
    instance's context
    """
    features = defaultdict(lambda:False)
    features['alwayson'] = True
    #cur_words = [w for (w, pos) in i.context]
    try:
        for(w, pos) in instance.context:
            if w in vocab:
                features[w] = True
    except ValueError:
        pass
    return features


def extract_vocab(instances, stopwords=STOPWORDS, n=300):
    """
    Given a list of senseval instances, return a list of the n most frequent words that
    appear in the context of instances.  The context is the sentence that the target word
    appeared in within the corpus.
    """
    #cfd = nltk.ConditionalFreqDist()
    fd = nltk.FreqDist()
    for i in instances:
        (target, suffix) = i.word.split('-')
        try:
            words = [w for (w, pos) in i.context if not w == target]
        except ValueError:
            pass
        for word in set(words) - set(stopwords):
            fd.inc(word) 
            #for sense in i.senses:
                #cfd[sense].inc(word)
    return sorted(fd.keys()[:n+1])

def extract_vocab_frequency(instances, stopwords=STOPWORDS, n=300):
    """
    Given a list of senseval instances, return a list of the n most frequent words that
    appears in its context (i.e., the sentence with the target word in), output is in order
    of frequency and includes also the number of instances in which that key appears in the
    context of instances.
    """
    #cfd = nltk.ConditionalFreqDist()
    fd = nltk.FreqDist()
    for i in instances:
        (target, suffix) = i.word.split('-')
        try:
            words = [w for (w, pos) in i.context if not w == target]
        except ValueError:
            pass
        for word in set(words) - set(stopwords):
            fd.inc(word) 
            #for sense in i.senses:
                #cfd[sense].inc(word)
    return fd.items()[:n+1]
        
    
##def wst_classifier(trainer, word, features,number=300):
##    print "Reading data..."
##    global _inst_cache
##    if word not in _inst_cache:
##        _inst_cache[word] = [(i, i.senses[0]) for i in senseval.instances(word)]
##    events = _inst_cache[word][:]
##    senses = list(set(l for (i, l) in events))
##    instances = [i for (i, l) in events]
##    vocab = extract_vocab(instances, n=number)
##    print ' Senses: ' + ' '.join(senses)
##
##    # Split the instances into a training and test set,
##    #if n > len(events): n = len(events)
##    n = len(events)
##    random.seed(5444522)
##    random.shuffle(events)
##    training_data = events[:int(0.8 * n)]
##    test_data = events[int(0.8 * n):n]
##    # Train classifier
##    print 'Training classifier...'
##    classifier = trainer([(features(i, vocab), label) for (i, label) in training_data])
##    # Test classifier
##    print 'Testing classifier...'
##    acc = accuracy(classifier, [(features(i, vocab), label) for (i, label) in test_data] )
##    print 'Accuracy: %6.4f' % acc

    
def wst_classifier(trainer, word, features, stopwords_list = STOPWORDS, number=300, log=False, distance=3, confusion_matrix=False):
    """
    This function takes as arguments:
        a trainer (e.g., NaiveBayesClassifier.train);
        a target word from senseval2 (you can find these out with senseval.fileids(),
            and they are 'hard.pos', 'interest.pos', 'line.pos' and 'serve.pos');
        a feature set (this can be wsd_context_features or wsd_word_features);
        a number (defaults to 300), which determines for wsd_word_features the number of
            most frequent words within the context of a given sense that you use to classify examples;
        a distance (defaults to 3) which determines the size of the window for wsd_context_features (if distance=3, then
            wsd_context_features gives 3 words and tags to the left and 3 words and tags to
            the right of the target word);
        log (defaults to false), which if set to True outputs the errors into a file errors.txt
        confusion_matrix (defaults to False), which if set to True prints a confusion matrix.

    Calling this function splits the senseval data for the word into a training set and a test set (the way it does
    this is the same for each call of this function, because the argument to random.seed is specified,
    but removing this argument would make the training and testing sets different each time you build a classifier).

    It then trains the trainer on the training set to create a classifier that performs WSD on the word,
    using features (with number or distance where relevant).

    It then tests the classifier on the test set, and prints its accuracy on that set.

    If log==True, then the errors of the classifier over the test set are written to errors.txt.
    For each error four things are recorded: (i) the example number within the test data (this is simply the index of the
    example within the list test_data); (ii) the sentence that the target word appeared in, (iii) the
    (incorrect) derived label, and (iv) the gold label.

    If confusion_matrix==True, then calling this function prints out a confusion matrix, where each cell [i,j]
    indicates how often label j was predicted when the correct label was i (so the diagonal entries indicate labels
    that were correctly predicted).
    """
    print "Reading data..."
    global _inst_cache
    if word not in _inst_cache:
        _inst_cache[word] = [(i, i.senses[0]) for i in senseval.instances(word)]
    events = _inst_cache[word][:]
    senses = list(set(l for (i, l) in events))
    instances = [i for (i, l) in events]
    vocab = extract_vocab(instances, stopwords=stopwords_list, n=number)
    print ' Senses: ' + ' '.join(senses)

    # Split the instances into a training and test set,
    #if n > len(events): n = len(events)
    n = len(events)
    random.seed(5444522)
    random.shuffle(events)
    training_data = events[:int(0.8 * n)]
    test_data = events[int(0.8 * n):n]
    # Train classifier
    print 'Training classifier...'
    classifier = trainer([(features(i, vocab, distance), label) for (i, label) in training_data])
    # Test classifier
    print 'Testing classifier...'
    acc = accuracy(classifier, [(features(i, vocab, distance), label) for (i, label) in test_data] )
    print 'Accuracy: %6.4f' % acc
    if log==True:
        #write error file
        print 'Writing errors to errors.txt'
        output_error_file = open('errors.txt', 'w')
        errors = []
        for (i, label) in test_data:
            guess = classifier.classify(features(i, vocab, distance))
            if guess != label:
                con =  i.context
                position = i.position
                item_number = str(test_data.index((i, label)))
                word_list = []
                for (word, tag) in con:
                    word_list.append(word)
                hard_highlighted = word_list[position].upper()
                word_list_highlighted = word_list[0:position] + [hard_highlighted] + word_list[position+1:]
                sentence = ' '.join(word_list_highlighted)
                errors.append([item_number, sentence, guess,label])
        error_number = len(errors)
        output_error_file.write('There are ' + str(error_number) + ' errors!' + '\n' + '----------------------------' +
                                '\n' + '\n')
        for error in errors:
            output_error_file.write(str(errors.index(error)+1) +') ' + 'example number: ' + error[0] + '\n' +
                                    '    sentence: ' + error[1] + '\n' +
                                    '    guess: ' + error[2] + ';  label: ' + error[3] + '\n' + '\n')
        output_error_file.close()
    if confusion_matrix==True:
        gold = [label for (i, label) in test_data]
        derived = [classifier.classify(features(i,vocab)) for (i,label) in test_data]
        cm = nltk.ConfusionMatrix(gold,derived)
        print cm
        return cm
        
        
    
def demo():
    print "NB, with features based on 300 most frequent context words"
    wst_classifier(NaiveBayesClassifier.train, 'hard.pos', wsd_word_features)
    print
    print "NB, with features based word + pos in 6 word window"
    wst_classifier(NaiveBayesClassifier.train, 'hard.pos', wsd_context_features)
    print
##    print "MaxEnt, with features based word + pos in 6 word window"
##    wst_classifier(MaxentClassifier.train, 'hard.pos', wsd_context_features)
    

demo()

# Frequency Baseline
##hard_sense_fd = nltk.FreqDist([i.senses[0] for i in senseval.instances('hard.pos')])
##most_frequent_hard_sense= hard_sense_fd.keys()[0]
##frequency_hard_sense_baseline = hard_sense_fd.freq(hard_sense_fd.keys()[0])

##>>> frequency_hard_sense_baseline
##0.79736902838679902
