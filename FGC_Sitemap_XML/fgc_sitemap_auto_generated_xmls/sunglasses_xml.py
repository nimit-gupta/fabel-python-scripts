#!/usr/bin/env python39 python310
#coding = utf-8
from IPython.core.display import display
from bs4 import BeautifulSoup
from contextlib import suppress
import pandas as pd 
import requests
import pymssql
import itertools

def web_scrap_href(soup):

    try:

        href_list = []

        for html_tag_div in soup.find_all('div', class_ = 'col-lg-4 col-md-4 col-sm-6 col-xs-6 no-padding products-list_item sunglasses'):

            for html_tag_a in html_tag_div.find_all('a', class_ = 'col-lg-12 col-md-12 col-sm-12 col-xs-12 products-list_item-link'):

                href_list.append(html_tag_a.get('href'))

    except AttributeError:

        href_list = ' '

    return href_list

def web_scrap_img(soup):

    try:

        img_list = []

        for html_tag_div in soup.find_all('div', class_ ="col-lg-12 col-md-12 col-sm-12 col-xs-12 products-list_item-image"):

            for html_tag_img in html_tag_div.find_all('img'):

                img_list.append(html_tag_img.get('data-src'))

    except AttributeError:

        img_list = ' '

    return img_list

def web_scrap_title(soup):

    try:

        title_list = []

        for html_tag_div in soup.find_all('div', class_ = 'col-lg-9 col-md-9 col-sm-9 col-xs-12 products-list_item-title'):

            title_list.append(html_tag_div.get_text(strip = True))

    except AttributeError:

        title_list = ' '

    return title_list


def beautiful_soup():

    href_list = []

    img_list = []

    title_list = []
  
    for page_no in range(1, 20):

        response = requests.get("https://www.feelgoodcontacts.com/sunglasses?page=" + str(page_no))

        soup = BeautifulSoup(response.text, "html.parser")

        href_list.append(web_scrap_href(soup))

        img_list.append(web_scrap_img(soup))

        title_list.append(web_scrap_title(soup))

    #print(href_list)

    #print(img_list)

    #print(title_list)

    product_link = list(itertools.chain.from_iterable(href_list))

    product_img = list(itertools.chain.from_iterable(img_list))

    product_title = list(itertools.chain.from_iterable(title_list))

    df = pd.DataFrame.from_dict(
                      { 
                       'Product_Link'  : product_link,
                       'Product_Img' : product_img,
                       'Product_title' : product_title
                      }, orient='index'

                     )

    df_sunglasses = df.transpose()
   
    return df_sunglasses


 

    
