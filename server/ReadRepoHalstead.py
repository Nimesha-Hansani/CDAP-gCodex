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

    print("Halstead for "+repo)
    repoName =repo
    baseUrl='https://raw.githubusercontent.com/'

    g = Github(username, password)
    repository=g.get_repo(repo)
    
    mycol.insert_one({"Repository":repo})
    user =g.get_user()
    branches=repository.get_branches()

    for br in branches:
        
        Branch=br.name
        headCommit=br.commit.sha
        mycol.update({"Repository":repository.full_name},
                    {'$push':{"Branches":{
                              "Branch":Branch
                    }}})
        
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
                    if(tr.type == "tree"):
                        treeContent=repository.get_contents(tr.path)
                        
                        # print(treeContent)
                        while len(treeContent)> 0:
                            file_content=treeContent.pop(0)

                            if file_content.type =="dir":
                                    treeContent.extend(repository.get_contents(file_content.path))
                            else:
                                    
                                    rawPath=Avoid_Files(file_content.path,repoName,baseUrl,commitKey)
                                    if(rawPath != None):
                                     
                                        r = requests.get(rawPath)
                               
                                        ExtFileName = rawPath.split('/')
                                        File_Extension =(ExtFileName[len(ExtFileName)-1]).split('.')
                                        Halstead. CalculateHalstead(Branch,Date[0],Date[1],File_Extension[1],file_content.path,rawPath,repository.full_name)
                    
                    elif (tr.type == "blob"):
                        
                        
                        rawPath=Avoid_Files(tr.path,repoName,baseUrl,commitKey)

                        if(rawPath != None):
                                        
                           
                            r = requests.get(rawPath)
                               
                            ExtFileName = rawPath.split('/')
                            File_Extension =(ExtFileName[len(ExtFileName)-1]).split('.')
                            Halstead.CalculateHalstead(Branch,Date[0],Date[1],File_Extension[1],tr.path,rawPath,repository.full_name)
                    else:
                        pass
               except:

                   pass
    
    
    return    