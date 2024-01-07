# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18RpHDOUkFR_CHGWYQqKvU7TDhfoYgzp5
"""

pip install mlflow

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import mlflow  # Import MLflow

import os
for dirname, _, filenames in os.walk('/IntelligentEngineering/'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

df_train=pd.read_csv('/content/train.csv')

df_train.head()

df_train.tail()

df_train.shape

df_train.isnull().sum()

df_train['Activity'].unique()

plt.figure(figsize=(12, 6))

# Get counts for each activity
activity_counts = df_train['Activity'].value_counts()

# Create bar chart using plt.bar
plt.bar(activity_counts.index, activity_counts.values)
plt.xlabel("Activity")
plt.ylabel("Count")

plt.xticks(rotation='vertical')
plt.tight_layout()  # Adjust layout for better spacing
plt.show()

df_train['subject'].unique()

X=pd.DataFrame(df_train.drop(['Activity','subject'],axis=1))
y=df_train.Activity.values.astype(object)

X.shape , y.shape

X.head()

y[5]

X.info()

num_cols = X._get_numeric_data().columns
print("Number of numeric features:",num_cols.size)

from sklearn import preprocessing

encoder=preprocessing.LabelEncoder()

encoder.fit(y)
y=encoder.transform(y)
y.shape

y[5]

encoder.classes_

encoder.classes_[5]

from sklearn.preprocessing import StandardScaler

scaler=StandardScaler()

X=scaler.fit_transform(X)

X[5]

from sklearn.model_selection import train_test_split

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.20,random_state=100)

X_train.shape, X_test.shape, y_train.shape, y_test.shape

from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# import metrics to compute accuracy (Evulate)
from sklearn.metrics import accuracy_score, confusion_matrix,classification_report
from sklearn.model_selection import cross_val_score, GridSearchCV

svc=SVC()

svc.fit(X_train,y_train)

y_pred=svc.predict(X_test)

svc2=SVC(kernel='rbf',C=100.0)


# fit classifier to training set
svc2.fit(X_train,y_train)

# make predictions on test set
y_pred2 = svc2.predict(X_test)

print('Model accuracy score with rbf kernel and C=100.0 : {0:0.4f}'. format(accuracy_score(y_test, y_pred2)))

"""# Now Random Forest Classifier"""

rand_clf=RandomForestClassifier(random_state=5)

rand_clf.fit(X_train,y_train)

# compute and print accuracy score
rand_clf.score(X_test,y_test)
import numpy as np
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import RandomizedSearchCV
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

# Load data
df = pd.read_csv('/content/train.csv')

# Define features and target variable
X = df.drop('Activity', axis=1)  # Drop the target column from X
y = df['Activity']  # Define the target variable

# Split the bloody data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Impute missing values with mean !! damn you MCU
imputer = SimpleImputer(strategy='mean')
X_train = imputer.fit_transform(X_train)
X_test = imputer.transform(X_test)

# SVC Model Training
svc = SVC()
svc.fit(X_train, y_train)
y_pred = svc.predict(X_test)

svc2 = SVC(kernel='rbf', C=100.0)
svc2.fit(X_train, y_train)
y_pred2 = svc2.predict(X_test)
# Convert y_test and y_pred2 to the same type if they are not
y_test = y_test.astype(str)  # or use .astype(int) as necessary
y_pred2 = y_pred2.astype(str)  # or use .astype(int) as necessary
print('Model accuracy score with rbf kernel and C=100.0 : {0:0.4f}'.format(accuracy_score(y_test, y_pred2)))

# Random Forest Classifier
rand_clf = RandomForestClassifier(random_state=5)

# Reduced and more targeted grid parameters for RandomizedSearchCV
grid_param = {
    'n_estimators': [100, 120, 140],
    'criterion': ['gini', 'entropy'],
    'max_depth': np.arange(5, 15),
    'min_samples_leaf': np.arange(1, 5),
    'min_samples_split': np.arange(2, 6),
    'max_features': ['sqrt', 'log2']
}

# Using RandomizedSearchCV

rand_search = RandomizedSearchCV(
    estimator=rand_clf,
    param_distributions=grid_param,
    n_iter=10,
    cv=3,
    verbose=3,
    random_state=5,
    n_jobs=-1
)


rand_search.fit(X_train, y_train)
best_parameters = rand_search.best_params_
best_score = rand_search.best_score_

print("Best parameters found: ", best_parameters)
print("Best score found: ", best_score)

# Training the best Random Forest model
best_rand_clf = RandomForestClassifier(**best_parameters)
best_rand_clf.fit(X_train, y_train)

# MLflow integration
with mlflow.start_run():
    # Log parameters and metrics
    mlflow.log_params(best_parameters)
    mlflow.log_metric("accuracy", best_score)

    # Log the model
    mlflow.sklearn.log_model(best_rand_clf, "RandomForestClassifier")
