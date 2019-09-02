import urllib.request
import os
import glob
import pymongo
import re
import keyword
from pymongo import MongoClient
from pymongo import InsertOne
import datetime

myclient = MongoClient('localhost',27017)
mydb = myclient["gCodexDB"]
mycol =mydb["cognitiveValues"]
newCommitDate ="Null"
newCommitTime ="Null"

#Function for Calculate Cognitive Weight
def CalculateCognitiveWeight(line):
    line = str(line.strip(),'utf-8')
    cognitiveWeight = 0
    res = re.findall(r'[a-zA-Z]+', line)

    for w in res:
      if (w == "if") or  (w == "elif") or (w == "elseif") or (w == "else") or  (w=="then") or (w == "case"):
        cognitiveWeight = cognitiveWeight + 2
      elif (w == "for") or (w == "while") or (w == "do") or (w == "repeat") or (w == "until"):
        cognitiveWeight = cognitiveWeight + 3 
      elif (w == "continue"):
        cognitiveWeight = cognitiveWeight + 1

    return cognitiveWeight

#Function For Calculate Arithmetic Operators
def CalculateArithmeticOperartors(line):
    c1 = 0
    if '+' in line:
        c1= c1 + 1
    if '-' in line:
        c1 = c1 + 1
    if '*' in line:
        c1 = c1 + 1
    if '/'in line:
        c1 = c1 + 1
    if '%' in line:
        c1 = c1 + 1
    if '++' in line:
        c1 = c1 + 1
    if '+=' in line:
        c1 = c1 + 1
    if '-=' in line:
        c1 = c1 + 1
    if '*-' in line:
        c1 = c1 + 1    
    if '/=' in line:
        c1 = c1 + 1
    if '%=' in line:
        c1 = c1 + 1
    if '--' in line:
         c1 = c1 + 1

      
    return c1

#Function for  Calculate Logical Operators
def CalculateLogicalOperators(line):
    c2 = 0
    if '!' in line:
      c2 = c2 + 1
    if '!=' in line:
      c2 = c2 + 1
    if '<' in line:
      c2 = c2 + 1
    if '<=' in line:
      c2 = c2 + 1
    if '>' in line :
       c2 = c2 + 1
    if '>=' in line:
       c2 = c2 + 1
    if '&&' in line:
       c2 = c2 + 1
    if '||' in line:
        c2 = c2 + 1
    if '==' in line:
        c2 = c2 + 1
    if 'or' in line:
        c2 = c2 + 1
    if 'and' in line:
        c2 = c2 + 1
    
    return c2      
    

#Count pass distinct identifier
def countIdentifiers(filePath):
        
        get_page = urllib.request.urlopen(filePath)
        filecontent = get_page.readlines()
        Identifiers=0
        
        for line in filecontent:
            line = str(line.strip(),'utf-8')
            wordList = []
            commonkeywords=['for' ,'do','while','if','else','elseif','elif','switch','case','continue','pass','try','catch',
                        'continue','int','double','float','finally' ,'from','return','null']
            keywords1 = keyword.kwlist
            keywordsJava= ['import' ,'from','abstract','boolean','break','byte','case','catch','char','class','continue','default','final','private',
                        'protected','throws','void']
            #keywordJavaScript = []
            #keywordC=[]
            res = re.findall(r'[a-zA-Z]+', line)
            for w in res:
                if (w not in keywords1) and (w not in keywordsJava) and (w not in commonkeywords):
                    wordList.append(w)
        
            
        Identifiers = set (wordList)
        return len(Identifiers)

#Calculate ComprehensionaMetrincValues
def CalculateComprehensionMetricValue(RawPath):
    
    
    LinesOfCode= 0
    TotalDistinctIdentifiers = countIdentifiers(RawPath)
    TotalCognitiveWeight = 0
    
    get_page = urllib.request.urlopen(RawPath)
    get_ver = get_page.readlines()

    WordContent = str(get_ver)
    # print(WordContent)
    SplittedWord = WordContent.split(' ')
    TotalDistinctOperators =CalculateArithmeticOperartors(SplittedWord) + CalculateLogicalOperators(SplittedWord)
    
    for line in get_ver:
            CalculateCognitiveWeight(line)
            TotalCognitiveWeight = TotalCognitiveWeight + CalculateCognitiveWeight(line)
            if line.strip():
               LinesOfCode = LinesOfCode + 1


    FinalValue = (TotalCognitiveWeight + TotalDistinctIdentifiers + TotalDistinctOperators)/ LinesOfCode
    print("LinesOfCode"+ str(LinesOfCode))
    print(TotalCognitiveWeight)
    return [FinalValue ,TotalCognitiveWeight ,TotalDistinctIdentifiers , TotalDistinctIdentifiers ]



def CalculateComprehension(BranchName,CommitDate,CommitTime,R,Extension,filePath,Raw):
    
    global newCommitDate
    global newCommitTime
    if(newCommitDate != CommitDate) or ( newCommitTime!= CommitTime):

    
        mycol.update_one({"Branch": BranchName},
                           {'$push':{"Commits":
                                    {"Commit Date":CommitDate,
                                     "Commit Time":CommitTime}}
                                    }
                     )
        newCommitDate = CommitDate
        newCommitTime = CommitTime
        print(newCommitDate)
        AttrList = CalculateComprehensionMetricValue(Raw)
        print(AttrList[0])
        mycol.update({"Branch":BranchName,
                             "Commits":{'$elemMatch':{"Commit Date":CommitDate ,
                                                      "Commit Time":CommitTime}}},
                                                      {'$push':{"Commits.$.Contents":
                                                               { 
                                                                "Cognitive Metric Value":AttrList[0],
                                                                "Cogitive Weight"   :AttrList[1],
                                                                "Distinct Identifiers" : AttrList[2],
                                                                "Distinct Operators": AttrList[3],
                                                                "File Extension":Extension,
                                                                "Folder Path"   :filePath
                                                               }

                                                }}
                    )



    else :

       
        AttrList = CalculateComprehensionMetricValue(Raw)
        print(AttrList[0])
        mycol.update({"Branch":BranchName,
                             "Commits":{'$elemMatch':{"Commit Date":CommitDate ,
                                                      "Commit Time":CommitTime}}},
                                                      {'$push':{"Commits.$.Contents":
                                                               {
                                                                "Cognitive Metric Value":AttrList[0],
                                                                "Cogitive Weight"   :AttrList[1],
                                                                "Distinct Identifiers" : AttrList[2],
                                                                "Distinct Operators": AttrList[3],
                                                                "File Extension":Extension,
                                                                "Folder Path"   :filePath
                                                               }

                                                }}
                                )

    
   
        
