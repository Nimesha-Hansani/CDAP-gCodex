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

#Folder path from Local Machine
filePath="D:/CDAP/g-Codex/Repo_Clonning/getRepoContents.py"

#Calculate Metric
commentSymbol = ['//','#','--','<!-- ','!','%',]

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
            
print(fileLineCount)
print(fileBlankLineCount)
print(SourceLinesOfCode)





