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

   
    
import os
import glob
import pymongo
import re
import keyword
from pymongo import MongoClient
from pymongo import InsertOne
import datetime
import sys
import os
from math import log2
import sys
import os, os.path
#DB Connection to the cognitive value collection

myclient = MongoClient('localhost',27017)
mydb = myclient["gCodexDB"]
mycol =mydb["LinesOfCode"]

#Folder path from Local Machine
folderPath="D:/SLIIT EDU/Test"

#Calculate Metric
filePath='D:/CDAP/g-Codex/Repo_Clonning/getRepoContents.py'
    
operatorsFileName = "IT16038288/operators"

operators = {}
operands = {}

with open(operatorsFileName) as f:
    for op in f:
        operators[op.replace('\n','')] = 0

    isAllowed = True

with open(filePath,'r') as f:
    for line in f:
        line = line.strip("\n").strip(' ')

        if(line.startswith("/*")):
            isAllowed = False
       
        if((not line.startswith("//")) and isAllowed == True and (not line.startswith('#'))):
            for key in operators.keys():
                operators[key] = operators[key] + line.count(key)
                line = line.replace(key,' ')
                for key in line.split():
                    if key in operands:
                        operands[key] = operands[key] + 1
                    else:
                        operands[key] = 1

            if(line.endswith("*/")):
                isAllowed = True


    n1, N1, n2, N2 = 0, 0, 0, 0

    #print("OPERATORS:\n")
    for key in operators:
        if(operators[key] > 0):
            if(key not in ")}]"):
                n1, N1 = n1 + 1, N1 + operators[key]
                #print("{} = {}".format(key, operators[key]))

    #print("\nOPERANDS\n")
    for key in operands.keys():
        if(operands[key] > 0):
            n2, N2 = n2 + 1, N2 + operands[key]
            #print("{} = {}".format(key, operands[key]))

    N = N1+N2
    n = n1+n2
    V = (N1 + N2) * log2(n1 + n2)
    D =  n1 * N2 / 2 / n2
    E = D * V
    T =  E / (18)

    val = {"N": N1 + N2, "n": n1 + n2, "V": (N1 + N2) * log2(n1 + n2), "D": n1 * N2 / 2 / n2}
    val['E'] = val['D'] * val['V']
    val['L'] = val['V'] / val['D'] / val['D']
    val['I'] = val['V'] / val['D']
    val['T'] = val['E'] / (18)
    val['N^'] = n1 * log2(n1) + n2 * log2(n2)
    val['L^'] = 2 * n2 / N2 / n1

    unit = {'V': 'bits', 'T': 'seconds'}
    name = {'N':'Halstead Program Length', 'n':'Halstead Vocabulary', 'V':'Program Volume', 'D':'Program Difficulty', 'E': 'Programming Effort', 'L':'Language level', 'I':'Intelligence Content', 'T':'Programming time','N^':'Estimated program length', 'L^':'Estimated language level'}

    print("\nThe various values are: ")
    for key in val.keys():
        print("{} ({}) = {} {}".format(key,name[key], val[key], unit[key] if key in unit else ''))






