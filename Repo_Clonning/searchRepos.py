from github import Github

# User Authentocation 
g = Github("Nimesha-Hansani", "19950525hansani")
repository =g.get_repo("Pylons/pyramid")
branches=repository.get_branches()
for br in branches:
    print(br)
repositories = g.search_repositories(query='python ')
for repo in repositories:
    print(repo)

def search_github(keywords):
    query = '+'.join(keywords) + '+in:readme+in:description'
    result = g.search_repositories(query, 'stars', 'desc')
 
    print('Found {result.totalCount} repo(s)')
 
    for repo in result:
        print(repo.clone_url)
        print(repo.full_name)


if __name__ == '__main__':
    keywords = input('Enter keyword(s)[e.g python, flask, postgres]: ')
    keywords = [keyword.strip() for keyword in keywords.split(' ')]
    search_github(keywords)
