import sklearn
from sklearn.utils import shuffle
from sklearn import datasets
import matplotlib.pyplot as pyplot
import pickle
from matplotlib import style
from sklearn import svm
import pandas as pd
import numpy as np
from sklearn import linear_model, preprocessing

# Load libraries
import numpy
from matplotlib import pyplot as plt
from pandas import read_csv
from pandas import set_option
from pandas.plotting import scatter_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier

mercedes_benz_data = pd.read_csv("mercedes-benz_update.csv")

def safe_to_datetime(date_str):
    return pd.to_datetime(date_str)

mercedes_benz_data['first_reg'] = mercedes_benz_data['first_reg'].apply(safe_to_datetime)

mercedes_benz_data = mercedes_benz_data.dropna(subset=['first_reg'])

mercedes_benz_data['first_reg'] = mercedes_benz_data['first_reg'].astype('int64') // 10**9

predict = "mb"

le = preprocessing.LabelEncoder()
model = le.fit_transform(list(mercedes_benz_data["model"]))
first_reg = le.fit_transform(list(mercedes_benz_data["first_reg"]))
fuel = le.fit_transform(list(mercedes_benz_data["fuel"]))
mileage_km = le.fit_transform(list(mercedes_benz_data["mileage_km"]))
mb = le.fit_transform(list(mercedes_benz_data["seller_type"]))
swift = le.fit_transform(list(mercedes_benz_data["swift"]))
price = le.fit_transform(list(mercedes_benz_data["price"]))
power_hp = le.fit_transform(list(mercedes_benz_data["power_hp"]))

x = list(zip(model,first_reg,fuel,mileage_km,price,swift,power_hp))
y = list(mb)
num_folds = 5
seed = 7
scoring = 'accuracy'

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = 0.20, random_state=seed)

models = []
models.append(('DT', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))
models.append(('GBM', GradientBoostingClassifier()))
models.append(('RF', RandomForestClassifier()))
results = []
names = []

print("Performance on Training set")

for name, model in models:
    kfold = KFold(n_splits=num_folds, shuffle=True, random_state=seed)
    cv_results = cross_val_score(model, x_train, y_train, cv=kfold, scoring='accuracy')
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    msg += '\n'
    print(msg)

dt = DecisionTreeClassifier()
nb = GaussianNB()
svc = SVC()
gb = GradientBoostingClassifier()
rf = RandomForestClassifier()

best_model = rf
best_model.fit(x_train, y_train)
y_pred = best_model.predict(x_test)
model_accuracy = accuracy_score(y_test, y_pred)
print("Best Model Accuracy Score on Test Set:", model_accuracy)

print(classification_report(y_test, y_pred))

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve

best_model = gb
best_model.fit(x_train, y_train)
rf_roc_auc = roc_auc_score(y_test,best_model.predict(x_test))
fpr,tpr,thresholds = roc_curve(y_test, best_model.predict_proba(x_test)[:,1])

fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(20, 5))
fig.tight_layout()

axs[0].boxplot(results)
axs[0].set_xticklabels(names)
axs[0].set_title('Algorithm Comparison')

cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(ax=axs[1])
axs[1].set_title('Confusion Matrix')

axs[2].plot(fpr, tpr, label='Random Forest (area = %0.2f)' % rf_roc_auc)
axs[2].plot([0, 1], [0, 1], 'r--')
axs[2].set_xlim([0.0, 1.0])
axs[2].set_ylim([0.0, 1.05])
axs[2].set_xlabel('False Positive Rate')
axs[2].set_ylabel('True Positive Rate')
axs[2].set_title('Receiver Operating Characteristic')
axs[2].legend(loc='lower right')

plt.subplots_adjust(wspace=0.3)
plt.show()

for x in range(len(y_pred)):
	print("Predicted: ", y_pred[x], "Actual: ", y_test[x], "Data: ", x_test[x],)
