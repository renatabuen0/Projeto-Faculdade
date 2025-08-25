import json
from flask import Flask, render_template, request

app = Flask(__name__)

#lista de musicas
_musicas_path = Path(__file__).resolve().parent / "static" / "musicas.json"
try:
    with _musicas_path.open("r", encoding="utf-8") as f:
        musicas = json.load(f)
    if not isinstance(musicas, list):
        musicas = []
except (FileNotFoundError, json.JSONDecodeError):
    musicas = []
# (mantenha suas funções bubble_sort, busca_linear, busca_binaria como estão)
#funcoes 
def bubble_sort(lista):
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista[j]["nome"] > lista[j+1]["nome"]:
                lista[j], lista[j+1] = lista[j+1], lista[j]
    return lista
def busca_linear(lista, nome_procurado):
    nome_procurado_minusculo = nome_procurado.lower()
    for item in lista:
        if item["nome"].lower() == nome_procurado_minusculo:
            return item
    return None
def busca_binaria(lista, nome_procurado):
    baixo = 0
    alto = len(lista) - 1
    while baixo <= alto:
        meio = (baixo + alto) // 2
        item_do_meio = lista[meio]["nome"]
        if item_do_meio == nome_procurado:
            return lista[meio]
        elif item_do_meio < nome_procurado:
            baixo = meio + 1
        else:
            alto = meio - 1
    return None

@app.route("/")
def index():
    return render_template("index.html")

#rota para pagina de musica
@app.route("/musicas")
def musicas_page():
    lista_atual=list(musicas)
    ordenar=request.args.get("ordenar")
    if ordenar=="sim":
        lista_atual=bubble_sort(lista_atual)
    nome_busca=request.args.get("nome_busca")
    if nome_busca:
        resultado=busca_linear(lista_atual, nome_busca)
        if resultado:
            lista_atual=[resultado]
        else:
            lista_atual=[]
    return render_template("musicas.html", musicas=lista_atual)
