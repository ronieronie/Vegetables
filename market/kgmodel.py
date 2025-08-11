import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import sklearn
df = pd.read_csv('kgmodel1.csv')

x = df.values
y = df['kilograms'].values
x = np.delete(x,2,axis=1)

from sklearn.linear_model import LinearRegression
ml = LinearRegression()
ml.fit(x,y)

pickle.dump(ml, open('kgmodel.pkl','wb'))
kgmodel = pickle.load(open('kgmodel.pkl','rb'))

print(f"✅ Model trained with scikit-learn version: {sklearn.__version__}")