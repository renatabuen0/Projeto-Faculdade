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

def bubble_sort(lista, key=None, reverse=False):
    """Bubble sort simples.
    Se key não for fornecida e os itens forem dicts com 'price', usa esse campo por padrão.
    Retorna a lista ordenada (in-place)."""
    if key is None:
        if lista and isinstance(lista[0], dict) and 'price' in lista[0]:
            key = lambda x: float(x.get('price', 0) or 0)
        else:
            key = lambda x: x  # identidade
    n = len(lista)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            a = key(lista[j]); b = key(lista[j + 1])
            if (a > b and not reverse) or (a < b and reverse):
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                swapped = True
        if not swapped:
            break
    return lista


def busca_linear(lista, termo, field="name"):
    """Retorna itens cujo campo contém 'termo' (substring, case-insensitive)."""
    termo = termo.strip().lower()
    if not termo:
        return []
    return [item for item in lista if termo in str(item.get(field, "")).strip().lower()]

def busca_binaria(lista, termo, field="name"):
    """Busca por substring usando ordenação + localização binária + expansão lateral.
    Retorna todas as ocorrências onde o campo contém o termo.
    """
    termo = termo.strip().lower()
    if not termo:
        return []
    ordenada = sorted(lista, key=lambda x: str(x.get(field, "")).strip().lower())
    nomes = [str(x.get(field, "")).strip().lower() for x in ordenada]
    lo, hi = 0, len(nomes) - 1
    found = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        val = nomes[mid]
        if termo in val:
            found = mid
            break
        if val < termo:
            lo = mid + 1
        else:
            hi = mid - 1
    if found == -1:
        return []
    res = [ordenada[found]]
    i = found - 1
    while i >= 0 and termo in nomes[i]:
        res.insert(0, ordenada[i]); i -= 1
    i = found + 1
    while i < len(nomes) and termo in nomes[i]:
        res.append(ordenada[i]); i += 1
    return res