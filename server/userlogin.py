from flask import Flask, jsonify,request,json
from datetime import datetime
from github  import Github
import json
import ReadRepoLOC
import ReadRepoCompr
import ReadRepoHalstead
import dbfunctions

app = Flask(__name__)
g = None
UNM = None
PSW = None 
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

    #meh loop eken return wena hama value ekakm ara user project wl enne oni
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
        # ReadRepoHalstead.TraverseHalstead(UNM,PSW,repo)
        # ReadRepoLOC.TraverseLOC(UNM ,PSW,repo)
        #ReadRepoCompr.TraverseCompr(UNM,PSW,repo)
        
        # data = dbfunctions.rtrComprehension(repo)

        return jsonify(success= True)

    except Exception as e:
        
        # print(getattr(e, 'message', str(e)))
        print(e.status)

        return jsonify(success = False)



@app.route('/users/comprehension',methods=['GET'])   
def comprehension():
    repo = request.args.get('repo')
    print(repo)
    try:
        # ReadRepoHalstead.TraverseHalstead(UNM,PSW,repo)
        # ReadRepoLOC.TraverseLOC(UNM ,PSW,repo)
        ReadRepoCompr.TraverseCompr(UNM,PSW,repo)
        data = dbfunctions.rtrComprehension(repo)

        return data

    except Exception as e:
        
        # print(getattr(e, 'message', str(e)))
        print(e)
        return jsonify(success = False)


    
    
    
    
# @app.route('/user/forecasting',methods='GET')
# def forecasting():

       



if __name__ == "__main__":
    # app.run(host='192.168.1.100',port=5000)
    app.run()