# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 18:32:48 2019

@author: Kushi
"""

from github  import Github
import datetime
import requests
import os
import pandas as pd
from collections import Counter
import string
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# User Authentocation 
g = Github("Kusheni", "Kusheni123#")
user =g.get_user()
repository=g.get_repo("tensorflow/tensorflow")
repoName="tensorflow/tensorflow"

#Get commit data
commits = repository.get_commits()

#Get author details
commitAuthors = []

for com in commits:

   #print("Commiter :" +com.commit.author.name)
   commitAuthors.append(com.commit.author.name)
   
#print(commitAuthors)

print("......................................................")
print("Committers") 
print(set(commitAuthors))

df=pd.DataFrame(commitAuthors)
#df["df_clean"] = df[0].apply(lambda x: clean_text(x))

# clean text data


def clean_text(text):
    # lower text
    text = text.lower()
    # tokenize text and remove puncutation
    text = [word.strip(string.punctuation) for word in text.split(" ")]
    # remove words that contain numbers
    text = [word for word in text if not any(c.isdigit() for c in word)]
    # remove stop words
    stop = stopwords.words('english')
    text = [x for x in text if x not in stop]
    # remove empty tokens
    text = [t for t in text if len(t) > 0]
    # pos tag text
    pos_tags = pos_tag(text)
    # lemmatize text
    text = [WordNetLemmatizer().lemmatize(t[0], get_wordnet_pos(t[1])) for t in pos_tags]
    # remove words with only one letter
    text = [t for t in text if len(t) > 1]
    # join all
    text = " ".join(text)
    return(text)



def most_frequent(commitAuthors): 
    return max(set(commitAuthors), key = commitAuthors.count) 
  
print("......................................................")
print("Most Contributed Committer : ") 

 
k = Counter(commitAuthors) 
high = k.most_common(3) 
print(high)

for i in high: 
    print(i[0])
    
print("......................................................")
print("Labels")
print("......................................................")
Labels =repository.get_labels()
for lb in Labels:
    print(lb.name)
    
print("......................................................")

print("Issues")
Issues =repository.get_issues()
for isu in Issues:
    print(isu.title)
    
commitIssues = []
for issues in Issues:

   print("Issues:" +(issues.title))
   commitIssues.append(issues.title)
   
   
print(set(commitIssues))

df_issues=pd.DataFrame(commitIssues)
# clean text data
#df_issues["df_issues_clean"] = df_issues[0].apply(lambda x: clean_text(x))


# wordcloud function

from wordcloud import WordCloud
import matplotlib.pyplot as plt

def show_wordcloud(data, title = None):
    wordcloud = WordCloud(
        background_color = 'white',
        max_words = 200,
        max_font_size = 40, 
        scale = 3,
        random_state = 42
    ).generate(str(data))

    fig = plt.figure(1, figsize = (20, 20))
    plt.axis('off')
    if title: 
        fig.suptitle(title, fontsize = 20)
        fig.subplots_adjust(top = 2.3)

    plt.imshow(wordcloud)
    plt.show()
    
# print wordcloud
show_wordcloud(df_issues[0])  

print("......................................................")
print("Labels")
Labels =repository.get_labels()
for lb in Labels:
    print(lb.name)

commitLabels = []
for issues in Issues:

   print("Issues:" +(issues.title))
   commitLabels.append(issues.title)
   
   
print(set(commitLabels))

df_labels=pd.DataFrame(commitLabels)
# clean text data

#df_labels["df_labels_clean"] = df_labels[0].apply(lambda x: clean_text(x))

show_wordcloud(df_labels[0])  



