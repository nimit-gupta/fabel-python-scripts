#!/usr/bin/env python39 python310
#coding = utf-8
from IPython.core.display import display
from lxml import etree as et
import pandas as pd
import product_xml

def read_query():

    df = product_xml.read_scripts()

    df.insert(1, 'ChangeFreq', 'weekly')

    df.insert(2, 'Priority', 0.9)

    df.rename(columns = {'Product_Link': 'URL', 'Product_Img' : 'Image', 'Product_title': 'Title'}, inplace = True)

    url_1 = "http://www.sitemaps.org/schemas/sitemap/0.9"

    url_2 = "http://www.google.com/schemas/sitemap-image/1.1"

    root = et.Element("urlset", nsmap={None : url_1,"image" : url_2})

    for row in df.iterrows():
        url = et.SubElement(root, 'url')
        loc = et.SubElement(url, 'loc')
        #lastmod = et.SubElement(url, 'lastmod')
        changefreq = et.SubElement(url, 'changefreq')
        priority = et.SubElement(url,'priority') 
        image = et.SubElement(url,'{http://www.google.com/schemas/sitemap-image/1.1}image')
        imageloc = et.SubElement(image,'{http://www.google.com/schemas/sitemap-image/1.1}loc')
        imagetitle = et.SubElement(image,'{http://www.google.com/schemas/sitemap-image/1.1}title')
        loc.text = str(row[1]['URL'])
        #lastmod.text = str(row[1]['LastMod'])
        changefreq.text = str(row[1]['ChangeFreq'])
        priority.text = str(row[1]['Priority'])
        imageloc.text = str(row[1]['Image'])
        imagetitle.text = str(row[1]['Title'])

    result = et.tostring(root, pretty_print=True, xml_declaration=True, encoding='utf-8').decode('utf-8')

    display(result)

    tree = et.ElementTree(root)

    tree.write(r"D:\Python_Deployments\FGC_Sitemap_XML\fgc_sitemap_auto_generated_xmls\auto_generated_xmls\sitemap_products.xml")


