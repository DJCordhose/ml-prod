import pandas as pd
import pickle
import numpy, sklearn, pandas

model_name = 'pipeline_pca_std_rf'
model_version = 2

versions = {
    'numpy': numpy.__version__,
    'sklearn': sklearn.__version__, 
    'pandas': pandas.__version__,
    'model_version': model_version,
    'model_name': model_name
}
print(versions)
# we need to have exactly the same versions for serving
pickle.dump(versions, open('model/versions.pickle', 'wb'))

# load data
df = pd.read_csv('data/insurance-customers-1500.csv', sep=';')
stats = df.describe()
print(stats)
# has the distribution of the data changed substantially?
pickle.dump(stats, open('model/describe.pickle', 'wb'))

# X,y, train test
y=df['group']
df.drop('group', axis='columns', inplace=True)
X = df.values
print(X)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
X_train.shape, y_train.shape, X_test.shape, y_test.shape

# setup pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

rf_clf = RandomForestClassifier(max_depth=9, min_samples_leaf=9, min_samples_split=3, n_estimators=7, n_jobs=-1)

column_trans = ColumnTransformer([], remainder=StandardScaler())
pca = PCA()
clf = Pipeline([('standardise', column_trans), ('reduce_dim', pca), ('clf', rf_clf)])

# training
clf.fit(X_train, y_train)
pickle.dump(clf, open('model/model.pickle', 'wb'))

# metrics
from sklearn.model_selection import cross_val_score

train_score = clf.score(X_train, y_train)
test_score = clf.score(X_test, y_test)

cross_val_scores = cross_val_score(clf, X_train, y_train, n_jobs=-1, cv=10)

scores = {
    'cross_val_scores': cross_val_scores,
    'cross_val_mean': cross_val_scores.mean(),
    'cross_val_2std': cross_val_scores.std() * 2,
    'train_score': train_score,
    'test_score': test_score
}
print(scores)
# has the score descread since last time or is suspiciously different?
pickle.dump(scores, open('model/scores.pickle', 'wb'))

