from main import app
from models import musicas, produtos, bubble_sort, busca_linear, busca_binaria
from flask import render_template, request

@app.route('/')
def home():
    return render_template('homepage.html')


@app.route("/musicas", endpoint="musicas")
def musicas_view():
    """Página de músicas com controles de busca e ordenação (similar a crafts).
    Query params:
      q: termo de busca (substring em 'nome')
      metodo: 'linear' | 'binaria'
      ordenacao: 'nome_asc' | 'nome_desc'
    """
    q = request.args.get('q', '').strip()
    metodo = request.args.get('metodo', 'linear')
    ordenacao = request.args.get('ordenacao', 'nome_asc')

    base = list(musicas)

    # Ordenação por nome
    if ordenacao == 'nome_desc':
        lista = sorted(base, key=lambda x: x.get('nome', '').lower(), reverse=True)
    else:  # default asc
        lista = sorted(base, key=lambda x: x.get('nome', '').lower())

    resultados = lista

    # Funções de busca locais para musicas (baseadas em campo 'nome')
    def busca_linear_musicas(lst, termo):
        alvo = termo.lower()
        return [m for m in lst if alvo in m.get('nome', '').lower()]

    def busca_binaria_musicas(lst, termo):
        alvo = termo.lower()
        if not alvo:
            return []
        ordenada = sorted(lst, key=lambda x: x.get('nome', '').lower())
        low, high = 0, len(ordenada) - 1
        found = -1
        while low <= high:
            mid = (low + high) // 2
            mid_nome = ordenada[mid].get('nome', '').lower()
            if alvo in mid_nome:
                found = mid
                break
            if mid_nome < alvo:
                low = mid + 1
            else:
                high = mid - 1
        if found == -1:
            return []
        res = []
        i = found
        while i >= 0:
            nome = ordenada[i].get('nome', '').lower()
            if alvo in nome:
                res.insert(0, ordenada[i])
                i -= 1
            else:
                break
        i = found + 1
        while i < len(ordenada):
            nome = ordenada[i].get('nome', '').lower()
            if alvo in nome:
                res.append(ordenada[i])
                i += 1
            else:
                break
        return res

    # Aplicar busca
    if q:
        if metodo == 'binaria':
            resultados = busca_binaria_musicas(lista, q)
        else:
            resultados = busca_linear_musicas(lista, q)

    return render_template(
        'musicas.html',
        musicas=resultados,
        q=q,
        metodo=metodo,
        ordenacao=ordenacao,
        total=len(resultados)
    )


@app.route('/crafts')
def crafts():
    q = request.args.get('q', '').strip()
    metodo = request.args.get('metodo', 'linear')
    ordenacao = request.args.get('ordenacao', 'price_asc')

    base = list(produtos)

    # ordenação
    if ordenacao == 'price_asc':
        lista = bubble_sort(base)
    elif ordenacao == 'price_desc':
        lista = bubble_sort(base)[::-1]
    elif ordenacao == 'name_asc':
        lista = sorted(base, key=lambda x: x['name'].lower())
    elif ordenacao == 'name_desc':
        lista = sorted(base, key=lambda x: x['name'].lower(), reverse=True)
    else:   
        lista = base

    resultados = lista

    
    # busca (match exato pelo name)
    if q:
        if metodo == 'binaria':
            resultados = busca_binaria(produtos, q)   # sua função já ordena internamente por name
        else:
            resultados = busca_linear(produtos, q)
        resultados = resultados if resultados else []

    return render_template(
        'crafts.html',
        produtos=resultados,
        q=q, metodo=metodo, ordenacao=ordenacao,
        total=len(resultados)
    )

# Product page route
@app.route('/product/<product_name>')
def product_page(product_name):
    # Buscar produto na base (ajuste conforme sua estrutura)
    alvo = product_name.strip().lower()
    produto = next((p for p in produtos if p.get('name', '').strip().lower() == alvo), None)
    if not produto:
        return render_template('productpage.html', not_found=True, product_name=product_name)

    return render_template(
        'productpage.html',
        product_name=produto.get('name', ''),
        product_img=produto.get('img', ''),
        product_desc=produto.get('description', 'Produto artesanal, feito com carinho e qualidade.'),
        product_price=produto.get('price', 0.0),
        not_found=False                      
    )