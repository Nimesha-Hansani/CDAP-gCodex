from github import Github

# User Authentocation 
g = Github("Nimesha-Hansani", "19950525hansani")
repos=g.get_user().get_repos()

def search_github(keywords):
    query = '+'.join(keywords) + '+in:readme+in:description'
    result = g.search_repositories(query, 'stars', 'desc')
 
    print(f'Found {result.totalCount} repo(s)')
 
    for repo in result:
        print(repo.clone_url)
        print(repo.full_name)


if __name__ == '__main__':
    keywords = input('Enter keyword(s)[e.g python, flask, postgres]: ')
    keywords = [keyword.strip() for keyword in keywords.split(' ')]
    search_github(keywords)
