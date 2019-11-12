import numpy as np
import pandas as pd
import urllib
from github  import Github
#import os
from collections import Counter
import string
#from nltk import pos_tag
from nltk.corpus import stopwords
# from nltk.tokenize import WhitespaceTokenizer
# from nltk.stem import WordNetLemmatizer
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
#from pprint import pprint

# import pyLDAvis
# import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt

#import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)
#import warnings
#warnings.filterwarnings("ignore",category=DeprecationWarning)
#from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
#from nltk.stem import PorterStemmer


#from nltk import pos_tag
# from nltk.tokenize import WhitespaceTokenizer
# from nltk.stem import WordNetLemmatizer
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# import seaborn as sns
# from matplotlib import*
# from matplotlib.cm import register_cmap
# from scipy import stats
# import seaborn
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

def topCommitters(username,password,repo):
   g = Github(username, password)
   user =g.get_user()
   repository=g.get_repo(repo)
   repoName=repo

   #Get commit data
   commits = repository.get_commits()

   #Get author details
   commitAuthors = []

   for com in commits:

    #print("Commiter :" +com.commit.author.name)
    commitAuthors.append(com.commit.author.name)

    k = Counter(commitAuthors) 
    high = k.most_common(3) 

   

    return high

def issueCloud(username,password,repo):

    g = Github(username, password)
    user =g.get_user()
    repository=g.get_repo(repo)
    repoName=repo

    Issues =repository.get_issues()
    commitIssues = []
    
    for issues in Issues:
        commitIssues.append(issues.title)
    
    df_issues=pd.DataFrame(commitIssues)

    #Get all to lowercase
    #df_issues = df_issues.apply(lambda x: x.lower())

    #Remove punctuations
    df_issues[0]= df_issues[0].apply(lambda x: x.translate(string.punctuation))

    #Remove numbers
    df_issues[0] = df_issues[0].apply(lambda x: x.translate(string.digits))

    # Remove distracting single quotes
    df_issues[0] = df_issues[0].str.replace('object_detection_tutorial', '')

    df_issues[0] = [x.strip('_') for x in df_issues[0]]


    wordcloud = WordCloud(
        background_color = 'black',
        max_words = 200,
        max_font_size = 40, 
        scale = 3,
        random_state = 42
    ).generate(str(df_issues[0]))

    fig = plt.figure(1, figsize = (20, 20))
    plt.axis('off')
    

    plt.imshow(wordcloud)
    plt.savefig('wordcloud.png')
    print ("iMAGE sAVED")
    return None


def defectstatus():
    dataset=pd.read_csv("D:/CDAP/defect_NEW.csv")
    df=pd.DataFrame(dataset)
    print("here")
    #df.defects = df.defects.astype(float)
    x=df.iloc[:,0:8]
    y=df.iloc[:,9]
    

    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.22,random_state=17)

    MultiNB=MultinomialNB()
    MultiNB.fit(x_train,y_train)
    #print(MultiNB)
    #x_test=[1,8,21,3,4,5,6,7,8,1]
    y_pred=MultiNB.predict(x_test)
    print (accuracy_score(y_test,y_pred))

    print("..............................................................................")
    x_test = ([[2.8,3,4,5,6,7,8,99]])

    y_pred=MultiNB.predict(x_test)

    MultiNB=MultinomialNB()
    MultiNB.fit(x_train,y_train)

    if y_pred==0:
        st ='Has Defects'
    else:
        st ='No Defects'

    return st