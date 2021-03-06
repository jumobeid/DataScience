#!/usr/bin/env python
# coding: utf-8

# In[2]:


#Load Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns


# In[3]:


#Load Dataset
dataset = pd.read_csv(r'c:/Python/mtcars.csv')
dataset.head()


# In[4]:


#Remove Model Column
dataset2=dataset.drop('model',axis=1)
dataset2.head()


# In[5]:


#Overview of Dataset Characteristics
dataset2.info()


# In[6]:


#Summary of N/A Values
dataset2.isnull().sum()


# In[7]:


dataset2.describe()


# In[8]:


#BoxPlot Feature Set Comparison
fig = plt.figure(figsize=(15,5))
fig.suptitle('Feature Set Comparison')
ax = fig.add_subplot(111)
sns.boxplot(data=dataset)
plt.show()


# In[9]:


#Visualization of Correlations
fig = plt.figure(figsize=(10,5))
sns.heatmap(dataset2.corr(),annot=True,cmap="Blues")


# In[23]:


#Find Independent Column Correlations
def correlation(dataset,threshold):
    col_corr= [] # List of correlated columns
    corr_matrix=dataset.corr() #finding correlation between columns
    for i in range (len(corr_matrix.columns)): #Number of columns
        for j in range (i):
            if abs(corr_matrix.iloc[i,j])>threshold: #checking correlation between columns
                colName=(corr_matrix.columns[i], corr_matrix.columns[j]) #getting correlated columns
                col_corr.append(colName) #adding correlated column name
    return col_corr #returning set of column names
col=correlation(dataset2,0.8)
print('Correlated columns @ 0.8:', col)


# In[26]:


#Create x and y variables
x = dataset2.drop('mpg', axis=1).to_numpy()
Y = dataset2['mpg'].to_numpy()
#Create Train and Test Datasets
from sklearn.model_selection import train_test_split
x_train,x_test,Y_train,Y_test = train_test_split(x,Y,test_size = 0.2,random_state = 100)
#Scale the Data
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
x_train2 = sc.fit_transform(x_train)
x_test2 = sc.transform(x_test)
#Model
from sklearn.neighbors import KNeighborsRegressor


# In[55]:


#Learning Curve
from sklearn.model_selection import learning_curve

def plot_learning_curves(model):
    train_sizes,train_scores,test_scores = learning_curve(estimator=model,
    X=x_train2,y=Y_train,train_sizes=np.linspace(.1,1,10),
    scoring = 'neg_root_mean_squared_error',cv=10, random_state=100)
    train_mean = np.sqrt(np.mean(-train_scores, axis=1))
    train_std = np.sqrt(np.std(-train_scores, axis=1))
    test_mean = np.sqrt(np.mean(-test_scores, axis=1))
    test_std = np.sqrt(np.std(-test_scores, axis=1))
    plt.plot(train_sizes, train_mean,color='blue', marker='o',markersize=5, label='training accuracy')
    plt.fill_between(train_sizes, train_mean + train_std, train_mean - train_std,alpha=0.15, color='blue')
    plt.plot(train_sizes, test_mean, color='green', linestyle='--', marker='s', markersize=5,label='validation accuracy')
    plt.fill_between(train_sizes, test_mean + test_std, test_mean - test_std,alpha=0.15, color='green')
    plt.grid(True)
    plt.xlabel('Number of training samples')
    plt.ylabel('RMSE')
    plt.legend(loc='best')
    plt.ylim([0,10])
    plt.show()


# In[57]:


#Plot Learning Curve
print('k-NN Regressor Learning Curve')
plot_learning_curves(KNeighborsRegressor(2))


# In[59]:


#Bias and Variance
from mlxtend.evaluate import bias_variance_decomp
#Script for Bias Variance
print('Bias Variance Trade-Off')
for name,method in[('kNN',KNeighborsRegressor(2))]:
    avg_expected_loss, avg_bias, avg_var = bias_variance_decomp(method, x_train2, Y_train, x_test2, Y_test,
    loss='mse',random_seed=100)
print('\nEstimator: {}'.format(name))
print('Average Bias: {:.2f}'.format(avg_bias))
print('Average Variance: {:.2f}'.format(avg_var))


# In[63]:


#Original Model - KNN
#Search for an optimal value of K for KNN
from sklearn.model_selection import cross_val_score
from sklearn import metrics
k_range = range(1, 10)
k_scores = []
for k in k_range:
    knn_org = KNeighborsRegressor(n_neighbors=k)
#obtain cross_val_score for KNeighborsClassifier with k neighbours
scores = cross_val_score(knn_org, x_train2, Y_train, cv=10, scoring='neg_root_mean_squared_error')
#append mean of scores for k neighbors to k_scores list
k_scores.append(scores.mean())
#Print Best Score
BestScore = [1 - x for x in k_scores]
best_k = k_range[BestScore.index(min(BestScore))]
#Create Orginal KNN model
classifier_org = KNeighborsRegressor(n_neighbors = best_k)
#Fit KNN Model
classifier_org.fit(x_train2, Y_train)
#Prediction
y_pred_org = classifier_org.predict(x_test2)
print('Original Model')
print('\nn_neighbors:',str(best_k))
print('\nR2: {:.2f}'.format(metrics.r2_score(Y_test, y_pred_org)))
adjusted_r_squared = 1-(1-metrics.r2_score(Y_test,y_pred_org))*(len(Y)-1)/(len
(Y)-x.shape[1]-1)
print('Adj_R2: {:0.2f}'.format(adjusted_r_squared))
print('Mean Absolute Error: {:0.2f}'.format(metrics.mean_absolute_error(Y_test
, y_pred_org)))
print('Mean Squared Error: {:0.2f}'.format(metrics.mean_squared_error(Y_test,
y_pred_org)))
print('Root Mean Squared Error: {:0.2f}'.format(np.sqrt(metrics.mean_squared_error(Y_test, y_pred_org))))


# In[67]:


#Gridsearch
from sklearn.model_selection import GridSearchCV
#k-NN Regression Model
knnreg2 = KNeighborsRegressor()
k_range = range(1, 10)
param_grid = {
'n_neighbors': k_range,
'algorithm' : ['auto','ball_tree','kd_tree','brute'],
'weights' : ['uniform','distance']}
knn_model = GridSearchCV(knnreg2, param_grid, cv=10, verbose=0,
scoring='neg_root_mean_squared_error')
grids = [knn_model]
grid_dict = {0:'k-NN Regression Model'}
#Model Creation
#Create Heading
print('Optimized Model')
#Fit the grid search objects
for idx, optmodel in enumerate(grids):
    print('\nEstimator: {}'.format(grid_dict[idx]))
#Fit grid search
optmodel.fit(x_train2, Y_train)
#Best params
print('\nBest params: {}'.format(optmodel.best_params_))
# Predict on test data with best params
y_pred3 = optmodel.predict(x_test2)
# Test data accuracy of model with best params
print('\nR2: {:.2f}'.format(metrics.r2_score(Y_test, y_pred3)))
adjusted_r_squared = 1-(1-metrics.r2_score(Y_test,y_pred3))*(len(Y)-1)/(len(Y)-x.shape[1]-1)
print('Adj_R2: {:0.2f}'.format(adjusted_r_squared))
#Print MSE and RMSE
print('Mean Absolute Error: {:.2f}'.format(metrics.mean_absolute_error(Y_test, y_pred3)))
print('Mean Squared Error: {:.2f}'.format(metrics.mean_squared_error(Y_test, y_pred3)))
print('Root Mean Squared Error: {:.2f}'.format(np.sqrt(metrics.mean_squared_error(Y_test, y_pred3))))

