import pandas as pd
from lxml import etree as et
from IPython.core.display import display

def read_query():

        df = pd.DataFrame({
                            'loc' : [   
                                        'https://www.feelgoodcontacts.com/contact-lenses',
                                        'https://www.feelgoodcontacts.com/solutions',
                                        'https://www.feelgoodcontacts.com/eye-care',
                                        'https://www.feelgoodcontacts.com/glasses',
                                        'https://www.feelgoodcontacts.com/sunglasses',
                                        'https://www.feelgoodcontacts.com/blog',
                                        'https://www.feelgoodcontacts.com/contact-lenses/daily-contact-lenses',
                                        'https://www.feelgoodcontacts.com/contact-lenses/monthly-contact-lenses',
                                        'https://www.feelgoodcontacts.com/contact-lenses/two-weekly-contact-lenses',
                                        'https://www.feelgoodcontacts.com/contact-lenses/toric-contact-lenses',
                                        'https://www.feelgoodcontacts.com/contact-lenses/multifocal-contact-lenses',
                                        'https://www.feelgoodcontacts.com/contact-lenses/coloured-contact-lenses',
                                        'https://www.feelgoodcontacts.com/contact-lenses',
                                        'https://www.feelgoodcontacts.com/contact-lenses/cheap-contact-lenses',
                                        'https://www.feelgoodcontacts.com/contact-lenses/extended-wear-contact-lenses',
                                        'https://www.feelgoodcontacts.com/contact-lenses/silicone-hydrogel-contact-lenses',
                                        'https://www.feelgoodcontacts.com/contact-lenses/no-prescription-contact-lenses',
                                        'https://www.feelgoodcontacts.com/solutions/multi-purpose-solutions',
                                        'https://www.feelgoodcontacts.com/solutions/saline-solutions',
                                        'https://www.feelgoodcontacts.com/solutions/peroxide-solutions',
                                        'https://www.feelgoodcontacts.com/solutions/travel-pack-solutions',
                                        'https://www.feelgoodcontacts.com/solutions/rigid-gas-permeable-solutions',
                                        'https://www.feelgoodcontacts.com/solutions/multi-pack-contact-lens-solutions',
                                        'https://www.feelgoodcontacts.com/eye-care/eye-drops',
                                        'https://www.feelgoodcontacts.com/eye-care/eye-accessories',
                                        'https://www.feelgoodcontacts.com/eye-care/dry-eye-treatments',
                                        'https://www.feelgoodcontacts.com/eye-care/supplements-hygiene',
                                        'https://www.feelgoodcontacts.com/face-masks',
                                        'https://www.feelgoodcontacts.com/covid-19-essentials',
                                        'https://www.feelgoodcontacts.com/travel-essentials',
                                        'https://www.feelgoodcontacts.com/seasonal-shop',
                                        'https://www.feelgoodcontacts.com/glasses/shape/aviator',
                                        'https://www.feelgoodcontacts.com/glasses/shape/oval',
                                        'https://www.feelgoodcontacts.com/glasses/shape/rectangle',
                                        'https://www.feelgoodcontacts.com/glasses/shape/round',
                                        'https://www.feelgoodcontacts.com/glasses/shape/square',
                                        'https://www.feelgoodcontacts.com/glasses/shape/wayfarer',
                                        'https://www.feelgoodcontacts.com/glasses/shape/clubmaster',
                                        'https://www.feelgoodcontacts.com/glasses/shape/cat-eye',
                                        'https://www.feelgoodcontacts.com/glasses/shape/butterfly',
                                        'https://www.feelgoodcontacts.com/glasses/shape/hexagonal',
                                        'https://www.feelgoodcontacts.com/sunglasses/frameshape/aviator',
                                        'https://www.feelgoodcontacts.com/sunglasses/frameshape/oval',
                                        'https://www.feelgoodcontacts.com/sunglasses/frameshape/rectangle',
                                        'https://www.feelgoodcontacts.com/sunglasses/frameshape/round',
                                        'https://www.feelgoodcontacts.com/sunglasses/frameshape/square',
                                        'https://www.feelgoodcontacts.com/sunglasses/frameshape/wayfarer',
                                        'https://www.feelgoodcontacts.com/sunglasses/frameshape/wrap',
                                        'https://www.feelgoodcontacts.com/sunglasses/frameshape/clubmaster',
                                        'https://www.feelgoodcontacts.com/sunglasses/frameshape/cat-eye',
                                        'https://www.feelgoodcontacts.com/sunglasses/frameshape/butterfly',
                                        'https://www.feelgoodcontacts.com/sunglasses/frameshape/hexagonal',
                                        'https://www.feelgoodcontacts.com/sunglasses/frameshape/octagonal',
                                        'https://www.feelgoodcontacts.com/sunglasses/frameshape/heart' 

                                    ]
                    
                        })

        df['changefreq'] = 'weekly'

        df['priority'] = 0.9

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

        tree.write(r"D:\Python_Deployments\FGC_Sitemap_XML\fgc_sitemap_auto_generated_xmls\auto_generated_xmls\sitemap_category.xml")