import numpy as np
import pandas as pd
import scipy
import matplotlib as plt
import networkx as nx
import itertools
import collections
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder


def convert_categorical(df_X, _X):
    values = np.array(df_X[_X])
    # integer encode
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(values)
    # binary encode
    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    df_X = df_X.drop(_X, 1)
    for j in range(integer_encoded.max() + 1):
        df_X.insert(loc=j + 1, column=str(_X) + str(j + 1), value=onehot_encoded[:, j])
    return df_X


dataPath = 'datasets/ml-1m/'

df = pd.read_csv(dataPath+'ratings.dat', sep='\::', engine='python', names=['UID', 'MID', 'rate', 'time'])
#dff_test = pd.read_csv(dataPath+'u1.test', sep='\\t', engine='python', names=['UID', 'MID', 'rate', 'time'])
df_user = pd.read_csv(dataPath+'users.dat', sep='\::', engine='python', names=['UID', 'gender', 'age', 'job', 'zip'])


df_user = convert_categorical(df_user, 'job')
df_user = convert_categorical(df_user, 'gender')
df_user['bin'] = pd.cut(df_user['age'], [0, 10, 20, 30, 40, 50, 100], labels=['1', '2', '3', '4', '5', '6'])
df_user['age'] = df_user['bin']

df_user = df_user.drop('bin', 1)
df_user = convert_categorical(df_user, 'age')
df_user = df_user.drop('zip', 1)

alpha_coefs = [0.045] #[0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045]

for alpha_coef in alpha_coefs:
    pairs = []
    grouped = df.groupby(['MID', 'rate'])
    for key, group in grouped:
        pairs.extend(list(itertools.combinations(group['UID'], 2)))
    counter = collections.Counter(pairs)
    alpha = alpha_coef * 3883  # param*i_no
    edge_list = map(list, collections.Counter(el for el in counter.elements() if counter[el] >= alpha).keys())
    G = nx.Graph()

    for el in edge_list:
        G.add_edge(el[0], el[1], weight=1)
        G.add_edge(el[0], el[0], weight=1)
        G.add_edge(el[1], el[1], weight=1)

    
    
    