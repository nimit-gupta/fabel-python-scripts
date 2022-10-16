import pandas as pd
import numpy as np
import requests
import itertools 
from bs4 import BeautifulSoup
from IPython.display import display

def web_scrapping_lenstore_product_name(soup):

    try:

        empty_list = []

        for div_1 in soup.find_all('a', class_ = 'c-product-list__title-link'):
            
            empty_list.append(div_1.get_text().strip())

    except AttributeError:

        empty_list = '0'

    return empty_list

def web_scrapping_lenstore_product_price(soup):

    try:

        empty_list_1 = []

        for div_2 in soup.find_all('div', class_ = 'c-product-list__price'):

            empty_list_1.append(div_2.get_text().strip())

    except AttributeError:

        empty_list_1 = '0'

    return empty_list_1

if __name__ == '__main__':

    url_links = ['https://www.lenstore.co.uk/1-day-acuvue-contact-lenses',
                 'https://www.lenstore.co.uk/acuvue-2-contacts',
                 'https://www.lenstore.co.uk/acuvue-oasys-contacts',
                 'https://www.lenstore.co.uk/air-optix-aqua-contact-lenses',
                 'https://www.lenstore.co.uk/avaira',
                 'https://www.lenstore.co.uk/biofinity-contact-lenses',
                 'https://www.lenstore.co.uk/biomedics',
                 'https://www.lenstore.co.uk/biotrue',
                 'https://www.lenstore.co.uk/clariti-contact-lenses',
                 'https://www.lenstore.co.uk/coopervision-expressions',
                 'https://www.lenstore.co.uk/focus-dailies',
                 'https://www.lenstore.co.uk/frequency',
                 'https://www.lenstore.co.uk/freshlook-contact-lenses',
                 'https://www.lenstore.co.uk/myday',
                 'https://www.lenstore.co.uk/proclear-contact-lenses',
                 'https://www.lenstore.co.uk/purevision-contact-lenses',
                 'https://www.lenstore.co.uk/soflens',
                 'https://www.lenstore.co.uk/blink-eye-drops',
                 'https://www.lenstore.co.uk/revitalens',
                 'https://www.lenstore.co.uk/opti-free-solutions',
                 'https://www.lenstore.co.uk/renu-solutions',
                 'https://www.lenstore.co.uk/macushield',
                 'https://www.lenstore.co.uk/hycosan',
                 'https://www.lenstore.co.uk/optrex',
                 'https://www.lenstore.co.uk/biotrue-solution',
                 'https://www.lenstore.co.uk/alcon',
                 'https://www.lenstore.co.uk/coopervision-solutions',
                 'https://www.lenstore.co.uk/solo-care-aqua',
                 'https://www.lenstore.co.uk/systane-eye-drops',
                ]

    empty_list_2 = [ ]

    empty_list_3 = [ ]

    for links in url_links:

        response = requests.get(links)

        soup = BeautifulSoup(response.text, 'html.parser')

        empty_list_2.append(web_scrapping_lenstore_product_name(soup))

        empty_list_3.append(web_scrapping_lenstore_product_price(soup))

    #display(empty_list_2)

    #display(empty_list_3)

    merged_1 = list(itertools.chain.from_iterable(empty_list_2))

    merged_2 = list(itertools.chain.from_iterable(empty_list_3))

    display(merged_1)

    display(merged_2)

    df = pd.DataFrame.from_dict(
                      { 
                       'Product_Name'  : merged_1,
                       'Product_Prices' : merged_2
                      }, orient='index'

                     )

    df = df.transpose()

    display(df)

    df.to_excel(r'C:\Users\Nimit\Desktop\webscraplenstore001.xlsx')