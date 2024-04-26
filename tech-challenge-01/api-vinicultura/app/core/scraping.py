import requests
from bs4 import BeautifulSoup

YEARS = list(range(1970, 2023))
# http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02
# Estrutura dos dados
#
# Produção - opt_02
# 
# Processamento - opt_03
#   Subprodutos 
#     Viniferas, Americanas e hibridas, Uvas de mesa, sem classificação
# Comercialização - opt_04
#
# Importação - opt_05
# Exportação - opt_06

def get_download_csv_link(soup):
  
  content_footer = soup.find('a', class_='footer_content')
  csv_url = content_footer.get('href')
  csv_filename = csv_url.split('/')[-1]
  full_csv_url = f'{base_url}/{csv_url}'

  print('Downloading:', full_csv_url)
  response = requests.get(full_csv_url)

  if response.status_code == 200:
      with open(csv_filename, 'wb') as file:
          file.write(response.content)
      print('Download concluído com sucesso!')
  else:
      print('Falha ao fazer o download:', response.status_code)

def get_table_content(soup):

  tables = soup.find_all('table')
  for table in tables:
      rows = table.find_all('tr')
      for row in rows:
          cols = row.find_all('td')
          cols = [col.text.strip() for col in cols]


categories = {
    'opt_02': 'Produção',
    'opt_03': 'Processamento',
    'opt_04': 'Comercialização',
    'opt_05': 'Importação',
    'opt_06': 'Exportação',
}

base_url = 'http://vitibrasil.cnpuv.embrapa.br'

for category_key in categories.keys():

  url = f'{base_url}/index.php?opcao={category_key}'
  
  print("Getting data from:", url)
  response = requests.get(url)

  if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
  else:
    print('Falha ao obter a página:', response.status_code)

  
  get_download_csv_link(soup)
