from typing import Any
from fastapi import APIRouter
from bs4 import BeautifulSoup
from utils import scraping
import requests
import glob

router = APIRouter()

@router.get("/")
def download() -> Any:
    print("Hey im running download...")
    base_url = 'http://vitibrasil.cnpuv.embrapa.br'
    YEARS = list(range(1970, 2023))
    categories = {
        'opt_02': 'Produção',
        'opt_03': 'Processamento',
        # subopcao=subopt_02&opcao=opt_03
        # subopcao=subopt_03&opcao=opt_03
        'opt_04': 'Comercialização',
        'opt_05': 'Importação',
        # subopcao=subopt_02&opcao=opt_05
        # subopcao=subopt_03&opcao=opt_05
        # subopcao=subopt_04&opcao=opt_05
        # subopcao=subopt_05&opcao=opt_05
        'opt_06': 'Exportação',
    }

    for category_key in categories.keys():

        url = f'{base_url}/index.php?opcao={category_key}'

        print("Getting data from:", url)
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
        else:
            print('Failed when loading html:', response.status_code)

        scraping.get_download_csv_link(soup, base_url)

    return "OK"
    
def populate_database(): 
    return ''
