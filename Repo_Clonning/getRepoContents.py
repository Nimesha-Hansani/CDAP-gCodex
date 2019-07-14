from github  import Github
import datetime
import os
import requests
from pathlib import Path

# User Authentocation 
g = Github("Nimesha-Hansani", "19950525hansani")
user =g.get_user()


#Repository Name
repository=g.get_repo("laveesha/Data-Minin-App")
repoName="laveesha/Data-Minin-App"
baseUrl='https://raw.githubusercontent.com/'

#Local Path which repository contents going to be stored


LocalDirPath="D:/Test2"


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


#Get All Branches in Repository and traversing through it 
branches=repository.get_branches()
for br in branches:
    Branch=br.name
    headCommit = br.commit.sha
    branchCommits=repository.get_commits(headCommit)
    
    #traversing through every commit
    for brCom in branchCommits:

        singleCommit = repository.get_commit(brCom.sha)

        #CommitTime
        commitDateTime = singleCommit.commit.author.date
        TimeStampStr= commitDateTime.strftime("%Y-%m-%d %H-%M-%S")
        print(commitDateTime)
        #Defining Folder Path to be created for commit history
        
        CommitsFolderPath=(LocalDirPath+'/'+Branch+'/'+TimeStampStr)
        
        #Commit Year and Month
        commitMonth = commitDateTime.month
         
        #Commit Key  
        commitKey=brCom.sha

        #Get trees for each commit
        trees = repository.get_git_tree(brCom.sha).tree
        
        for tr in trees:
         
         treeContent=repository.get_contents(tr.path)
         print(treeContent)
         try:
               if(treeContent.type == "file"):
                  if (os.path.exists(CommitsFolderPath)):
                     rawPath = Avoid_Files(treeContent.path,repoName,baseUrl,commitKey)
                     r = requests.get(rawPath)
                     f = open(CommitsFolderPath+'/'+treeContent.path ,"wb").write(r.content)
                     
                  else:
                     os.makedirs(CommitsFolderPath)
                     rawPath = Avoid_Files(treeContent.path,repoName,baseUrl,commitKey)
                  
                     r = requests.get(rawPath)
                     f = open(CommitsFolderPath+'/'+treeContent.path ,"wb").write(r.content)
                     
         except:
               
               try:
                  while len(treeContent)>1:
                        file_content=treeContent.pop(0)
                 
                        file_content_folder_path =CommitsFolderPath+'/'+file_content.path
                        parentPath= Path(file_content_folder_path).parent
                        if (os.path.exists(parentPath)):
                           rawPath=Avoid_Files(file_content.path,repoName,baseUrl,commitKey)
                           if(rawPath != None):
                              r = requests.get(rawPath)
                              f = open(CommitsFolderPath+'/'+file_content.path,"wb").write(r.content)
                        
                        else:
                           os.makedirs(parentPath)
                           rawPath=Avoid_Files(file_content.path,repoName,baseUrl,commitKey)
                           if(rawPath != None):
                              r = requests.get(rawPath)
               
                              f = open(CommitsFolderPath+'/'+file_content.path,"wb").write(r.content)
               except:
                     continue
                
                    
                 

         finally:
                  pass
            
            
      

          
        
        
