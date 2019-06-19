from github  import Github
import datetime
import requests
import os

# User Authentocation 
g = Github("Nimesha-Hansani", "19950525hansani")
user =g.get_user()
repository=g.get_repo("tensorflow/tensorflow")
repoName="tensorflow/tensorflow"


commits = repository.get_commits()
#for com in commits:
    
   # print("Commiter :" +com.commit.author.name)
   # print("Commiter :" +com.commit.author.email)
   #print(com.commit.message)
   # print("------------------------------")


#Labels =repository.get_labels()
#for lb in Labels:
    #print(lb.name)

Issues =repository.get_issues()
for isu in Issues:
    print(isu.title)
