import requests

#BASE_URL = "https://treinamento.suapdevs.ifrn.edu.br/api"
BASE_URL = "https://suap.ifrn.edu.br/api"

def autenticar_suap(matricula, senha):
    response = requests.post(
        f"{BASE_URL}/token/pair",
        json={
            "username": matricula,
            "password": senha
        },
        timeout=10
    )

    if response.status_code != 200:
        return None

    return response.json().get("access")

def buscar_diarios(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f"{BASE_URL}/ensino/meus-diarios/2025/2/",
        headers=headers,
        timeout=10
    )

    if response.status_code != 200:
        return None

    return response.json().get("results")

#token = autenticar_suap("1221471", "123456")

#busca = buscar_diarios(token)

#for d in busca:
#    for a in d["aulas"]:
#        print(a)

#print(busca)