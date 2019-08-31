from github  import Github
# using username and password

g = Github("nimeshaamarasingha@gmail.com", "19950525hansani")

repo =g.get_repo("tensorflow/tensorflow")

labels =repo.get_labels()
for lb in labels:
    print(lb.name)
print("------------------------------")
issues = repo.get_issues()
for iss in issues:
     print(iss.title)
