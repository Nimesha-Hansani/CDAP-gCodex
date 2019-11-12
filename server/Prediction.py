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
from flask import Flask, jsonify,request,json


def forcasting(repo):
    
    connection = MongoClient('localhost',27017)
    Database = connection.gCodexDB
    data_cog =Database.cognitiveValues
    data_loc =Database.LinesOfCode
    data_hal =Database.Halstead
    # ------------------------------------------------------------
    cogDF = pd.DataFrame(columns =['Date','Time','Value'])
    
    
    dataList1= data_cog.find({'Repository':repo})
    
    for data in dataList1:
        try:
            for branch in data['Branches']:
        
                for commit in branch['Commits']:
           
                    for content in commit['Contents']:
                        RowDataSet = {'Date':commit['Commit Date'],'Time':commit['Commit Time'],'Value':content['Cognitive Metric Value']}
                        cogDF = cogDF.append(RowDataSet,ignore_index=True)
            
        except:
        
                continue
    cogDF['Date'] =  pd.to_datetime(cogDF['Date'], format='%Y-%m-%d')
    cogDF['Value'] = pd.to_numeric(cogDF['Value'])
    
    cogDF=cogDF.groupby('Date').mean()
    
    cogDF = cogDF.resample('D').ffill().reset_index()
    
    value_list = cogDF['Value'].tolist()
    date_list = cogDF['Date'].tolist()

    # ----------------------------------------------
  
    locDF = pd.DataFrame(columns =['Date','Time','F_Value','S_Value'])
    dataList2 =data_loc.find({'Repository':repo})

    
    for data in dataList2:
        try:
            for branch in data['Branches']:
        
                for commit in branch['Commits']:
           
                    for content in commit['Contents']:
                        RowDataSet = {'Date':commit['Commit Date'],'Time':commit['Commit Time'],'F_Value':content['File Lines of Code'],'S_Value':content['Source Lines of Code']}

                        locDF = locDF.append(RowDataSet,ignore_index=True)
                        
        except:
        
                continue
    locDF['Date'] =  pd.to_datetime(locDF['Date'], format='%Y-%m-%d')
    
    locDF['F_Value'] = pd.to_numeric(locDF['F_Value'])
    locDF['S_Value'] = pd.to_numeric(locDF['S_Value'])

    locDF=locDF.groupby('Date').mean()
    
    locDF = locDF.resample('D').ffill().reset_index()
    
    F_value_list = locDF['F_Value'].tolist()
    S_value_list = locDF['S_Value'].tolist()
    loc_date_list = locDF['Date'].tolist()

#    ------------------------------------------------------------------------------------------
   

    halDF = pd.DataFrame(columns =['Date','Time','Pr_Length','Pr_Diff','Pr_Ef','Pr_Ti'])

    dataList3 = data_hal.find({'Repository':repo})

    
    
    for data in dataList3:
        try:
            for branch in data['Branches']:
        
                for commit in branch['Commits']:
           
                    for content in commit['Contents']:
                        RowDataSet = {'Date':commit['Commit Date'],'Time':commit['Commit Time'],'Pr_Length':content['Program Length'],'Pr_Diff':content['Program Difficulty'],'Pr_Ef':content['Program Effort'],'Pr_Ti':content['Programming Time']}

                        halDF  = halDF .append(RowDataSet,ignore_index=True)
                        
            
        except:
        
                continue
    halDF['Date'] =  pd.to_datetime(halDF['Date'], format='%Y-%m-%d')
  
    # halDF['Time'] = pd.to_numeric(halDF['Time'])
    halDF['Pr_Length'] = pd.to_numeric(halDF['Pr_Length'])
    halDF['Pr_Diff'] = pd.to_numeric(halDF['Pr_Diff'])
    halDF['Pr_Ef'] = pd.to_numeric(halDF['Pr_Ef'])
    halDF['Pr_Ti'] = pd.to_numeric(halDF['Pr_Ti'])
    


    halDF=halDF.groupby('Date').mean()
    
    
    
    halDF = halDF.resample('D').ffill().reset_index()
    
    
    Pr_Length_list = halDF['Pr_Length'].tolist()
    Pr_Diff_list = halDF['Pr_Diff'].tolist()
    Pr_Ef_list = halDF['Pr_Ef'].tolist()
    Pr_Ti_list = halDF['Pr_Ti'].tolist()
    
    Pr_date_list = halDF['Date'].tolist()


    data = json.dumps([{'g1_x': date_list, 'g1_y': value_list}, 
                        {'g2_x': loc_date_list, 'g2_y1': F_value_list, 'g2_y2': S_value_list},
                        {'g3_x': Pr_date_list, 'g3_y1': Pr_Length_list, 'g3_y2': Pr_Diff_list, 'g3_y3': Pr_Ef_list, 'g3_y4': Pr_Ti_list}])

   

    return data