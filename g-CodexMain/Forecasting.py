import pymongo
from pymongo import MongoClient
from nested_lookup import nested_lookup
import pandas as pd 

connection = MongoClient('localhost',27017)
Database = connection.gCodexDB
data =Database.Halstead
dataList =data.find()
New_df = pd.DataFrame() #Temporary empty dataframe
for data in dataList:
    print(data['Branch'])
    
    for data1 in data['Commits']:
        # print(data1['Commit Date'] +' '+ data1['Commit Time'])
        try :
            for data2 in data1['Contents']:
              FNameList = data2['Folder Path'].split('/')
              File_Name =FNameList[len(FNameList)-1]
              PathArray =[]
              for i in FNameList:
                   PathArray.append(i)
                  
            #   print(data1['Commit Date']+','+
            #         data1['Commit Time']+','+
            #         str(PathArray)+','+
            #         PathArray[len(PathArray)-1]+
            #         ','+str(data2['Program Volume'])+','+
            #         str(data2['Program Difficulty'])+','+
            #         str(data2['Program Effort'])+','+
            #         str(data2['Programming Time']))
            # -----------------------------------------------------------------------
              RowDataSet=[[
                         data['Branch'],
                         data1['Commit Date'], data1['Commit Time'],
                         str(PathArray),PathArray[len(PathArray)-1],
                         str(data2['Program Volume']) ,str(data2['Program Difficulty']), 
                         str(data2['Program Effort']),str(data2['Programming Time'])     ]]
              
              temp_df = pd.DataFrame(RowDataSet, columns = ['Branch','Commit Date', 'Commit Time','Repo Path','File Name','Program Volume','Program Difficulty','Program Effort','Programming Time'])
              New_df = temp_df.append(temp_df, ignore_index=True) 
            #   print(RowDataSet)
            #   Initialize the data set
               
        except:
             continue

# Create the pandas DataFrame 
print(New_df[:10])
