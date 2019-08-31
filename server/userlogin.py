from flask import Flask, jsonify,request,json
from datetime import datetime
from github  import Github
import json
import ReadRepoContents

app = Flask(__name__)
g = None
ReadRepoContents.CalculateHalstead()

@app.route('/users/login',methods=['POST'])
def login():
    result = ''
    username = request.json.get('username')
    password = request.json.get('password')
    print(username)
    print(password)

    try:
        instance = Github(username, password)
        global g
        g= instance
        
        user =g.get_user()   

        result = user.login
    except:
        print("cannot login")
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
        List.append(repo.name) 

    return jsonify(userName = user.login , avatar=user.avatar_url, repoList = List)

@app.route('/users/getByInputs',methods = ['GET'])
def getByInputs ():
    # here, the search method and the searched keyword both are sent by url params (ex: ?search=language&keyword=java)
    search = request.args.get('search')
    keyword = request.args.get('keyword')
    # test = g.rate_limiting_resettime
    # print(test)
    # return "ela"

    if (search == 'language'):

        lan_repos = g.search_repositories(query=keyword)[:50]
        lan_List = []

        for repo in lan_repos:

            lan_List.append(repo.name)
          
        return jsonify(RepoList = lan_List)
    else :

        url_repos = g.search_repositories(keyword)
        url_List = []

        for repo in url_repos:

            url_repos.append=(repo.name)
        
        return jsonify(RepoList = url_List)

  

    
    

if __name__ == "__main__":
    app.run()