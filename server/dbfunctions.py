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

#Retreive cognitiveValus data from Mongo DB
def rtrComprehension (repo):

    dataList = dumps(Compr.find({ 'Repository' : repo}))
    

    return dataList

#Retreive LinesOfCode data from Mongo DB
def rtrLinesofCode (repo):

    dataList = dumps(LOC.find({'Repository':repo}))


#Retreive Halstead data from Mongo DB
def rtrHalstead (repo):

    dataList = dumps(Halstead.find({'Repository':repo}))


#Delete all collection from Mongo DB
def deleteCollections ():

    Compr.delete_many({})
    LOC.delete_many({})
    Halstead.delete_many({})




