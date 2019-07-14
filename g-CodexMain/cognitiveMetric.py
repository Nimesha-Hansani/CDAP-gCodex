import os
import glob
import pymongo
import re
import keyword
from pymongo import MongoClient
from pymongo import InsertOne
import datetime




#DB Connection to the cognitive value collection

myclient = MongoClient('localhost',27017)
mydb = myclient["gCodexDB"]
mycol =mydb["cognitiveValues"]

#Folder path from Local Machine
folderPath="D:/SLIIT EDU/Test"

#Function for Calculate Cognitive Weight
def CalculateCognitiveWeight(line):
    
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


#Function For Calculate Arithmetic operators
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
    



#Calculate Metric

def CalculateCognitiveMetricValue(filePath):
    LinesOfCode= 0
    TotalDistinctIdentifiers = countIdentifiers(filePath)
    TotalCognitiveWeight = 0
    
    with open(filePath, 'r') as filehandle:
        
        filecontent = filehandle.readlines()
        
        WordContent = str(filecontent)
        SplittedWord = WordContent.split(' ')
        TotalDistinctOperators =CalculateArithmeticOperartors(SplittedWord) + CalculateLogicalOperators(SplittedWord)
        
        for line in filecontent:
            CalculateCognitiveWeight(line)
            TotalCognitiveWeight = TotalCognitiveWeight + CalculateCognitiveWeight(line)
            if line.strip():
               LinesOfCode = LinesOfCode + 1
    
    FinalValue = (TotalCognitiveWeight + TotalDistinctIdentifiers + TotalDistinctOperators)/ LinesOfCode
    print("LinesOfCode"+ str(LinesOfCode))
    
    return [FinalValue ,TotalCognitiveWeight ,TotalDistinctIdentifiers , TotalDistinctIdentifiers ]

#Function for Calculate Identifier
def countIdentifiers(filePath):
    with open(filePath, 'r') as filehandle:
        Identifiers=0
        filecontent = filehandle.readlines()
        for line in filecontent:

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
          print(contentFolderPath)
          mycol.update_one({"Branch": BranchName},
                        {'$push':{"Commits":
                                 {"Commit Date":commitdatetime[0],
                                  "Commit Time":commitdatetime[1]}}
                                }
                     )   

          
          for file in glob.iglob(contentFolderPath+ "/**",recursive=True):
            
            testingPath = file.replace("\\","/")
          
            childPath=testingPath.split(contentFolderPath)
                   

            if os.path.isfile(testingPath):
         
               MetricValue = CalculateCognitiveMetricValue(testingPath)
               file_extension =  os.path.splitext(testingPath)
               file_Type =file_extension[1]
               
               mycol.update({"Branch":BranchName,
                           "Commits":{'$elemMatch':{"Commit Date":commitdatetime[0] ,
                                                    "Commit Time":commitdatetime[1]}}},
                                                     {'$push':{"Commits.$.Contents":
                                                             { "Cognitive Metric Value":MetricValue[0],
                                                               "Cogitive Weight"   :MetricValue[1],
                                                               "Distinct Identifiers" : MetricValue[2],
                                                               "Distinct Operators": MetricValue[3],
                                                               "File Extension":file_extension[1],
                                                               "Folder Path"   :childPath[1]
                                                               }

                                             }}


               )          











                 

  