import os
import glob
import pymongo
import re
import keyword
from pymongo import MongoClient
from bson.json_util import dumps, loads


connection = MongoClient('localhost',27017)
Database = connection.gCodexDB
Compr = Database.cognitiveValues
LOC = Database.LinesOfCode
Halstead = Database.Halstead

def deleteCompr():
    Compr.delete_many({})
    return None

def deleteHalstead():

    Halstead.delete_many({})

    return None

def deleteLinesofCode():

    LOC.delete_many({})

    return None

def returnHalsteaddata():
    
    dataList =dumps(Halstead.find())
    print(dataList)
    return dataList




#Return Lines of Code Data
def returnLOCdata():
    
    
    dataList =dumps(LOC.find())
    print(dataList)
    return dataList
def returnHalsteaddata():
    
    dataList =dumps(Halstead.find())
    print(dataList)
    return dataList





