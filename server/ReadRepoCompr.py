from github  import Github
import urllib.request
import requests

import datetime
import os
import glob
import pymongo
import re
import keyword
from pymongo import MongoClient
from pymongo import InsertOne
import datetime
import sys
import os, os.path
import LinesOfCode
import Comprehension


#DB Connection to the cognitive value collection
myclient = MongoClient('localhost',27017)
mydb = myclient["gCodexDB"]
mycol =mydb["cognitiveValues"]


#Filter required files   
def Avoid_Files(filePath ,rpName ,bUrl,ck):
   ExtensionList =['asc','txt','log','cnf','cfg','conf','bak','bk','md','R','css','csv','html','ihtml',
                    'htm','xhtml','xht','maff','log','xsl','png','gif','gz','r','zip','xml','BULD','sql']

   pExList=['py','c','class','cpp','cxx','CXX','java','js','jsp','php','php3','vbs','cc','h','pl']
   try :
      fileformat =filePath.split(".")[1]
      if fileformat in pExList:
          rawUrl = bUrl + rpName +'/'+ ck +'/'+filePath
          
          return rawUrl
      elif fileformat in ExtensionList:
          return  None
      else:
          return  None
   except:
      pass


def TraverseCompr(username ,password,repo):

    repoName =repo
    baseUrl='https://raw.githubusercontent.com/'

    g = Github(username, password)
    user =g.get_user()
    # print(user.login)
    # print(repo)
    print("Com"+repo)
    repository=g.get_repo(repo)
    mycol.insert_one({"Repository":repo})
    branches=repository.get_branches()
    
    for br in branches:
        
        Branch=br.name
        headCommit=br.commit.sha
        mycol.update_one({"Repository": repo},
                           {'$push':{"Branches":
                                    {"Branch":br.name
                                     }}
                                    }
                     )

        # print("This is  branch commit : " +headCommit)
        commits = repository.get_commits(headCommit)

        for com in commits:

            #CommitTime
            commitDateTime = com.commit.author.date
            TimeStampStr= commitDateTime.strftime("%Y-%m-%d %H-%M-%S")
            Date = TimeStampStr.split(' ')
            commitKey = com.sha
            tree=repository.get_git_tree(com.sha).tree

            for tr in tree:

                try:
                    # print("Tree of the Commit :"+ tr.sha + "Path :" + tr.path)
                    treeContent=repository.get_contents(tr.path)
                    # print(treeContent)
                    while len(treeContent)> 1:
                        file_content=treeContent.pop(0)

                        if file_content.type =="dir":
                            treeContent.extend(repository.get_contents(file_content.path))

                        else :
                
                            rawPath=Avoid_Files(file_content.path,repoName,baseUrl,commitKey)
                            if(rawPath != None):
                                r = requests.get(rawPath)
                                print("Compreh"+rawPath)
                                ExtFileName = rawPath.split('/')
                                File_Extension =(ExtFileName[len(ExtFileName)-1]).split('.')
                                Comprehension.CalculateComprehension(br.name,Date[0],Date[1],r,File_Extension[1],file_content.path,rawPath)
                
                except:

                    pass
    return
    