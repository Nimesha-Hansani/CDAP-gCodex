import os
import glob
import pymongo
import re
import keyword
from pymongo import MongoClient
from nested_lookup import nested_lookup
import pandas as pd 
import dateutil
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from stationarizer import simple_auto_stationarize
import json


def forcastingComprehension(repo):
    
    connection = MongoClient('localhost',27017)
    Database = connection.gCodexDB
    data =Database.LinesOfCode
    New_df = pd.DataFrame(columns =['Date','Time','Value'])
    
    dataList =data.find({'Repository':repo})
    


    for data in dataList:
        try:
            for branch in data['Branches']:
        
                for commit in branch['Commits']:
           
                    for content in commit['Contents']:
                        RowDataSet = {'Date':commit['Commit Date'],'Time':commit['Commit Time'],'Value':content['Source Lines of Code']}
                        New_df = New_df.append(RowDataSet,ignore_index=True)
            
        except:
        
                continue
    New_df['Date'] =  pd.to_datetime(New_df['Date'], format='%Y-%m-%d')
    New_df['Value'] = pd.to_numeric(New_df['Value'])

    New_df=New_df.groupby('Date').mean()
    
    New_df = New_df.resample('D').ffill().reset_index()
    print(New_df['Date'])
    
