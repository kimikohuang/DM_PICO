#!/usr/bin/python
"""Generates K (training, validation) pairs from the items in X.

The validation iterables are a partition of X, and each validation
iterable is of length len(X)/K. Each training iterable is the
complement (within X) of the validation iterable, and so each training
iterable is of length (K-1)*len(X)/K.

http://code.activestate.com/recipes/521906-k-fold-cross-validation-partition/
"""

def k_fold_cross_validation(X, K, randomise = False):
    """
    Generates K (training, validation) pairs from the items in X.

    Each pair is a partition of X, where validation is an iterable
    of length len(X)/K. So each training iterable is of length (K-1)*len(X)/K.

    If randomise is true, a copy of X is shuffled before partitioning,
    otherwise its order is preserved in training and validation.
    """
    if randomise: from random import shuffle; X=list(X); shuffle(X)
    for k in xrange(K):
        training = [x for i, x in enumerate(X) if i % K != k]
        validation = [x for i, x in enumerate(X) if i % K == k]
        yield training, validation

#X = [i for i in xrange(97)]
#for training, validation in k_fold_cross_validation(X, K=7):
#    for x in X: assert (x in training) ^ (x in validation), x
    
if __name__ == "__main__":
    X = [i for i in xrange(97)]
    for training, validation in k_fold_cross_validation(X, K=7):
        for x in X: assert (x in training) ^ (x in validation), x