

from service.PullRequestService import get_repos_json


start_date = input("Ingrese la fecha de inicio (formato YYYY-MM-DD): ")
end_date = input("Ingrese la fecha de fin (formato YYYY-MM-DD): ")

get_repos_json(start_date, end_date)
