import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
from imblearn.over_sampling import SMOTE

def DataPreprocessing(file,isTrain):
	df = pd.read_csv(file)

	objectColumns = df.select_dtypes(include=["object"]).columns
	df[objectColumns] = df[objectColumns].fillna("Unknown")

	df['DAYS_EMPLOYED_ANOM'] = (df['DAYS_EMPLOYED'] == df['DAYS_EMPLOYED'].max())
	df['DAYS_EMPLOYED'].replace({df['DAYS_EMPLOYED'].max():0},inplace = True)

	df['DAYS_BIRTH'] = abs(df['DAYS_BIRTH'])

	numColumns = []
	for head in df:
		if(df[head].isnull().sum()!=0):
			numColumns.append(head)
	imr = Imputer(missing_values='NaN',strategy='mean',axis=0)
	imr = imr.fit(df[numColumns])
	df[numColumns] = imr.transform(df[numColumns])

	objectColumns = df.select_dtypes(include=["object"]).columns
	var = df[objectColumns].columns
	le = LabelEncoder()
	le_count = 0
	for col in var:
		if len(list(df[col].unique()))<=2:
			le.fit(df[col])
			df[col] = le.transform(df[col])
			le_count += 1

	df = pd.get_dummies(df)

	df['DAYS_EMPLOYED_ANOM'] = df['DAYS_EMPLOYED_ANOM'].astype('int')

	col = df.select_dtypes(include=['int64','float64']).columns
	if(isTrain==True):
		col = col.drop('TARGET')
	df_copy = df

	sc = StandardScaler()
	df_copy[col] = sc.fit_transform(df_copy[col])

	x_feature = list(df_copy.columns)
	if(isTrain==True):
		x_feature.remove('TARGET')
	x_val = df_copy[x_feature]
	if(isTrain==True):
		y_val = df_copy['TARGET']


	pca = PCA(n_components=80,random_state=42)
	pca.fit(x_val)
	X_pca = pca.transform(x_val)

	if(isTrain==True):
		sm = SMOTE(random_state=42, n_jobs = 8)
		X,y = sm.fit_sample(X_pca,y_val)
		return X,y
	else:
		return X_pca