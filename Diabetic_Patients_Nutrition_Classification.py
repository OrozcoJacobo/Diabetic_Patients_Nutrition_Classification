'''
Logistic Regression
Data set that contains detailed nutrition information about food items for people with diabetes. 
Objective => Classify whether a diabetic patient should choose More Often, Less Often or In Moderation for a specific food item based on the nutrition information in the dataset

'''
# %%
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, precision_recall_fscore_support, precision_score, recall_score
import matplotlib.pyplot as plt
import seaborn as sns

#Set a random state
random_state = 123

#------------------------EXPLORATORY DATA ANALYSIS AND FEATURE ENGINEERING---------------------------------

#%%

#Load and explore the dataset
food_df = pd.read_csv("food_items.csv")


#%%
#Quickly check its columns types
print('\nData types:\n')
food_df.dtypes


#%%
#Print the first ten food items
print('\nFist 10 food items:\n')
food_df.head(10)


#%%
#Get the row entries with col 0 to -1 (16)
feature_cols = list(food_df.iloc[:, :-1].columns)
print('\nFeature Columns:\n')
feature_cols


# %%
#Obtain descriptive statistics
print('\nDescriptive statistics\n')
food_df.iloc[: , :-1].describe()
#This dataset contains 17 nutrient categories about each food item. These categories include Calories, Total Fat, Protein, Sugar, etc... and are liste as numeric values
#As such the only need is to scale them for training the logistic regression model, so that a comparison can be performed to the coefficients directly 


# %%
#Check the target variable in the class column to see the label values and their distribution
food_df.iloc[:, -1:].value_counts(normalize=True)#Get the row entries with the last col 'class'


#%%
food_df.iloc[:, -1:].value_counts().plot.bar(color=['yellow', 'red', 'green'])
#From the chart generated by the line above one can tell this data set has 3 classes: In Moderation, Less Often, and More Often. The three labels
#are imbalanced. For diabetic patients, most food items are in the Moderation and Less Often categories. This makes diabetes diet management very hard, so one could build 
#a machine learning model to help patients choose their food

#Three labels means the logistic regression model will be multinomial with three classes

#A multinomial logistic regression is generalized logistic regression model which generates a probability distribution over all classes, based on the logits
#or exponentiated log-odds calculated for each class (susually more than two)

#Note => A multinomial logistic regression model is different from the one-vs-rest binary logistic regression. For one-vs-rest schema, you need to train an independant classifier for each class.
    #i.e one needs a More Often classifier to differentiate a food item between More Often and Not More Often (or, In Moderation and Less Often)



#%%
#FEATURE ENGINEERING
#Process the raw dataset and contruct input data X and label/output y for logistic regression model trainig.

X_raw = food_df.iloc[:, :-1]
y_raw = food_df.iloc[:, -1:]

#Fortunately all feature columns are number so we just need to scale them. Here we use the MinMaxScaler provided by sklearn for scaling

#Create a MinMaxSacler object
scaler = MinMaxScaler()

#Scaling the raw input features
X = scaler.fit_transform(X_raw)

#Check the scaled feature value range:
print(f'The range of feature inputs are within {X.min()} to {X.max()}')


#%%
#For the target variable y, let's use the LabelEncoder provided by sklearn to encode its three class values
#Create a LabelEnconder object
label_encoder = LabelEncoder()
#Encode the target varaible
y = label_encoder.fit_transform(y_raw.values.ravel())
#The encoded target variable will only contain values 0=IN MODERATION, 1=LESS OFTEN, 2=MORE OFTEN
np.unique(y, return_counts=True)


#%%
#TRAIN LOGISTIC REGRESSION MODEL
#Firstsplit the data into training and testing dataset. Training data set will be used to train and tune models, and testing dataset will be used to evaluate the models
#Note that one may also split a validation dataset from the training dataset for model tuning only

#First let's split the training and testing dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state= random_state)

print(f'Traininig dataset shape, X_train: {X_train.shape}, ')
#Now have the training and testing datasets ready, start the model training task


# %%
#L2 penalty to shrink coefficients whithout removing any features from the model
penalty = 'l2'
#Our classification problem is multinomial
multi_class = 'multinomial'
#Use lbfgs for L2 penalty and multinomial classes
solver = 'lbfgs'
#Max iteration = 1000
max_iter = 1000


# %%
#Define a logistic regression model with above arguments
l2_model = LogisticRegression(random_state = random_state, penalty = penalty, multi_class=multi_class, solver=solver, max_iter=max_iter)

#Train the model with training imput data X_train and labels y_train

l2_model.fit(X_train, y_train)


#%%
l2_preds = l2_model.predict(X_test)
#Because one may need to evaluate the modle multiple times with different model hyper parameters, here I define an utility method to take the ground truths y_test and the predictions preds, and return
#a Python dict with accuracy, recall, precision and f1score

#%%
def evaluate_metrics(yt, yp):
    results_pos = {}
    results_pos['accuracy'] = accuracy_score(yt, yp)
    precision, recall, f_beta, _ = precision_recall_fscore_support(yt, yp)
    results_pos['recall'] = recall
    results_pos['precision'] = precision
    results_pos['f1score'] = f_beta
    return results_pos

#%%
evaluate_metrics(y_test, l2_preds)
#Observe that the evalutation results show a logistic model that has relatively good performance on this multinomial classification task
#The overall accuracy is around 0.77 and the f1score is around 0.8. Note that for recall, precision and f1score, the output shows values for each class to see how the model performs on an indiviudal class
#see from the results the recall for class 2 (More Often) is not very good. This is actually  common problem called imbalanced classification challenge(but I will not fix it for now, its not the focus right now)


#%%