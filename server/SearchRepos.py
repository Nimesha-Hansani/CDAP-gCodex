from flask import Flask, jsonify,request,json
from datetime import datetime
from github  import Github
import json


app = Flask(__name__)

@app.route('/users/getUserRepos',methods=['POST'])

def getUserRepos():
    
   
    g = Github("Nimesha-Hansani", "19950525hansani")
    user= g.get_user().login
    List =[ ]
    repos=g.get_user().get_repos()
    #meh loop eken return wena hama value ekakm ara user project wl enne oni
    for repo in repos:
        # This should be the out put 
        print(repo.name)  
        List.append(repo.name) 

    return jsonify(Username = user , RepoList = List)

  


    


