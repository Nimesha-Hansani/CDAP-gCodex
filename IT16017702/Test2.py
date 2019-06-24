# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 10:21:59 2019

@author: Kushi
"""

from github  import Github
import pandas as pd
import datetime
import requests
import os

# User Authentocation 
g = Github("Kusheni", "Kusheni123#")
user =g.get_user()
repository=g.get_repo("angular/angular")
repoName="angular/angular"

commits = repository.get_commits()
commitAuthors = []
commitemail=[]
commitmessage=[]
commitissues=[]
commitlabels=[]
for com in commits:
    
   
   commitAuthors.append(com.commit.author.name)
   commitemail.append(com.commit.author.email)
   commitmessage.append(com.commit.message)
    

Issues =repository.get_issues()
for isu in Issues:
    commitissues.append(isu.title)
    
    
Labels =repository.get_labels()
for lb in Labels:
     commitlabels.append(lb.name)
     
     
df1=pd.DataFrame(commitAuthors)
df2=pd.DataFrame(commitemail)
df3=pd.DataFrame(commitmessage)
df4=pd.DataFrame(commitissues)
df5=pd.DataFrame(commitlabels)

df1[1] = df2[0].values
df1[2]= df3[0].values

df4


df4.to_csv('issues.csv', index=False)

