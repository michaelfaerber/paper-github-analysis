import os
import json
import csv

def duplicates(x):
  return list(dict.fromkeys(x))

def listdirs(folder):
    return [
        d for d in (os.path.join(folder, d1) for d1 in os.listdir(folder))
        if os.path.isdir(d)
    ]

def get_fileextension():

    with open('frameworks.json', 'r') as json_file:
        data=json_file.read()
    
    frameworks = json.loads(data)
    extension = []

    for i in range(len(frameworks)): 
        extension.append(frameworks[i].get("endung"))
    
    extensionlist = [item for elem in extension for item in elem]
            
    return tuple(extensionlist)

def findframeworks(path):
    
    with open('frameworks.json', 'r') as json_file:
        data=json_file.read()
    
    frameworksjson = json.loads(data)
    frameworklist = []
    
    with open(path,'r',newline='', encoding='ISO-8859-1') as f:
        line = f.readline()
        while line:
            for i in range(len(frameworksjson)): 
                for j in range(len(frameworksjson[i].get("frameworks"))):
                    header = frameworksjson[i].get("frameworks")[j].get("header")
                    for head in header:
                        if line.startswith(head):
                            frameworklist.append(frameworksjson[i].get("frameworks")[j].get('name'))        

            line = f.readline()
                
    return frameworklist
 
def get_frameworks(path):  
    
    folders = listdirs(path)
    frameDict = {}
    for repo in folders:   
        frameworks = []
        for root, dirs, files in os.walk(repo):
            try:
                if os.path.isdir(root):
                    for file in files:    
                        fp = os.path.abspath(os.path.join(root, file))
                        if file.endswith(get_fileextension()):
                            frameworks = frameworks + findframeworks(os.path.join(root,file)) 
    
            except FileNotFoundError:
                 print("File not found!")
        frameworks = duplicates(frameworks)
        reponame = repo.split("/")[-1]
        frameDict[reponame] = frameworks
    
    return frameDict
        
if __name__ == '__main__':
    
    dict = get_frameworks("/vol3/erhan/crawl-github1")
    with open('frameworks.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Repo","Frameworks"])
    
        for key in dict.keys():
            writer.writerow([key, dict[key]]) 
    