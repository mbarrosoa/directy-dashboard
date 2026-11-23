# Dashboard Vendas x Metas

Dashboard interativo que compara o faturamento com as metas (01/01/2017 a 16/03/2019) e o ano de 2018 com 2017.

**Acesse o dashboard:** https://mbarrosoa.github.io/directy-dashboard/

## Páginas do dashboard
- **Visão geral** – faturamento, meta, % de atingimento, lucro e quantidade, com filtros de ano, continente e categoria. Gráficos de faturamento x meta por ano, continente e categoria, ranking de subcategorias e evolução mensal.
- **Comparativo 2018 x 2017** – variação por categoria, continente e subcategoria, representatividade de cada subcategoria, análise da queda de Desktops e destaques para revisar as metas de 2019.
- **Respostas do case** – as perguntas do desafio respondidas a partir dos dados.

## Arquivos
| Arquivo | Para que serve |
|---|---|
| `index.html` | O dashboard (já contém os dados agregados) |
| `preparar_dados.py` | Lê as bases e atualiza os dados dentro do `index.html` |
| `Vendas.xlsx`, `Metas.xlsx`, `Subcategoria.json`, `Localizacao.csv` | Bases usadas no cálculo |
| `Cliente.xlsx`, `Produto.csv` | Cadastros recebidos no case (referência) |

## Regras de cálculo
- **Faturamento** = Preço Unitário × Quantidade − Valor Desconto
- **Custo** = Custo Unitário × Quantidade · **Lucro bruto** = Faturamento − Custo
- **Continente** vem da Localização (pelo ID Cidade da venda); **Categoria** vem da Subcategoria.
- **Meta** é anual, por Continente e Categoria (abas 2017, 2018 e 2019 do Metas.xlsx). A meta de 2019 é do ano inteiro, mas as vendas vão só até 16/03/2019.

## Como atualizar os dados
```
pip install pandas openpyxl
python preparar_dados.py
```
