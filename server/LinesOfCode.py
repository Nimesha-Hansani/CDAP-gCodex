import os
import glob
import pymongo
import re
import keyword
from pymongo import MongoClient
from pymongo import InsertOne
import datetime
import urllib.request
import requests
import sys
import os, os.path
#DB Connection to the cognitive value collection

myclient = MongoClient('localhost',27017)
mydb = myclient["gCodexDB"]
mycol =mydb["LinesOfCode"]
newCommitDate ="Null"
newCommitTime ="Null"

def LinesOfCode(rawPath):

    commentSymbol = ['//','#','--','<!-- ','!','%',]
    fileLineCount = 0
    fileBlankLineCount = 0
    fileCommentLineCount = 0
   
    #r = requests.get(rawPath)
    #fileContent = r.content.readlines()
    get_page = urllib.request.urlopen(rawPath)
    get_ver = get_page.readlines()

    for line in get_ver:
       
        fileLineCount += 1
        lineWithoutWhitespace = str(line.strip(), 'utf-8')
        
        if not  lineWithoutWhitespace:
            fileBlankLineCount += 1
            
        elif lineWithoutWhitespace.startswith(tuple(commentSymbol)):
            fileCommentLineCount += 1
            
    SourceLinesOfCode = fileLineCount - fileBlankLineCount -fileCommentLineCount
    print(SourceLinesOfCode,fileCommentLineCount,fileLineCount)
    return [SourceLinesOfCode,fileCommentLineCount,fileLineCount]
    








def CalculateLinesofCode(BranchName,CommitDate,CommitTime,R,Extension,filePath,Raw):
    global newCommitDate
    global newCommitTime
 
    if(newCommitDate != CommitDate) or ( newCommitTime != CommitTime):

    
        mycol.update_one({"Branch":BranchName},
                           {'$push':{"Commits":
                                    {"Commit Date":CommitDate,
                                     "Commit Time":CommitTime}}
                                    }
                     )
        newCommitDate = CommitDate
        newCommitTime = CommitTime
        
        AttrList = LinesOfCode(Raw)
    
        mycol.update({"Branch":BranchName,
                             "Commits":{'$elemMatch':{"Commit Date":CommitDate ,
                                                      "Commit Time":CommitTime}}},
                                                      {'$push':{"Commits.$.Contents":
                                                               {"Source Lines of Code":AttrList[0],
                                                                "Comment Lines" : AttrList[1],
                                                                "File Lines of Code":AttrList[2],
                                                                "File Extension":Extension,
                                                                "Folder Path"   :filePath
                                                               }

                                                }}


               )  


    else :

       
        AttrList = LinesOfCode(Raw)
        mycol.update({"Branch":BranchName,
                             "Commits":{'$elemMatch':{"Commit Date":CommitDate ,
                                                      "Commit Time":CommitTime}}},
                                                      {'$push':{"Commits.$.Contents":
                                                               {"Source Lines of Code":AttrList[0],
                                                                "Comment Lines" : AttrList[1],
                                                                "File Lines of Code":AttrList[2],
                                                                "File Extension":Extension,
                                                                "Folder Path"   :filePath
                                                               }

                                                }}


               )  
    