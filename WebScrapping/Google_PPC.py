import pandas as pd
import numpy as np
import requests
import pymssql
import itertools 
from bs4 import BeautifulSoup
from IPython.display import display

def web_scrapping_google_ads_product_name(soup):
     
    try:
        
        product_name = []
        
        for div_1 in soup.find_all('span', class_ = 'pymv4e'):
            product_name.append(div_1.get_text().strip())
    
    except AttributeError:
        
        product_name = ' '
        
    return product_name

def web_scrapping_google_ads_product_price(soup):
             
    try:
        
        product_price = []

        for div_2 in soup.find_all('div', class_ = 'qptdjc'):
            product_price.append(div_2.get_text().strip())

    except AttributeError:

        product_price = ' '
            
    return product_price

def web_scrapping_google_ads_product_manufacturer(soup):
     
    try:
        
        product_manufacturer = []
        
        for div_3 in soup.find_all('span', class_ = 'zPEcBd LnPkof'):
            product_manufacturer.append(div_3.get_text().strip())
            
    except AttributeError:

        product_manufacturer = ' '
            
    return product_manufacturer
        

if __name__ == '__main__':
    
    headers = {
               "User-Agent":
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3538.102 Safari/537.36 Edge/18.19582"
              }

    
    con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585',database = r'feelgood.live')
    
    sql = '''
             SELECT 
                   PD.NAME NAME
             FROM 
                  [feelgood.live].dbo.FG_Product PN 
             INNER JOIN 
                   [feelgood.live].dbo.FG_ProductDescription PD ON (PN.ProductId = PD.ProductId)
             WHERE 
                   PN.Enable = 1 
                   AND PN.Discontinued = 0
          
          '''
    
    df = pd.read_sql_query(sql, con)
    
    product_list = []
    
    for x in df['NAME'].str.replace(" ", "+"):
        
        product_list.append(x)
        
    
    '''
    google_links = []
    
    for y in product_list:
        
        google_links.append('https://www.google.com/search?q='+ y)
        
    display(google_links)
    
    '''
        
    product_name_1 = []
    
    product_price_1 = []
    
    product_manufacturer_1 = []
    
    #for google_search_url in product_list[0:50]:
    
    for google_search_url in product_list:
        
        response = requests.get('https://www.google.com/search?q=' + google_search_url, headers = headers)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        product_name_1.append(web_scrapping_google_ads_product_name(soup))
        
        product_price_1.append(web_scrapping_google_ads_product_price(soup))
        
        product_manufacturer_1.append(web_scrapping_google_ads_product_manufacturer(soup))
        
    display(product_name_1)
    
    display(product_price_1)
    
    display(product_manufacturer_1)
    
    merged_1 = list(itertools.chain.from_iterable(product_name_1))

    merged_2 = list(itertools.chain.from_iterable(product_price_1))
    
    merged_3 = list(itertools.chain.from_iterable(product_manufacturer_1))
    
    df = pd.DataFrame.from_dict({
                        'Product Name': merged_1,
                        'Product Price' : merged_2,
                        'Product Manufacturer' : merged_3
    
                     }, orient = 'index')
    display(df.transpose())