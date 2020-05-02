import numpy as np
import pandas as pd
import requests
import json
import csv

import githubapi as g
import frameworklist as fwl
import utils as u

def main():

    links = u.get_githublinks("PaperResources_20191213_Code_primary_github.txt")
    owner = u.get_owner(links)
    repositories = u.get_repository(links)
    onlyrepo = [repo.split("/")[-1] for repo in repositories]
    
    names = [g.getName(owner) for owner in owner]
    stars = [g.getStars(repo) for repo in repositories]
    forks = [g.getForks(repo) for repo in repositories]
    languages = [g.getLanguages(repo) for repo in repositories]
    contributors = [g.getContributors(repo) for repo in repositories]
    
    firstcommit= [g.getFirstCommit(repo) for repo in repositories]
    lastcommit = [g.getLastCommit(repo) for repo in repositories]
    
    gitapidf = pd.DataFrame(np.column_stack([names, repositories, onlyrepo, stars, forks,languages, contributors, firstcommit, lastcommit]), 
                             columns=['Name', 'Repository', 'onlyrepo', 'Stars', 'Forks', 'Languages', 'Contributors', 'First Commit', 'Last Commit'])
    
    frameworkdict = fwl.get_frameworks("/vol3/erhan/crawl-github1")
    frameworkseries = pd.Series(frameworkdict)
    frameworkdf = pd.DataFrame({'onlyrepo':frameworkseries.index, 'Frameworks':frameworkseries.values})
    
    github_analyse = gitapidf.merge(frameworkdf, on='onlyrepo', how='left')
    github_analyse.to_excel("output.xlsx") 
    
if __name__ == '__main__':
    main()
   
    