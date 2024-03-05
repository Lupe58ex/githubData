from json import loads
from config.DataConfig.config import PERPAGE
from repository.GithubApi import get_pull_request, get_user_repos


def get_all_repo():
    all_repo = []
    page = 1
    flag = True

    while (flag):
        temp_repo = get_user_repos(PERPAGE, page)
        repo = loads(temp_repo.content)
        page += 1
        all_repo.extend(repo)
        if len(repo) < PERPAGE:
            flag = False

    return all_repo


def get_repo_all_prs(repo_name, fecha_inicio, fecha_fin):
    all_prs = []
    page = 1
    flag = True

    while (flag):
        temp_pr = get_pull_request(
            repo_name, fecha_inicio, fecha_fin, PERPAGE, page)
        if (temp_pr.status_code == 200):
            prs = temp_pr.json()['items']
            page += 1
            all_prs.extend(prs)
            if len(prs) < PERPAGE:
                flag = False
        else:
            flag = False

    return all_prs
