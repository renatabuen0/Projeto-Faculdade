from main import app
from models import produtos, bubble_sort, busca_linear, busca_binaria
from flask import render_template, request

@app.route('/')
def home():
    return render_template('homepage.html')

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