from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score
import pandas as pd


trainData = pd.read_csv('timbl_pos_ngrams_train_1.csv',sep=",")
testData = pd.read_csv('timbl_pos_ngrams_test_1.csv',sep=",",)





clf = RandomForestClassifier(n_estimators=20, n_jobs=2)


ncols  = len(trainData.columns)
train_y = trainData[trainData.columns[-1]]



clf.fit(trainData[trainData.columns[0:ncols-2]], train_y)


preds = clf.predict(testData[testData.columns[0:ncols-2]])

test_y = testData[testData.columns[-1]]

print accuracy_score(test_y,preds)
