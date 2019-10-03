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
import ReadRepoHalstead

import Halstead

#DB Connection to the LinesofCode value collection
myclient = MongoClient('localhost',27017)
mydb = myclient["gCodexDB"]
mycol =mydb["Halstead"]


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


def TraverseHalstead(username ,password,repo):

    repoName =repo
    baseUrl='https://raw.githubusercontent.com/'

    g = Github(username, password)
    user =g.get_user()
    # print(user.login)
    # print(repo)
    print("Halstead    "+repo)
    repository=g.get_repo(repo)

    branches=repository.get_branches()

    for br in branches:
        
        Branch=br.name
        headCommit=br.commit.sha
        mycol.insert_one({"Branch":Branch})

        # print("This is  branch commit : " +headCommit)
        commits = repository.get_commits(headCommit)

        for com in commits:

            #CommitTime
            commitDateTime = com.commit.author.date
            print(commitDateTime)
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
                                print("Halstead" + rawPath)
                                ExtFileName = rawPath.split('/')
                                File_Extension =(ExtFileName[len(ExtFileName)-1]).split('.')
                                Halstead.CalculateHalstead(br.name,Date[0],Date[1],r,File_Extension[1],file_content.path,rawPath)
                
                except:

                    pass
    
    
    return    