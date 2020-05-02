import subprocess

def duplicates(x):
    return list(dict.fromkeys(x))

def get_extensions(path):
    
    proc = subprocess.Popen("find " + path + " -type f | perl -ne 'print $1 if m/\.([^.\/]+)$/' | sort | uniq -c | sort -n", stdout=subprocess.PIPE,shell=True)


    for line in proc.stdout.readlines(): 
        print(line.decode("utf-8").replace("\n", "").lstrip())
        
def get_githublinks(file):
    
    proc = subprocess.Popen("cat " + file + " | awk '{ print $3 }'", stdout=subprocess.PIPE,shell=True)
    
    links = [line.decode("utf-8").replace("\n", "").lstrip() for line in proc.stdout.readlines()]
    
    for i, link in enumerate(links):
        
        links[i] = link.lower()
        
        if link.find("/blob/") != -1:
            links[i] = link[:link.find("/blob/")]
        if link.find("/tree/") != -1:
            links[i] = link[:link.find("/tree/")]
        if link.find("/pull/") != -1:
            links[i] = link[:link.find("/pull/")]
        if link.find("/releases/") != -1:
            links[i] = link[:link.find("/releases/")]
        
        if link.endswith("/releases"):
            links[i] = link[:-len("/releases")]
        if link.endswith("/downloads"):
            links[i] = link[:-len("/downloads")]
        if link.endswith(".git"):
            links[i] = link[:-len(".git")]
                   
    return duplicates(links)   

def get_owner(links):
    
    owner = []
    for link in links:
        #1. github-link
        if link.find("github.com/")!= -1 and not is_gist(link):
            
            link = link[link.find("github.com/")+len("github.com/"):]
            owner.append(link.split("/")[0])
            
        #2. github-page
        #elif link.find("github.io")!=-1:
        #    link = link[link.find("//")+2:]
        #    owner.append(link.split('.')[0])
      
    return owner
        
def get_repository(links):
    
    repos = []
    
    for link in links:
        if link.find("github.com/") != -1 and not is_gist(link):
            repos.append(link[link.find("github.com/")+len("github.com/"):])
            
    for i, repo in enumerate(repos):
        if repo.endswith("/"):
            repos[i] = repo[:-1] 
            
    return repos    
        
def is_gist(link):
    
    if link.find("gist.github.com") != -1:
        return True
    
    return False

def is_pages(link):
    
    if link.find(".github.io") != -1:
        return True
    
    return False
