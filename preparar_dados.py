"""Prepara os dados do dashboard Vendas x Metas.
Lê os arquivos de dados (Vendas.xlsx, Metas.xlsx, Subcategoria.json, Localizacao.csv)
e atualiza os dados embutidos no index.html (agregados por Ano, Mês, Subcategoria e Continente).
Uso (na pasta do repositório):  python preparar_dados.py
Requer: pip install pandas openpyxl
"""
import sys, re, csv, json
import pandas as pd

P = (sys.argv[1] if len(sys.argv) > 1 else '.').rstrip('/') + '/'
def achar(nome):
    import glob
    return sorted(glob.glob(P + '*' + nome))[0]

# Vendas (cabeçalho na linha 6 da planilha)
v = pd.read_excel(achar('Vendas.xlsx'), header=5).dropna(subset=['Data Venda'])
v['Faturamento'] = v['Preço Unitário'] * v['Quantidade'] - v['Valor Desconto']
v['Custo'] = v['Custo Unitário'] * v['Quantidade']

# Subcategoria / Categoria
sub = pd.DataFrame(json.load(open(achar('Subcategoria.json'), encoding='utf-8')))

# Localização -> Continente (o continente vem nas linhas "Continente:")
loc, cont = [], None
for r in csv.reader(open(achar('Localizacao.csv'), encoding='utf-8-sig'), delimiter=';'):
    if not r or not r[0].strip(): continue
    if r[0].startswith('Continente'): cont = r[1].strip(); continue
    if r[0].strip().isdigit(): loc.append((int(r[0]), r[4].strip(), cont))
loc = pd.DataFrame(loc, columns=['ID Cidade', 'Pais', 'Continente'])

v = v.merge(sub, left_on='ID Subcategoria', right_on='idSubcategoria').merge(loc, on='ID Cidade')
v['Ano'] = v['Data Venda'].dt.year; v['Mes'] = v['Data Venda'].dt.month

# Metas (uma aba por ano: categorias nas linhas, continentes nas colunas)
metas = []
for ano in ['2017', '2018', '2019']:
    d = pd.read_excel(achar('Metas.xlsx'), sheet_name=ano, header=1).rename(columns={f'Ano: {ano}': 'Categoria'})
    d = d[d.Categoria != 'Total'].melt(id_vars='Categoria', var_name='Continente', value_name='Meta')
    d['Ano'] = int(ano); metas.append(d)
metas = pd.concat(metas)

subs = sorted(v.Subcategoria.unique()); conts = sorted(v.Continente.unique())
cat_of = dict(zip(sub.Subcategoria, sub.Categoria))
g = v.groupby(['Ano', 'Mes', 'Subcategoria', 'Continente']).agg(f=('Faturamento', 'sum'), c=('Custo', 'sum'), q=('Quantidade', 'sum'), n=('No. Venda', 'nunique')).reset_index()
out = {
  'atualizado': str(v['Data Venda'].max().date()),
  'subs': subs, 'cats': {s: cat_of[s] for s in subs}, 'conts': conts,
  'vendas': [[int(r.Ano), int(r.Mes), subs.index(r.Subcategoria), conts.index(r.Continente), round(r.f, 2), round(r.c, 2), int(r.q), int(r.n)] for r in g.itertuples()],
  'metas': [[int(r.Ano), r.Categoria, r.Continente, round(float(r.Meta), 2)] for r in metas.itertuples()],
}
json.dump(out, open('dados.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('dados.json gerado:', len(out['vendas']), 'linhas de vendas,', len(out['metas']), 'metas')

# Atualiza a linha "const D = ..." do index.html com os dados novos
linhas = open('index.html', encoding='utf-8').read().split('\n')
linhas = ['const D = ' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';' if l.startswith('const D = ') else l for l in linhas]
open('index.html', 'w', encoding='utf-8').write('\n'.join(linhas))
print('index.html atualizado')
