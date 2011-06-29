from hydrat.frameworks.offline import OfflineFramework
import hydrat.corpora.dummy as dummy

# Subclass dummy.unicode_dummy, to add an automatically-constructed
# train/test split to it, as well as an automatically-contrsucted
# 10-fold cross-validation split.
from hydrat.dataset.split import TrainTest, CrossValidation
class unicode_dummy(dummy.unicode_dummy, TrainTest, CrossValidation): pass

import hydrat.classifier.NLTK as nltk
import hydrat.classifier.SVM as svm
import hydrat.classifier.knn as knn
import hydrat.classifier.nearest_prototype as np
import hydrat.classifier.maxent as maxent
import hydrat.classifier.scikits_learn as scikits_learn
#import hydrat.classifier.flann as flann

learners=\
  [ np.cosine_mean_prototypeL()
  , knn.cosine_1nnL()
  , knn.skew_1nnL()
  , knn.oop_1nnL()
#  , maxent.maxentLearner()
#  , svm.libsvmExtL(kernel_type='linear')
#  , svm.bsvmL(kernel_type='linear')
  , nltk.naivebayesL()
  , nltk.decisiontreeL()
#  , scikits_learn.SVC()
#  , scikits_learn.SVC(kernel='rbf')
#  , scikits_learn.NuSVC()
#  , scikits_learn.LinearSVC()
#  , flann.FLANNL()
#  , flann.kl()
#  , flann.cs()
  ]

if __name__ == "__main__":
  fw = OfflineFramework(unicode_dummy())
  fw.set_class_space('dummy_default')
  fw.set_feature_spaces('byte_unigram')

  def do():
    for l in learners:
      fw.set_learner(l)
      fw.run()

  # Run over crossvalidation split
  fw.set_split('crossvalidation')
  do()

  # Run over train/test split
  fw.set_split('traintest')
  do()

  # Perform tfidf weighting
  from hydrat.common.transform.weight import TFIDF
  fw.transform_taskset(TFIDF())
  do()

  # Extend the task with an additional feature space
  fw.extend_taskset('codepoint_unigram')
  do()