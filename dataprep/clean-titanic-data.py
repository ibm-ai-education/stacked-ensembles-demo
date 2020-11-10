import pandas as pd
import numpy as np

# Performs various transformations on Kaggle training set for Titanic
# to make it palatable for a ML model

# Get  training set
df_train = pd.read_csv('train.csv')

#Data Cleaning and Data Drop Process

# Impute median for missing fare
df['Fare'] = df['Fare'].fillna(df['Fare'].dropna().median())

# Change to sex column to numeric
df.loc[df['Sex']=='male','Sex']=0
df.loc[df['Sex']=='female','Sex']=1
df = df.astype({"Sex": int})

# Impute Southampton for port of embarkation
df['Embarked']=df['Embarked'].fillna('S')
# Change  emabarked column to numeric
df.loc[df['Embarked']=='S','Embarked']=0
df.loc[df['Embarked']=='C','Embarked']=1
df.loc[df['Embarked']=='Q','Embarked']=2


# For Title map to fixed set of values
df['Title'] = df['Name'].apply(lambda name: name.split(',')[1].split('.')[0].strip())
# normalize the titles
normalized_titles = {
    "Capt":       "Officer",
    "Col":        "Officer",
    "Major":      "Officer",
    "Jonkheer":   "Royalty",
    "Don":        "Royalty",
    "Sir" :       "Royalty",
    "Dr":         "Officer",
    "Rev":        "Officer",
    "the Countess":"Royalty",
    "Dona":       "Royalty",
    "Mme":        "Mrs",
    "Mlle":       "Miss",
    "Ms":         "Mrs",
    "Mr" :        "Mr",
    "Mrs" :       "Mrs",
    "Miss" :      "Miss",
    "Master" :    "Master",
    "Lady" :      "Royalty"
}

# map the normalized titles to the current titles
df['Title'] = df['Title'].map(normalized_titles)# view value counts for the normalized titles
print(df['Title'].value_counts())

# Imute missing ages with median age grouped
# by Sex, Pclass, and Title
grouped = df.groupby(['Sex','Pclass', 'Title'])  # view the median Age by the grouped features
grouped['Age'].median()

# apply the grouped median value on the Age NaN
df['Age'] = grouped['Age'].apply(lambda x: x.fillna(x.median()))


# Create bins for groups of ages
bins = [-1, 0, 14, 25, 35, 60, np.inf]
labels = ['Unknown', 'Child', 'Teenager', 'Young Adult', 'Adult', 'Senior']
df['AgeGroup'] = pd.cut(df["Age"], bins, labels = labels)
age_mapping = {'Unknown': None,'Child': 1, 'Teenager': 2, 'Young Adult': 3, 'Adult': 4, 'Senior': 5}
df['AgeGroup'] = df['AgeGroup'].map(age_mapping)


# size of families (including the passenger)
df['FamilySize'] = df['Parch'] + df['SibSp'] + 1
# fill Cabin NaN with U for unknown
df['Cabin'] = df['Cabin'].fillna('U')# find most frequent Embarked value and store in variable



# map first letter of cabin to itself
# Had cabin is boolean indicatiing whether passenger had assigned cabin
df['HadCabin'] = np.where(df['Cabin']=='U', 1, 0)


# create dummy variables for categorical features
pclass_dummies = pd.get_dummies(df['Pclass'], prefix="Pclass")
title_dummies = pd.get_dummies(df['Title'], prefix="Title")
embarked_dummies = pd.get_dummies(df['Embarked'], prefix="Embarked")# concatenate dummy columns with main dataset
df = pd.concat([df, pclass_dummies, title_dummies, embarked_dummies], axis=1)

# drop categorical fields
df.drop(['Age','Pclass', 'Title', 'Cabin', 'Embarked', 'Name', 'Ticket','Parch','SibSp'], axis=1, inplace=True)

# save cleaned data in csv
df.to_csv('titanic_cleaned_train.csv', index=False)
