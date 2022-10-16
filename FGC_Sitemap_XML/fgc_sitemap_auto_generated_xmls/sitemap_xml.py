import pandas as pd
from lxml import etree as et
from IPython.core.display import display

def read_query():

    df = pd.DataFrame({'loc':[ 
                              'https://www.feelgoodcontacts.com/sitemap_category.xml',
                              ' https://www.feelgoodcontacts.com/sitemap_products.xml',
                              'https://www.feelgoodcontacts.com/sitemap_general.xml',
                              'https://www.feelgoodcontacts.com/sitemap_catalogue.xml',
                              ' https://www.feelgoodcontacts.com/sitemap_blog.xml',
                              ' https://www.feelgoodcontacts.com/sitemap_ech.xml'
                                  
                            ]
                  
                      })


    url = "http://www.sitemaps.org/schemas/sitemap/0.9"

    root = et.Element("sitemapindex", nsmap={None:url})

    for row in df.iterrows():
        url = et.SubElement(root,'sitemap')
        loc = et.SubElement(url, 'loc')
        loc.text = str(row[1]['loc'])
      
    result = et.tostring(root, pretty_print=True, xml_declaration=True, encoding='utf-8').decode('utf-8')

    display(result)

    tree = et.ElementTree(root)
    tree.write(r"D:\Python_Deployments\FGC_Sitemap_XML\fgc_sitemap_auto_generated_xmls\auto_generated_xmls\sitemap.xml")

    