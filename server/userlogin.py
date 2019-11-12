from flask import Flask, jsonify,request,json
from datetime import datetime
from github  import Github
import json
import ReadRepoLOC
import ReadRepoCompr
import ReadRepoHalstead
import dbfunctions
import Prediction
from pymongo import MongoClient
import pymongo
import commited


app = Flask(__name__)
g = None
UNM = None
PSW = None 

# ReadRepoCompr.TraverseCompr("nimeshaamarasingha@gmail.com","19950525hansani","Nimesha-Hansani/TestRepo-CDAP")
@app.route('/users/login',methods=['POST'])
def login():
    result = ''
    username = request.json.get('username')
    password = request.json.get('password')
    global UNM
    global PSW
    UNM = username
    PSW = password
    try:
        instance = Github(username, password)
        global g
        g= instance
       
        user =g.get_user()   
        

        result = user.login
    except:
        print("Cannot login")
        result =  "False"
   
    return result

    
@app.route('/users/getUserRepo',methods=['GET'])   
def getUserRepos():
    
    repos=g.get_user().get_repos()
    user= g.get_user()
    List =[]

    
    for repo in repos:
        # This should be the out put    
        List.append(repo.full_name) 

    return jsonify(userName = user.login , avatar=user.avatar_url, repoList = List)

  
@app.route('/users/searchByInputs',methods = ['GET'])
def searchByInputs ():
    # here, the search method and the searched keyword both are sent by url params (ex: ?search=language&keyword=java)
    search = request.args.get('search')
    keyword = request.args.get('keyword')

    if (search == 'language'):

        lan_repos = g.search_repositories(query=keyword)[:50]
        lan_List = []

        for repo in lan_repos:

            lan_List.append(repo.full_name)
          
        return jsonify(RepoList = lan_List)
    else :

        url_repos = g.search_repositories(keyword)
        url_List = []

        for repo in url_repos:

            url_repos.append=(repo.full_name)
        
        return jsonify(RepoList = url_List)
        


@app.route('/users/readContents',methods=['GET'])   
def readContents():
    repo = request.args.get('repo')
    print(repo)
    try:
    
        # dbfunctions.deleteLinesofCode()
        # ReadRepoLOC.TraverseLOC(UNM ,PSW,repo)

        connection = MongoClient('localhost',27017)
        Database = connection.gCodexDB
        data1 =Database.LinesOfCode
        data2 = Database.Halstead
        data3 = Database.cognitiveValues

        dataList = data1.find({'Repository':repo})

        if (dataList.count() == 0):

            data1.delete_many({})
            data2.delete_many({})
            data3.delete_many({})
            ReadRepoLOC.TraverseLOC(UNM,PSW,repo)
            ReadRepoCompr.TraverseCompr(UNM,PSW,repo)
            ReadRepoHalstead.TraverseHalstead(UNM,PSW,repo)
            locdata=dbfunctions.returnLOCdata()
            return locdata
        else :
            locdata=dbfunctions.returnLOCdata()
            return locdata

    except Exception as e:
        
        print(e.status)

        return jsonify(success = False)



@app.route('/users/halstead',methods=['GET'])
def halstead():
    
    repo = request.args.get('repo')
    print(repo)
    try:
        
       
        datalist=dbfunctions.returnHalsteaddata()
        print(datalist)
        return datalist
    
    except Exception as e:
        
        print(e)
        return jsonify(success = False)

@app.route('/users/comprehension',methods=['GET'])   
def comprehension():
    repo = request.args.get('repo')
    print(repo)
    try:
    
     
        datalist=dbfunctions.returnComprdata()
        print(datalist)
        return datalist
        

    except Exception as e:
        
        print(e.status)

        return jsonify(success = False)




@app.route('/users/forcasting',methods=['GET'])  
def forcasting():
    try:
        
        repo = request.args.get('repo')
        data =Prediction.forcasting(repo)
       
        return data 
        # return jsonify(success = False)


    except Exception as e:
        print(e)
        return jsonify(success = False)


@app.route('/users/defects',methods=['GET'])  
def defects():
    try:
        
        repo = request.args.get('repo')
        commits =commited.topCommitters(UNM,PSW,repo)

        commited.issueCloud(UNM,PSW,repo)
        status = commited.defectstatus()


        data = json.dumps({'commit': commits, 'status': status})

        return data
       
        # return jsonify(success = False)


    except Exception as e:
        print(e)
        return jsonify(success = False)






       
if __name__ == "__main__":
    app.run(host='192.168.8.100',port=5000)
#     app.run()