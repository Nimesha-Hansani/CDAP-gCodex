import pymongo
from pymongo import MongoClient
from nested_lookup import nested_lookup
import pandas as pd 

connection = MongoClient('localhost',27017)
Database = connection.gCodexDB
data =Database.cognitiveValues
dataList =data.find()
New_df = pd.DataFrame() #Temporary empty dataframe

for data in dataList:
    for data1 in data['Commits']:
        try:
            for data2 in data1['Contents']:

                RowDataSet=[[
                        
                         data1['Commit Date'], data1['Commit Time'],
                         data1['Cognitive Metric Value']
                    ]]
                print(RowDataSet)
                New_df = New_df.append(RowDataSet,ignore_index=False)
        except:
            continue
print(New_df)