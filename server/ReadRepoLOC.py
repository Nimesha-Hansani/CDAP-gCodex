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


#DB Connection to the LinesofCode value collection
myclient = MongoClient('localhost',27017)
mydb = myclient["gCodexDB"]
mycol =mydb["LinesOfCode"]

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






def TraverseLOC(username ,password,repo):

    print("LOC for" + repo)
    repoName =repo
    baseUrl='https://raw.githubusercontent.com/'
    Base_Link = 'https://github.com/'


    g = Github(username, password)
    repository=g.get_repo(repo)
    
    mycol.insert_one({"Repository":repo})
    url_Link1 = Base_Link + repo +'/blob/'
    branches=repository.get_branches()
    for br in branches:
        
        Branch=br.name
        headCommit=br.commit.sha
        mycol.update({"Repository":repository.full_name},
                    {'$push':{"Branches":{
                              "Branch":Branch
                    }}})
        print(Branch+"Inserted")
        commits = repository.get_commits(headCommit)
        
        for com in commits:

            #CommitTime
            commitDateTime = com.commit.author.date
            url_Link2 = url_Link1 + com.sha +'/'
            TimeStampStr= commitDateTime.strftime("%Y-%m-%d %H-%M-%S")
            Date = TimeStampStr.split(' ')
            commitKey = com.sha
            tree=repository.get_git_tree(com.sha).tree
    
            
            for tr in tree:

                try:
               
                    if (tr.type =="tree"):
                        
                        treeContent=repository.get_contents(tr.path)
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
                                    SC_Link = url_Link2 +file_content.path
                                    
                                    LinesOfCode.CalculateLinesofCode(Branch,Date[0],Date[1],File_Extension[1],file_content.path,rawPath,repository.full_name,SC_Link)
                    
                    elif (tr.type == "blob"):

    

                        # print(tr.path)
                        rawPath=Avoid_Files(tr.path,repoName,baseUrl,commitKey)

                        if(rawPath != None):
                                        
                            # print(rawPath)
                            r = requests.get(rawPath)
                               
                            ExtFileName = rawPath.split('/')
                            File_Extension =(ExtFileName[len(ExtFileName)-1]).split('.')
                            SC_Link = url_Link2 +tr.path
                            
                            LinesOfCode.CalculateLinesofCode(Branch,Date[0],Date[1],File_Extension[1],tr.path,rawPath,repository.full_name,SC_Link)
                    
                    else:

                        pass
                
                    



                

                except:
                        pass
                
                      
                   
                    
    return