import os
import glob
import pymongo
from pymongo import MongoClient
from pymongo import InsertOne


myclient = MongoClient('localhost',27017)
mydb = myclient["gCodexDB"]
mycol =mydb["LinesOfCode"]

folderPath="D:/SLIIT EDU/Test"

def CalculateLinesOfCode(filePath):

   LinesOfCode = 0
   with open(filePath, 'r') as filehandle:
     filecontent = filehandle.readlines()
     for line in filecontent:
         if not line.strip():
            pass

         else :
             LinesOfCode =LinesOfCode + 1
   print(LinesOfCode)
   return LinesOfCode

    

for file in os.listdir(folderPath):
   BranchName = file
   print("Branch :" + BranchName)

   #Insert a Document
   mycol.insert({"Branch":BranchName })
                 
   if os.path.isdir(folderPath+'/'+BranchName):
      commitFoldersPath = folderPath+'/'+BranchName 
      for file in  os.listdir(commitFoldersPath):
        
        contentFolderPath =commitFoldersPath+'/'+file
        print("Content Folder Path :-" +contentFolderPath)
        commitdatetime =str(file).split(' ')
        print("Commit Date :" + str(commitdatetime[0]))
        print("Commit Time :" + commitdatetime[1])
        mycol.update ( {"Branch": BranchName},
                       {'$push' :{
                                  "Commits":{
                                              "Commit Date":commitdatetime[0],
                                              "Commit Time":commitdatetime[1]
                                  }
                                 }
                        }
                     )
                 
    
        for file in glob.iglob(contentFolderPath+"/**",recursive=True):
            testingPath = file.replace("\\","/")
            

            if os.path.isfile(testingPath):
               print(testingPath)
               CountedLOC = CalculateLinesOfCode(testingPath)
               file_extension =  os.path.splitext(testingPath)
               file_Type =file_extension[1]
               print(file_Type)
               mycol.update({"Branch":BranchName,
                             "Commits":{'$elemMatch':{"Commit Date":commitdatetime[0] ,
                                                      "Commit Time":commitdatetime[1]}}},
                                                      {'$push':{"Commits.$.Contents":
                                                               {"SLOC":CountedLOC,
                                                                "File Extension":file_extension[1],
                                                                "Folder Path"   :testingPath
                                                               }

                                                }}


               )

             
               
               
               