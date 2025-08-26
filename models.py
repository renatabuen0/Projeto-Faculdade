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
    resultados = []
    for item in lista:
        valor = str(item.get(field, "")).strip().lower()
        if termo in valor:
            resultados.append(item)
    return resultados

def busca_binaria(lista, termo, field="name"):
    """
    Busca itens cujo campo 'field' combina com o termo (case-insensitive).
    
    Estratégia:
    - Usa busca binária para encontrar rapidamente todos os itens cujo campo começa
      com o prefixo (termo). (Prefixo => região contígua em ordem lexicográfica)
    - Se nenhum item começar com o prefixo, faz fallback para busca linear de
      substring (termo em qualquer parte do campo).
    
    Parâmetros:
    - lista: lista de dicionários (ex.: produtos, músicas)
    - termo: string digitada pelo usuário (critério de busca)
    - field: chave do dicionário a ser pesquisada (padrão: "name")
    
    Retorna:
    - Lista de itens correspondentes.
    """
    termo = termo.strip().lower()
    if not termo:
        return [] 

    # Criar uma cópia ordenada da lista pelo campo alvo
    #    Usamos bubble_sort já existente para manter consistência.
    ordenada = bubble_sort(
        list(lista),
        key=lambda x: str(x.get(field, "")).strip().lower()
    )
    nomes = [str(x.get(field, "")).strip().lower() for x in ordenada]
    n = len(nomes)
    if n == 0:
        return []

    #Busca binária para achar a primeira posição onde nomes[i] >= termo
    esquerda, direita = 0, n
    while esquerda < direita:
        meio = (esquerda + direita) // 2
        if nomes[meio] < termo:
            esquerda = meio + 1
        else:
            direita = meio
    inicio_prefixo = esquerda  # possível início dos que têm o prefixo

    #Coletar todos os itens consecutivos que começam com o prefixo
    resultados = []
    indice = inicio_prefixo
    while indice < n:
        nome = nomes[indice]
        if nome.startswith(termo):
            resultados.append(ordenada[indice])
            indice += 1
        else:
            break  # Sai ao primeiro que não corresponde (região contígua acabou)

    if resultados:
        return resultados  # Encontrou via prefixo (mais eficiente)
    
    # 4. Fallback: usar busca_linear (substring em qualquer posição)
    return busca_linear(lista, termo, field=field)
