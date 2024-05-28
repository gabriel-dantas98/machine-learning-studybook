import logging
import requests
from typing import Any
from fastapi import APIRouter
from bs4 import BeautifulSoup
from utils import scraping

router = APIRouter()

@router.get("/")
def download() -> Any:
    logging.info("Running download...")
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

        logging.info("Getting data from:", url)
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
        else:
            logging.error('Failed when loading html:', response.status_code)

        scraping.get_download_csv_link(soup, base_url)

    return "Download CSV files from site done!"
