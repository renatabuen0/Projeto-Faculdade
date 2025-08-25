import json
from pathlib import Path

#lista de produtos
_produtos_path = Path(__file__).resolve().parent / "static" / "produtos.json"
try:
    with _produtos_path.open("r", encoding="utf-8") as f:
        produtos = json.load(f)
    if not isinstance(produtos, list):
        produtos = []
except (FileNotFoundError, json.JSONDecodeError):
    produtos = []
# (mantenha suas funções bubble_sort, busca_linear, busca_binaria como estão)

#lista de musicas
_musicas_path = Path(__file__).resolve().parent / "static" / "musicas.json"
try:
    with _musicas_path.open("r", encoding="utf-8") as f:
        musicas = json.load(f)
    if not isinstance(musicas, list):
        musicas = []
except (FileNotFoundError, json.JSONDecodeError):
    musicas = []

# Bubble sort por price
def bubble_sort(lista):
    n = len(lista)
    for i in range(n):
        trocou = False
        for j in range(0, n - i - 1):
            if float(lista[j].get("price", 0)) > float(lista[j + 1].get("price", 0)):
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                trocou = True
        if not trocou:
            break
    return lista


# Busca linear por name (substring)
def busca_linear(lista, name):
    ordenada =  bubble_sort(lista, key=lambda x: x.get("name", "").strip().lower())
    alvo = name.strip().lower()
    resultados = []
    for produto in ordenada:
        nome_produto = produto.get("name", "").strip().lower()
        if alvo in nome_produto:
            resultados.append(produto)
    return resultados

# Busca binária por name (substring, lista ordenada por name)
def busca_binaria(lista, name):
    ordenada = bubble_sort(lista, key=lambda x: x.get("name", "").strip().lower())
    alvo = name.strip().lower()
    if not alvo:
        return []
    low, high = 0, len(ordenada) - 1
    found = -1
    while low <= high:
        mid = (low + high) // 2
        mid_name = ordenada[mid].get("name", "").strip().lower()
        if alvo in mid_name:
            found = mid
            break
        if mid_name < alvo:
            low = mid + 1
        else:
            high = mid - 1
    if found == -1:
        return []
    resultados = []
    i = found
    while i >= 0:
        nome = ordenada[i].get("name", "").strip().lower()
        if alvo in nome:
            resultados.insert(0, ordenada[i])
            i -= 1
        else:
            break
    i = found + 1
    while i < len(ordenada):
        nome = ordenada[i].get("name", "").strip().lower()
        if alvo in nome:
            resultados.append(ordenada[i])
            i += 1
        else:
            break
    return resultados