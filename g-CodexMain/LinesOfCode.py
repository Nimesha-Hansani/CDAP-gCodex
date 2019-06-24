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
#DB Connection to the cognitive value collection

myclient = MongoClient('localhost',27017)
mydb = myclient["gCodexDB"]
mycol =mydb["LinesOfCode"]

#Folder path from Local Machine
folderPath="D:/SLIIT EDU/Test"

#Calculate Metric
commentSymbol = ['//','#','--','<!-- ','!','%',]
def CalculateLinesOfCode (filePath):
    fileLineCount = 0
    fileBlankLineCount = 0
    fileCommentLineCount = 0
   
   
    
    with open(filePath,'r') as filehandle:
            filecontent = filehandle.readlines()
            

            for line in filecontent:
               
                fileLineCount += 1

                lineWithoutWhitespace = line.strip()
                if not lineWithoutWhitespace:
                    fileBlankLineCount += 1
                elif lineWithoutWhitespace.startswith(tuple(commentSymbol)):
                     fileCommentLineCount += 1
            
            SourceLinesOfCode = fileLineCount - fileBlankLineCount -fileCommentLineCount
            
    return [fileLineCount , fileCommentLineCount , SourceLinesOfCode]









for file in os.listdir(folderPath):
   BranchName = file
   print("Branch :" + BranchName)

   #Insert a Document
   mycol.insert_one({"Branch":BranchName })

   if os.path.isdir(folderPath+'/'+BranchName):
      commitFoldersPath = folderPath+'/'+BranchName 
      for file in  os.listdir(commitFoldersPath):
          contentFolderPath =commitFoldersPath+'/'+file
          commitdatetime =str(file).split(' ') 
        
          mycol.update_one({"Branch": BranchName},
                           {'$push':{"Commits":
                                    {"Commit Date":commitdatetime[0],
                                     "Commit Time":commitdatetime[1]}}
                                    }
                     )    

          
          for file in glob.iglob(contentFolderPath+"/**",recursive=True):
            testingPath = file.replace("\\","/")
            

            if os.path.isfile(testingPath):
         
               MetricValue = CalculateLinesOfCode(testingPath)
               
               file_extension =  os.path.splitext(testingPath)
               file_Type =file_extension[1]
               
               mycol.update({"Branch":BranchName,
                             "Commits":{'$elemMatch':{"Commit Date":commitdatetime[0] ,
                                                      "Commit Time":commitdatetime[1]}}},
                                                      {'$push':{"Commits.$.Contents":
                                                               {"Source Lines of Code":MetricValue[2],
                                                                "Comment Lines" : MetricValue[2],
                                                                "File Lines of Code":MetricValue[0],
                                                                "File Extension":file_extension[1],
                                                                "Folder Path"   :testingPath
                                                               }

                                                }}


               )          





