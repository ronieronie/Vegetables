import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import sklearn

df = pd.read_csv('model.csv')

x = df.values
y = df['price'].values
x = np.delete(x,2,axis=1)

from sklearn.linear_model import LinearRegression
ml = LinearRegression()
ml.fit(x,y)

pickle.dump(ml, open('model.pkl','wb'))
model = pickle.load(open('model.pkl','rb'))


print(f"✅ Model trained with scikit-learn version: {sklearn.__version__}")
