from repository.GithubApi import get_repo_pullrequest, get_pull_request, get_user_repos, get_pr_reviews, send_request, get_pr_files
from config.DataConfig.config import PERPAGE
from config import util
import requests
from json import loads
import pandas as pd
from datetime import datetime
from requests.auth import HTTPBasicAuth
from utils.repos import get_all_repo, get_repo_all_prs

requests.packages.urllib3.disable_warnings()


def get_pr_info(pr, name, fullname):
    file_extension_count_dict = {}

    comments_response = send_request(pr["comments_url"])
    comments = loads(comments_response.content)

    pr["comments"] = len(comments)
    pr["user"] = pr["user"]["login"]

    pr_response = send_request(pr["pull_request"]["url"])
    pull_request = loads(pr_response.content)

    pr["origen"] = pull_request["head"]["ref"]
    pr["destino"] = pull_request["base"]["ref"]

    files_response = get_pr_files(fullname, pull_request["number"])
    if (files_response.status_code == 200):
        files = loads(files_response.content)
        pr["archivos"] = len(files)
        eliminadas = 0
        agregadas = 0
        for file in files:
            eliminadas += file["deletions"]
            agregadas += file["additions"]

            filename = file["filename"]
            file_extension = filename.split(".")[-1]

            if file_extension in file_extension_count_dict:
                file_extension_count_dict[file_extension] += 1
            else:
                file_extension_count_dict[file_extension] = 1

        pr["archivos_mod_ext"] = file_extension_count_dict
        pr["agregadas"] = agregadas
        pr["eliminadas"] = eliminadas

    reviewer_response = get_pr_reviews(fullname, pull_request["number"])
    if (reviewer_response.status_code == 200):
        reviewers = loads(reviewer_response.content)
        approves = 0
        commented = 0
        for reviewer in reviewers:
            if reviewer["state"] == "APPROVED":
                approves += 1
            if reviewer["state"] == "COMMENTED":
                commented += 1
        pr["approves"] = approves
        pr["involucrados"] = commented

    if pr["state"] == "open":
        pr["state"] = "OPEN"
    if pr["state"] == "closed":
        pr["state"] = "MERGED"

    pr["name"] = name
    pr["number"] = pull_request["number"]
    pr["requested_reviewers"] = pull_request["requested_reviewers"]

    return pr


def get_repos_json(fecha_inicio, fecha_fin):
    df_prs_all = pd.DataFrame()
    repos = get_all_repo()

    for repo in repos:
        prs = get_repo_all_prs(repo["full_name"], fecha_inicio, fecha_fin)

        for pr in prs:
            pr = get_pr_info(pr, repo["name"], repo["full_name"])

        df_prs = pd.DataFrame(prs)

        if df_prs.empty == False:
            df_prs["created_at"] = pd.to_datetime(df_prs["created_at"])
            df_prs["created_at"] = pd.to_datetime(
                df_prs["created_at"]) - pd.Timedelta(hours=5)
            df_prs["closed_at"] = pd.to_datetime(df_prs['closed_at'])
            df_prs["closed_at"] = pd.to_datetime(
                df_prs["closed_at"]) - pd.Timedelta(hours=5)
            df_prs["tiempo"] = df_prs.apply(lambda pr: util.get_diff_of_dates(
                pr["created_at"], pr["closed_at"]), axis=1)
            df_prs["created_at"] = df_prs.apply(
                lambda pr: pr["created_at"].tz_localize(None), axis=1)
            df_prs["closed_at"] = df_prs.apply(
                lambda pr: pr["closed_at"].tz_localize(None), axis=1)
        df_prs_all = pd.concat([df_prs_all, df_prs], ignore_index=True)

    df_repos = pd.DataFrame(repos)

    df_prs_all.to_excel("output/pr.xlsx", index=False, columns=['name', 'title', 'number', 'origen', 'destino', 'state', "archivos", 'agregadas', 'eliminadas', 'created_at', 'closed_at', 'tiempo', 'user',
                                                                'requested_reviewers', "involucrados", "approves", "comments", "archivos_mod_ext"])
    df_repos.to_excel("output/repo.xlsx", index=False,
                      columns=['name', 'size', 'language', 'created_at'])
