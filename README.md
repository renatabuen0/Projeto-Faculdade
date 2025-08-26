# Aplicação de busca linear/binária com bubble sort - ESTRUTURA DE DADOS
# Renata Cibelle / Ian Monteiro 

# Os sete casos do gráfico de Big-O: https://colab.research.google.com/drive/1VhsHbQ6Je1qntE3dovoQyAdNI6zxsI2_?usp=sharing


Aplicação Flask didática que demonstra:
- Carregamento de dados estruturados (JSON)
- Ordenação customizada (Bubble Sort) para reforçar conceitos de algoritmos
- Busca linear (substring, case-insensitive)
- Busca "binária" adaptada para prefixos (com fallback para substring geral)
- Duas áreas: produtos artesanais (Crafts) e músicas com player de áudio fixo

Foco pedagógico: clareza do código sobre performance.

## Sumário
- [Tecnologias](#tecnologias)
- [Estrutura de Pastas](#estrutura-de-pastas)
- [Funcionalidades](#funcionalidades)
- [Algoritmos de Busca e Ordenação](#algoritmos-de-busca-e-ordenação)
- [Rotas](#rotas)
- [Instalação](#instalação)
- [Execução](#execução)
- [Parâmetros de Query](#parâmetros-de-query)
- [Formato dos Dados](#formato-dos-dados)
- [Personalização](#personalização)
- [Melhorias Futuras](#melhorias-futuras)

## Tecnologias
- Python 3.10+
- Flask
- HTML / CSS (layout responsivo, grid, player de áudio)
- JSON para persistência simples

## Estrutura de Pastas
```
Projeto-Faculdade/
  main.py (ponto de entrada flask, importa app)
  views.py (rotas)
  models.py (carregamento de dados + algoritmos)
  requirements.txt
  static/
    style.css
    produtos.json
    musicas.json
    *.mp3 / *.mp4 / imagens
  templates/
    homepage.html
    crafts.html
    musicas.html
    productpage.html
```

## Funcionalidades
- Homepage com escolha entre "Crafts" e "Músicas" (cards com vídeo / imagem)
- Listagem de produtos com ordenação por preço ou nome
- Listagem de músicas com ordenação por nome
- Busca:
  - Linear: substring em qualquer parte do texto
  - Binária (adaptada): rápida para prefixos, correta via fallback para substring
- Player de áudio global (sticky) na parte inferior
- Placeholder para itens sem capa
- Tema escuro consistente (variáveis CSS)
- Manifest e ícones básicos (favicon / PWA simples)

## Algoritmos de Busca e Ordenação
Implementados em `models.py`:

### bubble_sort(lista, key=None, reverse=False)
- Implementação didática; ordena in-place.
- Usa `key` customizável (por padrão tenta `price`).
- Otimização: interrompe quando nenhuma troca ocorre em um ciclo.

### busca_linear(lista, termo, field="name")
- Percorre todos os itens e retorna aqueles cujo campo contém o termo (substring, case-insensitive).
- Útil como fallback universal.

### busca_binaria(lista, termo, field="name")
- Ordena uma cópia da lista pelo campo.
- Executa busca binária para localizar o primeiro índice onde `valor >= termo`.
- Coleta sequência contígua de itens cujo campo começa com o prefixo (`startswith`).
- Se não houver matches de prefixo, faz fallback para busca_linear (garantindo substring no meio).
- Observação: busca binária clássica não resolve substring arbitrária (apenas prefixos são contíguos em ordem lexicográfica).

## Rotas
| Rota | Descrição |
|------|-----------|
| `/` | Homepage com escolha de categoria |
| `/crafts` | Lista de produtos com busca e ordenação |
| `/musicas` | Lista de músicas com player e filtros |
| `/product/<product_name>` | Página individual de produto |

## Instalação
1. Clone ou baixe o repositório.
2. (Opcional, recomendado) Crie um ambiente virtual:
   - Windows PowerShell:
     ```powershell
     python -m venv .venv; .venv\\Scripts\\Activate.ps1
     ```
   - Linux / macOS:
     ```bash
     python -m venv .venv
     source .venv/bin/activate
     ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Execução
```bash
python main.py
```
Abra no navegador: http://localhost:5000

## Parâmetros de Query
### /crafts
- `q`: termo de busca (substring ou prefixo, conforme método)
- `metodo`: `linear` | `binaria`
- `ordenacao`: `price_asc` | `price_desc` | `name_asc` | `name_desc`

### /musicas
- `q`: termo de busca (substring ou prefixo)
- `metodo`: `linear` | `binaria`
- `ordenacao`: `nome_asc` | `nome_desc`

## Formato dos Dados
### Produto (`produtos.json`)
```json
{
  "name": "Bolsa artesanal",
  "price": 79.9,
  "img": "img/bolsa.jpg",
  "description": "Descrição opcional"
}
```

### Música (`musicas.json`)
```json
{
  "nome": "Frenesi",
  "artista": "Artista X",
  "caminho_arquivo": "frenesi.mp3",
  "capa": "frenesi.jpg"
}
```
Campos obrigatórios: `nome`, `caminho_arquivo`. Capa é opcional.

## Personalização
- Cores: alterar variáveis em `:root` (`static/style.css`).
