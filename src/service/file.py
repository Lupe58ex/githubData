import requests
 
# Configura tus parámetros aquí
owner = "spring-projects"
repo = "spring-boot"
fecha_inicio = "2024-03-01"
fecha_fin = "2024-03-31"
token = None  # Opcional, para autenticación
 
# Construye la consulta de búsqueda con cualificadoreqs de rango de fechas
query = f"repo:{owner}/{repo} is:pr created:{fecha_inicio}..{fecha_fin}"
 
# URL para la API de búsqueda de GitHub
url = "https://api.github.com/search/issues"
 
# Parámetros para la solicitud
params = {
    "q": query,
    "sort": "created",  # Opcional: ordenar por fecha de creación
    "order": "desc",  # Opcional: orden descendente
}
 
# Encabezados, incluyendo el token de autorización si es necesario
headers = {
    "Accept": "application/vnd.github.v3+json",
}
if token:
    headers["Authorization"] = f"token {token}"
 
response = requests.get(url, headers=headers, params=params)
 
if response.status_code == 200:
    pulls = response.json()['items']
    print(f"Pull requests encontrados: {len(pulls)}")
    for pull in pulls:
        print(f"- {pull['title']} creado en {pull['created_at']}")
else:
    print(f"Error al buscar los pull requests: {response.status_code}")