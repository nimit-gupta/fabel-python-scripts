from IPython.core.display import display
from lxml import etree as et
import pandas as pd
import pymssql


def read_query():

    con = pymssql.connect(

                          host = r'217.174.248.81',
                          port = 49559,
                          user = r'DevUser3',
                          password = r'flgT!9585',
                          database = r'feelgood.live'
                         )

    sql = '''
             SELECT 
                  CONCAT('https://www.feelgoodcontacts.com/eye-care-hub/', EyeCareHubPageName) AS loc
             FROM 
                  FG_CmsEyeCareHub 
             WHERE 
                  Enable = 1 
                  AND CurrencyID = 1
                  AND EyeCareHubPageName NOT LIKE 'https://%'
          '''

    df = pd.read_sql_query(sql, con)

    df['changefreq'] = 'monthly'

    df['priority'] = 0.7

    df.sort_values(by = 'priority', ascending = False, inplace = True)

    url = "http://www.sitemaps.org/schemas/sitemap/0.9"

    root = et.Element("urlset", nsmap={None:url})

    for row in df.iterrows():

        url = et.SubElement(root, 'url')

        loc = et.SubElement(url, 'loc')

        changefreq = et.SubElement(url, 'changefreq')

        priority = et.SubElement(url,'priority') 
        
        loc.text = str(row[1]['loc'])

        changefreq.text = str(row[1]['changefreq'])

        priority.text = str(row[1]['priority'])
        

    result = et.tostring(root, pretty_print=True, xml_declaration=True, encoding='utf-8').decode('utf-8')

    display(result)

    tree = et.ElementTree(root)

    tree.write(r"D:\Python_Deployments\FGC_Sitemap_XML\fgc_sitemap_auto_generated_xmls\auto_generated_xmls\sitemap_ech.xml")

if __name__ == '__main__':
    read_query()