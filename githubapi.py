import requests
import json
import utils
from ratelimit import limits, sleep_and_retry

headers={
    
    'Authorization': 'token <myToken>'
}

FIFTEEN_MINUTES = 900

@sleep_and_retry
@limits(calls=1000, period=FIFTEEN_MINUTES)
def getName(owner):
    
    r = requests.get('https://api.github.com/users/' +  owner, headers=headers)
    if(r.ok):
        
        repoItem = json.loads(r.text or r.content)
        name = repoItem.get('name')
        return name
    else:
        return None


@sleep_and_retry
@limits(calls=1000, period=FIFTEEN_MINUTES)
def getStars(repository):
    
    r = requests.get('https://api.github.com/repos/' +  repository, headers=headers)
    if(r.ok):
        
        repoItem = json.loads(r.text or r.content)
        star_amount = repoItem.get('stargazers_count')
        return star_amount
    else:
        return None


@sleep_and_retry
@limits(calls=1000, period=FIFTEEN_MINUTES)        
def getLanguages(repository):
    
    r = requests.get('https://api.github.com/repos/' +  repository + '/languages', headers=headers)
    if(r.ok):
        
        repoItem = json.loads(r.text or r.content)
        languages = repoItem.keys()
        return list(languages)
    else:
        return None
 
    
@sleep_and_retry
@limits(calls=1000, period=FIFTEEN_MINUTES)   
def getContributors(repository):
    
    r = requests.get('https://api.github.com/repos/' + repository + '/contributors?per_page=100&page=1', headers = headers)
    contributor_amount = 0
    
    if(r.ok and r.status_code != 204):
        contributors = r.json()
        
        while 'next' in r.links.keys():
            r=requests.get(r.links['next']['url'], headers = headers)
            contributors.extend(r.json())
        
        contributor_amount = len(contributors)
        
    return contributor_amount 

          
@sleep_and_retry
@limits(calls=1000, period=FIFTEEN_MINUTES)                
def getForks(repository):
    
    r = requests.get('https://api.github.com/repos/' +  repository, headers=headers)
    if(r.ok):
        
        repoItem = json.loads(r.text or r.content)
        fork_amount = repoItem.get('forks')
        return fork_amount
    else:
        return None
  
        
@sleep_and_retry
@limits(calls=500, period=FIFTEEN_MINUTES) 
def getLastCommit(repository, branch=None):
    
    r = requests.get('https://api.github.com/repos/' + repository + '/commits', headers=headers)
    if(r.ok):
        repoItem = json.loads(r.text or r.content)
       
        if len(repoItem) != 0:
            try:
                last_commit = repoItem[0].get('commit').get('author').get('date')
                return last_commit
            except KeyError:
                print(KeyError)
        else:
            return None
    else:
        return None
 
    
@sleep_and_retry
@limits(calls=500, period=FIFTEEN_MINUTES)    
def getFirstCommit(repository, branch=None):
    
    r = requests.get('https://api.github.com/repos/' + repository + '/commits?simple=yes&per_page=100&page=1', headers=headers)
    if(r.ok):
       
        commits = r.json()
        
        while 'next' in r.links.keys():
            r=requests.get(r.links['next']['url'], headers=headers)
            commits.extend(r.json())
        
        repoItem = json.loads(r.text or r.content)
        
        if len(repoItem) != 0:
            try:
                first_commit = repoItem[-1].get('commit').get('author').get('date')
                return first_commit
            except KeyError:
                print(KeyError)
        else:
            return None
    else:
        return None
    
