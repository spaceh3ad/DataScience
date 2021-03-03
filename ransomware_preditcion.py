from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error

import pandas as pd

# df as data.zip in https://archive.ics.uci.edu/ml/machine-learning-databases/00526/
df = pd.read_csv('BitcoinHeistData.csv')

global lb
lb = LabelEncoder()
y = lb.fit_transform(df.label)
# y = df.label

features = ['length','weight','count','looped','neighbors','income']
X = df[features]

train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=0) 

def mea(max_leaf_nodes, train_X, val_X, train_y, val_y):
	ransomware_model = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, random_state=1)
	ransomware_model.fit(train_X,train_y)

	predictions = [int(i) for i in ransomware_model.predict(val_X)]
	return mean_absolute_error(val_y, predictions)

candidate_max_leaf_nodes = [5, 25, 50, 100, 250, 500]

mea_min = min([(mea(i, train_X, val_X, train_y, val_y ), i) for i in candidate_max_leaf_nodes])
print(mea_min)
