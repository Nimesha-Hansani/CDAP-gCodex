from github  import Github
# using username and password
g = Github("Nimesha-Hansani", "19950525hansani")
user =g.get_user()
repository=g.get_repo("laveesha/Data-Minin-App")
branches=repository.get_branches()
for br in branches:
    print(br)
    headCommit=br.commit.sha
    
    print("This is the head commit of a branch : " +headCommit)
    commits = repository.get_commits(headCommit)
    
    for com in commits:
      commitDate=repository.get_commit(com.sha)
      print(commitDate.commit.author.date)
      print("Commit SHA Key " +com.sha)
      
      
      
      tree=repository.get_git_tree(com.sha).tree
      for tr in tree:
        
        try:
          treeContent=repository.get_contents(tr.path)
          while len(treeContent)> 1:
            file_content=treeContent.pop(0)
            print(file_content)
            if file_content.type =="dir":
               treeContent.extend(repository.get_contents(file_content.path))
            else :
                print(file_content.path)

        except:
          pass
         
    