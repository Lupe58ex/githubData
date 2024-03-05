import requests
import json
import pandas as pd
from datetime import datetime
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()
from src.repository.GithubApi import get_repo_pullrequest,get_user_repos,get_pull_commits,send_request, get_pr_files

def get_commit_info(commits_url,prid, name, origen, destino):
    commits_response = send_request(commits_url)
    if(commits_response.status_code==200): 
        commits =  json.loads(commits_response.content)
        for commit in commits:
            commits_details_response = send_request(commit["url"])
            if(commits_details_response.status_code==200):
                commits_details =  json.loads(commits_details_response.content)
                commit["lineas_agregadas"] = commits_details["stats"]["additions"]
                commit["lineas_eliminadas"] = commits_details["stats"]["deletions"]
                commit["autor"] = commits_details["commit"]["author"]["email"]
                commit["message"] = commits_details["commit"]["message"]
                commit["date"] = commits_details["commit"]["committer"]["date"]
                commit["date"] = pd.to_datetime(commit["date"]) - pd.Timedelta(hours=5)
                commit["date"] = commit["date"].tz_localize(None)
                # commit['date'] = pd.to_datetime(commit['date'])
                # commit['date'] = commit['date'].dt.tz_convert('America/Bogota')
                commit["prid"] = prid
                commit["repository"] = name
                commit["files_count"] = len(commits_details["files"])
                commit["origin_branch"] = origen
                commit["destino_branch"] = destino
        df_commits = pd.DataFrame(commits)
        return df_commits


def get_repos_json():

    repositories_response = get_user_repos() 
    df_prs_all = pd.DataFrame()
    df_commit_all = pd.DataFrame()

    if(repositories_response.status_code==200): 
        repos =  json.loads(repositories_response.content)
        df_repos = pd.DataFrame(repos)
        for repo in repos:
            pull_request_response = get_repo_pullrequest(repo["full_name"])
            if(pull_request_response.status_code==200): 
                prs =  json.loads(pull_request_response.content)
                for pr in prs:
                    df_commits = get_commit_info(pr["commits_url"], pr["number"],repo["name"], pr["head"]["ref"], pr["base"]["ref"])
                    df_commit_all = pd.concat([df_commit_all, df_commits], ignore_index=True)

        df_commit_all.to_excel("output/commits.xlsx",index = False, columns=["repository",'prid','sha','files_count','lineas_agregadas','lineas_eliminadas','origin_branch','destino_branch','sha','message','autor','date'])
    else:
        return None
    
get_repos_json()