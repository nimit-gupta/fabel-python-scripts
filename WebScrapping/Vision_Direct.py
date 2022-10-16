import pandas as pd
import numpy as np
import requests
import itertools 
from bs4 import BeautifulSoup
from IPython.display import display


def web_scrapping_vision_direct_product_name(soup_1):
    
    try:
        empty_list_2 = []

        for div_1 in soup_1.find_all('div','products-list__name same-height__name'):
        
            empty_list_2.append(div_1.get_text().strip())

    except AttributeError:

        empty_list_2 = '0'

    return empty_list_2

def web_scrapping_vision_direct_product_price(soup_1):

    try:

       empty_list_3 = []

       for div_2 in soup_1.find_all('div', class_ = 'products-list__prices'):
           
           for div_2_1 in div_2.find('span',class_ = 'price'):
            
               empty_list_3.append(div_2_1.get_text().strip())

    except AttributeError:

        empty_list_3 = '0'

    return empty_list_3

if __name__ == '__main__':

    response = requests.get("https://www.visiondirect.co.uk/all-brands")

    soup = BeautifulSoup(response.text, 'html.parser')

    empty_list = []

    for div_1 in soup.find_all('ul', class_= 'layout'):

        for div_2 in div_1.find_all('li', class_ = 'layout__item +1/3 +1/2-smart-land +1/1-smart'):

            div_3 = div_2.find_all('a')

            empty_list.append(div_3)

    merged = list(itertools.chain.from_iterable(empty_list))


    empty_list_1 = []

    for div_4 in merged:

        empty_list_1.append(div_4.get('href'))


    empty_list_4 = []

    empty_list_5 = []

    empty_list_null = []
    
    for div_5 in empty_list_1:

        if div_5 == 'https://www.visiondirect.co.uk/extreme-h2o':

            empty_list_null.append(div_5)

        else:

           response_1 = requests.get(div_5)

           soup_1 = BeautifulSoup(response_1.text, 'html.parser')

           empty_list_4.append(web_scrapping_vision_direct_product_name(soup_1))

           empty_list_5.append(web_scrapping_vision_direct_product_price(soup_1))

    #display(empty_list_4)

    #display(empty_list_5)

    merged_1 = list(itertools.chain.from_iterable(empty_list_4))

    merged_2 = list(itertools.chain.from_iterable(empty_list_5))

    #display(merged_1)

    #display(merged_2)

    #merged_1 = np.concatenate(empty_list_4)

    #merged_2 = np.concatenate(empty_list_5)

    df = pd.DataFrame.from_dict(
                      { 
                       'Product_Name'  : merged_1,
                       'Product_Prices' : merged_2
                      }, orient='index'

                     )

    df = df.transpose()

    df_copy = df.iloc[0:573,:]

    df_copy.to_excel(r'C:\Users\Nimit\Desktop\webscrap009.xlsx')


    
    
    
