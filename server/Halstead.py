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
from math import log2
import sys
import os, os.path
#DB Connection to the cognitive value collection

myclient = MongoClient('localhost',27017)
mydb = myclient["gCodexDB"]
mycol =mydb["Halstead"]
newCommitDate ="Null"
newCommitTime ="Null"
DateList = []
TimeList = []

def Halstead(rawPath):
    
    print("Halstead"+rawPath)
    
    operatorsFileName = "opr"
    operators = {}
    operands = {}
   
    with open(operatorsFileName) as f:
        for op in f:
            print(op)
            operators[op.replace('\n','')] = 0
    
   
    


def CalculateHalstead(BranchName,CommitDate,CommitTime,FileExtension,FilePath,RawPath,Repo):

    if (CommitDate in DateList) and (CommitTime in TimeList):

        AttrList = Halstead(RawPath)

        mycol.update_many({"Repository":Repo,
                  "Branches":{'$elemMatch':{
                   "Branch":BranchName ,"Commits.Commit Date":CommitDate,"Commits.Commit Time":CommitTime}}},
               {
                   '$push':{"Branches.$[outer].Commits.$[inner].Contents":{
                                                            "Program Length":AttrList[0],
                                                            "Vocabulary" : AttrList[1],
                                                            "Program Volume":AttrList[2],
                                                            "Program Difficulty":AttrList[3],
                                                            "Program Effort":AttrList[4],
                                                            "Programming Time":AttrList[5],
                                                            "File Extension":FileExtension,
                                                            "Folder Path"   :FilePath
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
        
        AttrList = Halstead(RawPath)
    
        mycol.update_many({"Repository":Repo,
                  "Branches":{'$elemMatch':{
                   "Branch":BranchName ,"Commits.Commit Date":CommitDate,"Commits.Commit Time":CommitTime}}},
               {
                   '$push':{"Branches.$[outer].Commits.$[inner].Contents":{
                                                            "Program Length":AttrList[0],
                                                            "Vocabulary" : AttrList[1],
                                                            "Program Volume":AttrList[2],
                                                            "Program Difficulty":AttrList[3],
                                                            "Program Effort":AttrList[4],
                                                            "Programming Time":AttrList[5],
                                                            "File Extension":FileExtension,
                                                            "Folder Path"   :FilePath
                   }}
               },
               
                array_filters= [  {'outer.Branch':BranchName},
                                  {'inner.Commit Date':CommitDate,
                                  'inner.Commit Time':CommitTime}
                                 ]
               
               )

       
 
