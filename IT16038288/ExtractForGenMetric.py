from github  import Github
import datetime
import requests
import os

# User Authentocation 
g = Github("dakhz", "dPYAREE@18")
user =g.get_user()
repository=g.get_repo("4CBookClub")
repoName="4CBookClub"
baseUrl='https://raw.githubusercontent.com/'
#Functions
#Get all the repository comments
#Filter required files    
def Avoid_Files(filePath ,rpName ,bUrl,ck):
   ExtensionList =['asc','txt','log','cnf','cfg','conf','bak','bk','md','R','css','csv','html','ihtml',
                    'htm','xhtml','xht','maff','log','xsl','png','gif','gz','r','zip','xml','BULD','sql']

   pExList=['py','c','class','cpp','cxx','CXX','java','js','jsp','php','php3','vbs','cc','h','pl']
   fileformat =filePath.split(".")[1]

   if fileformat in pExList:
      rawUrl = bUrl + rpName +'/'+ ck +'/'+filePath
     
      return rawUrl
   elif fileformat in ExtensionList:
      return  None
   else:
      return  None
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
       
        #Commit Year and Month
        commitMonth = commitDateTime.month

        #Get trees for each commit
        trees = repository.get_git_tree(brCom.sha).tree
        commitKey=brCom.sha
        for tr in trees:
         try:
            treeContent=repository.get_contents(tr.path)
              
            while len(treeContent)> 1:
                  file_content=treeContent.pop(0)
                   
                  if(file_content.type == "dir"):
                    
                     dirPath= 'F:/4th year Research/1-The Project/50%/Test'
                     folderPath=(dirPath+'/'+Branch+'/'+TimeStampStr+'/'+file_content.path)
                     parentFolderPath=(dirPath+'/'+Branch+'/'+TimeStampStr+'/')
                     if (os.path.exists(dirPath)):
                        os.makedirs(folderPath)
                       
                    
                     treeContent.extend(repository.get_contents(file_content.path))

                  else:
                     
                     
                     rawPath = Avoid_Files(file_content.path ,repoName ,baseUrl,commitKey)
                     if(rawPath != None):
                        r = requests.get(rawPath)
                        f = open(parentFolderPath+file_content.path ,"wb").write('r.content')
                        
                       
         except :
            pass     
            

          
        
        
