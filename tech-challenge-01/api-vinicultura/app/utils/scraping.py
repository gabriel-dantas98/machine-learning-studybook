import requests

def get_download_csv_link(soup, base_url):
  
  content_footer = soup.find('a', class_='footer_content')
  csv_url = content_footer.get('href')
  csv_filename = csv_url.split('/')[-1]
  full_csv_url = f'{base_url}/{csv_url}'

  print('Downloading:', full_csv_url)

  response = requests.get(full_csv_url)

  if response.status_code == 200:
      with open(csv_filename, 'wb') as file:
          file.write(response.content)
      print('Download done!')
  else:
      print('Failed downloading:', full_csv_url, response.status_code)

def get_table_content(soup):

  tables = soup.find_all('table')

  for table in tables:
      rows = table.find_all('tr')
      for row in rows:
          cols = row.find_all('td')
          cols = [col.text.strip() for col in cols]
