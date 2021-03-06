#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'maxent-classifier'))
	print(os.getcwd())
except:
	pass
    
#%% [markdown]
#  # CMSC 678 — Introduction to Machine Learning
#  ## Assignment 3
#  ## Divyesh Chitroda

#%%
import gzip, pickle, numpy
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
get_ipython().run_line_magic('matplotlib', 'inline')

#%%
with gzip.open('mnist_rowmajor.pkl.gz', 'rb') as data_fh:
   data = pickle.load(data_fh, encoding='latin1')

#%%
trainX = data["images_train"]
trainY = data["labels_train"]

testX = data["images_test"]
testY = data["labels_test"]

#%%
img_index = 207
img = trainX[img_index].reshape(28,28)
plt.imshow(img, cmap='Greys')
print(trainY[img_index])

#%%
split_idx = int(trainX.shape[0] * 0.7)

train_splitX = trainX[:split_idx]
train_splitY = trainY[:split_idx]
print(train_splitX.shape)

dev_splitX = trainX[split_idx:]
dev_splitY = trainY[split_idx:]
print(dev_splitX.shape)

#%%
labels, count = numpy.unique(train_splitY, return_counts = True)
print(count)
plt.bar(labels, count)
plt.xlabel("labels")
plt.ylabel("frequency")
plt.savefig("bctry.png")

#%%
labels, count = numpy.unique(dev_splitY, return_counts = True)
print(count)
plt.bar(labels, count)
plt.xlabel("labels")
plt.ylabel("frequency")
plt.savefig("bctsy.png")

#%%
clf = LogisticRegression(random_state=0, solver='liblinear', multi_class="ovr")
clf.fit(train_splitX, train_splitY)
clf.score(dev_splitX, dev_splitY)

#%%
y_pred = clf.predict(dev_splitX)
print(confusion_matrix(dev_splitY, y_pred))
print(classification_report(dev_splitY, y_pred))

#%%
clf = LogisticRegression(random_state=0, solver='liblinear', multi_class="ovr", penalty="l1")
clf.fit(train_splitX, train_splitY)
clf.score(dev_splitX, dev_splitY)

#%%
y_pred = clf.predict(dev_splitX)
print(confusion_matrix(dev_splitY, y_pred))
print(classification_report(dev_splitY, y_pred))

#%%
# dclf = DummyClassifier(strategy='most_frequent', random_state=0)
# dclf.fit(train_splitX, train_splitY)
# dclf.score(dev_splitX, dev_splitY)

#%%
feat_max = lambda arr : numpy.max(arr)
# feat_avg = lambda arr : 1 if numpy.sum(arr)/(len(arr) ** 2) >= 0.5 else 0
feat_avg = lambda arr : numpy.sum(arr)/(len(arr) ** 2)
# feat_avg = lambda arr : numpy.sum(arr)

def featurization(image, mask, fc="max"):
    func = feat_max
    if fc == "avg":
        func = feat_avg
    
    m = len(image)
    k = m - mask + 1
    result = numpy.zeros((k, k))
    for i in range(k):
        for j in range(k):
            result[i][j] = func(image[i:i+mask, j:j+mask])

    return result

#%%
temp = featurization(train_splitX[208].reshape((28,28)), 3, "avg")
plt.imshow(temp, cmap='Greys')

#%%
# max featurization
(m,n) = train_splitX.shape
f1_train_splitX = numpy.zeros((m, 27*27), dtype=object)
for i in range(m):
    features = featurization(train_splitX[i].reshape((28,28)), 2, "max")
    f1_train_splitX[i, numpy.newaxis] = features.flatten()

(m,n) = dev_splitX.shape
f1_dev_splitX = numpy.zeros((m,27*27), dtype=object)
for i in range(m):
    features = featurization(dev_splitX[i].reshape((28,28)), 2, "max")
    f1_dev_splitX[i] = features.flatten()


#%%
print(train_splitX.shape, f1_train_splitX.shape)
clf = LogisticRegression(random_state=0, solver='liblinear', multi_class="ovr", penalty="l2")
clf.fit(f1_train_splitX, train_splitY)
clf.score(f1_dev_splitX, dev_splitY)

#%%
y_pred = clf.predict(f1_dev_splitX)
print(confusion_matrix(dev_splitY, y_pred))
print(classification_report(dev_splitY, y_pred))


#%%
# average featurization
(m,n) = train_splitX.shape
f2_train_splitX = numpy.zeros((m, 26*26), dtype=object)
for i in range(m):
    features = featurization(train_splitX[i].reshape((28,28)), 3, "avg")
    f2_train_splitX[i] = features.flatten()

(m,n) = dev_splitX.shape
f2_dev_splitX = numpy.zeros((m,26*26), dtype=object)
for i in range(m):
    features = featurization(dev_splitX[i].reshape((28,28)), 3, "avg")
    f2_dev_splitX[i] = features.flatten()

#%%
print(train_splitX.shape, f2_train_splitX.shape)
clf = LogisticRegression(random_state=0, solver='liblinear', multi_class="ovr", penalty="l2")
clf.fit(f2_train_splitX, train_splitY)
clf.score(f2_dev_splitX, dev_splitY)

#%%
y_pred = clf.predict(f2_dev_splitX)
print(confusion_matrix(dev_splitY, y_pred))
print(classification_report(dev_splitY, y_pred))

#%%
# test evaluation
clf = LogisticRegression(random_state=0, solver='liblinear', multi_class="ovr", penalty="l1")
clf.fit(trainX, trainY)
clf.score(testX, testY)

#%%
y_pred = clf.predict(testX)
print(confusion_matrix(testY, y_pred))
print(classification_report(testY, y_pred))

#%%
