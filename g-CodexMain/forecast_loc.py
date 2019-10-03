import pymongo
from pymongo import MongoClient
from nested_lookup import nested_lookup
import pandas as pd
import datetime 
import pyaf.ForecastEngine as autof

connection = MongoClient('localhost',27017)
Database = connection.gCodexDB
data =Database.LinesOfCode
dataList =data.find()

Row_df= pd.DataFrame(columns = ['Commit Date', 'Commit Time', 'SLOC'])

try:
    for data in dataList:
        # print(data)

        for Commits in data['Commits']:
            # ?\print(Commits['Commit Date'] +' '+ Commits['Commit Time'])
            for contents in Commits['Contents']:

                # FNameList = contents['Folder Path'].split('/')
                # File_Name =FNameList[len(FNameList)-1]
                # PathArray =[]

                # for i in FNameList:
                #     PathArray.append(i)

                RowDataSet=[
                            
                            Commits['Commit Date'], 
                            Commits['Commit Time'],
                            str(contents['SLOC'] )]

                s = pd.Series(RowDataSet, index=Row_df.columns)
                Row_df= Row_df.append(s, ignore_index=True)
    
    print(Row_df)
    Row_df['Commit Date'] =pd.to_datetime(Row_df['Commit Date'], format='%Y-%m-%d')
    Row_df['SLOC'] = pd.to_numeric(Row_df['SLOC'])

    Row_df=Row_df.set_index(Row_df['Commit Date']).groupby(pd.Grouper(freq='D')).mean()

    Row_df = Row_df.reset_index(level=0)
    Row_df['SLOC'] = Row_df.SLOC.fillna(method='ffill')

except:
    pass
# # create a forecast engine. This is the main object handling all the operations
# lEngine = autof.cForecastEngine()
# # print(lEngine)
# lEngine.train(iInputDS = Row_df, iTime = 'Commit Date', iSignal = 'SLOC', iHorizon = 2)
# # lEngine.getModelInfo() # => relative error 7% (MAPE)
