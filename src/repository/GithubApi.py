import logging as log
import requests

GITHUB_BASE = "https://api.github.com/"
GITHUB_TOKEN = "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" 

def get_user_repos(per_page, page):
    url = GITHUB_BASE + f"user/repos?per_page{per_page}&page{page}"
    token = GITHUB_TOKEN
    headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }
    response = requests.request("GET", url, headers=headers)
    print(response)
    return response

def get_repo_pullrequest(owner_repository, perpage,page):
    url = GITHUB_BASE + f"repos/{owner_repository}/pulls?state=all&per_page={perpage}&page={page}"
    token = GITHUB_TOKEN
    headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }
    response = requests.request("GET", url, headers=headers)
    print(response)
    return response


def get_pull_commits(owner_repository, number):
    url = GITHUB_BASE + f"{owner_repository}/pulls/{number}/commits"
    token = GITHUB_TOKEN
    headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }
    response = requests.request("GET", url, headers=headers)
    print(response)
    return response




def get_pr_files(owner_repository, number):
    url = GITHUB_BASE + f"repos/{owner_repository}/pulls/{number}/files"
    token = GITHUB_TOKEN
    headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }
    response = requests.request("GET", url, headers=headers)
    print(response)
    return response

def get_pr_reviews(owner_repository, number):
    url = GITHUB_BASE + f"repos/{owner_repository}/pulls/{number}/reviews"
    token = GITHUB_TOKEN
    headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }
    response = requests.request("GET", url, headers=headers)
    print(response)
    return response

def send_request(url):
    url = url 
    token = GITHUB_TOKEN
    headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }
    response = requests.request("GET", url, headers=headers)
    print(response)
    return response

def get_pull_request(ownerrepo,fecha_inicio,fecha_fin,per_page,page):
    query = f"repo:{ownerrepo} is:pr created:{fecha_inicio}..{fecha_fin}"
    headers = {
    "Accept": "application/vnd.github.v3+json",
    }
    params = {
    "q": query,
    "sort": "created",  # Opcional: ordenar por fecha de creación
    "order": "desc",  # Opcional: orden descendente
    "per_page" : per_page,
    "page" : page
    }
    url = GITHUB_BASE + f"search/issues"

    response = requests.get(url, headers=headers, params=params)

    return response
