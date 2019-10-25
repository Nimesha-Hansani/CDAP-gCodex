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
DateList = []
TimeList = []



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
    # print(SourceLinesOfCode,fileCommentLineCount,fileLineCount)
    return [SourceLinesOfCode,fileCommentLineCount,fileLineCount]

def CalculateLinesofCode(BranchName,CommitDate,CommitTime,FileExtension,FilePath,RawPath,Repo,LocLink):
    print(FilePath) 
    if (CommitDate in DateList) and (CommitTime in TimeList):

        AttrList = LinesOfCode(RawPath)

        mycol.update_many({"Repository":Repo,
                  "Branches":{'$elemMatch':{
                   "Branch":BranchName ,"Commits.Commit Date":CommitDate,"Commits.Commit Time":CommitTime}}},
               {
                   '$push':{"Branches.$[outer].Commits.$[inner].Contents":{
                                                            "Source Lines of Code":AttrList[0],
                                                            "Comment Lines"    :AttrList[1],
                                                            "File Lines of Code" : AttrList[2],
                                                            "File Extension":FileExtension,
                                                            "Folder Path"   :FilePath,
                                                            "Git_Web_Link"  :LocLink
                   }}
               },
               
                array_filters= [  {'outer.Branch':BranchName},
                                  {'inner.Commit Date':CommitDate,
                                  'inner.Commit Time':CommitTime}
                                 ]
               
               )

    else :

        DateList.append(CommitDate)
        TimeList.append(CommitTime)

        mycol.update_many({"Repository":Repo,
                          "Branches":{'$elemMatch':{"Branch":BranchName}}},
                          {'$push':{"Branches.$.Commits":{
                                  "Commit Date":CommitDate,
                                  "Commit Time":CommitTime
                           }}})
        
        AttrList = LinesOfCode(RawPath)
    
        mycol.update_many({"Repository":Repo,
                  "Branches":{'$elemMatch':{
                   "Branch":BranchName ,"Commits.Commit Date":CommitDate,"Commits.Commit Time":CommitTime}}},
               {
                   '$push':{"Branches.$[outer].Commits.$[inner].Contents":{
                                                            "Source Lines of Code":AttrList[0],
                                                            "Comment Lines"    :AttrList[1],
                                                            "File Lines of Code" : AttrList[2],
                                                            "File Extension":FileExtension,
                                                            "Folder Path"   :FilePath,
                                                            "Git_Web_Link"  :LocLink
                   }}
               },
               
                array_filters= [  {'outer.Branch':BranchName},
                                  {'inner.Commit Date':CommitDate,
                                  'inner.Commit Time':CommitTime}
                                 ]
               
               )

       