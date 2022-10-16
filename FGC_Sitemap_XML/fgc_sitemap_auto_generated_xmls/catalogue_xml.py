import pandas as pd
from lxml import etree as et
from IPython.core.display import display

def read_query():

        df = pd.DataFrame({
                            'loc' : [ 
                                        'https://www.feelgoodcontacts.com/catalogue/acuvue-contact-lenses',
                                        'https://www.feelgoodcontacts.com/catalogue/air-optix',
                                        'https://www.feelgoodcontacts.com/catalogue/bausch-lomb-contact-lenses',
                                        'https://www.feelgoodcontacts.com/catalogue/biofinity',
                                        'https://www.feelgoodcontacts.com/catalogue/clariti',
                                        'https://www.feelgoodcontacts.com/catalogue/comfi',
                                        'https://www.feelgoodcontacts.com/catalogue/cooper-vision-contact-lenses',
                                        'https://www.feelgoodcontacts.com/catalogue/focus-dailies',
                                        'https://www.feelgoodcontacts.com/catalogue/freshlook',
                                        'https://www.feelgoodcontacts.com/catalogue/aosept',
                                        'https://www.feelgoodcontacts.com/catalogue/boston',
                                        'https://www.feelgoodcontacts.com/catalogue/easysept',
                                        'https://www.feelgoodcontacts.com/catalogue/ote-optics',
                                        'https://www.feelgoodcontacts.com/catalogue/renu',
                                        'https://www.feelgoodcontacts.com/catalogue/biotrue',
                                        'https://www.feelgoodcontacts.com/catalogue/comfi',
                                        'https://www.feelgoodcontacts.com/catalogue/opti-free',
                                        'https://www.feelgoodcontacts.com/catalogue/oxysept',
                                        'https://www.feelgoodcontacts.com/catalogue/total-care',
                                        'https://www.feelgoodcontacts.com/catalogue/hycosan',
                                        'https://www.feelgoodcontacts.com/catalogue/altacor',
                                        'https://www.feelgoodcontacts.com/catalogue/biotrue',
                                        'https://www.feelgoodcontacts.com/catalogue/comfi',
                                        'https://www.feelgoodcontacts.com/catalogue/the-body-doctor',
                                        'https://www.feelgoodcontacts.com/catalogue/artelac',
                                        'https://www.feelgoodcontacts.com/catalogue/blink',
                                        'https://www.feelgoodcontacts.com/catalogue/systane',
                                        'https://www.feelgoodcontacts.com/catalogue/optase',
                                        'https://www.feelgoodcontacts.com/glasses/brand/calvin-klein',
                                        'https://www.feelgoodcontacts.com/glasses/brand/dkny',
                                        'https://www.feelgoodcontacts.com/glasses/brand/gucci',
                                        'https://www.feelgoodcontacts.com/glasses/brand/lacoste',
                                        'https://www.feelgoodcontacts.com/glasses/brand/marc-jacobs',
                                        'https://www.feelgoodcontacts.com/glasses/brand/oakley',
                                        'https://www.feelgoodcontacts.com/glasses/brand/persol',
                                        'https://www.feelgoodcontacts.com/glasses/brand/polo-ralph-lauren',
                                        'https://www.feelgoodcontacts.com/glasses/brand/radley',
                                        'https://www.feelgoodcontacts.com/glasses/brand/superdry',
                                        'https://www.feelgoodcontacts.com/glasses/brand/versace',
                                        'https://www.feelgoodcontacts.com/glasses/brand/chloe',
                                        'https://www.feelgoodcontacts.com/glasses/brand/feel-good-collection',
                                        'https://www.feelgoodcontacts.com/glasses/brand/hugo-boss',
                                        'https://www.feelgoodcontacts.com/glasses/brand/le-specs',
                                        'https://www.feelgoodcontacts.com/glasses/brand/maxmara',
                                        'https://www.feelgoodcontacts.com/glasses/brand/oneill',
                                        'https://www.feelgoodcontacts.com/glasses/brand/polaroid',
                                        'https://www.feelgoodcontacts.com/glasses/brand/prada',
                                        'https://www.feelgoodcontacts.com/glasses/brand/ray-ban',
                                        'https://www.feelgoodcontacts.com/glasses/brand/tommy-hilfiger',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/calvin-klein',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/dolce-gabbana',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/giorgio-armani',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/jimmy-choo',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/le-specs',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/oakley',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/persol',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/prada',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/saint-laurent',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/taylor-morris',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/victoria-beckham',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/carrera',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/dunlop',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/gucci',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/kendall-kylie',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/linda-farrow',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/oneill',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/polaroid',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/radley',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/sunpocket',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/tommy-hilfiger',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/vogue',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/chloe',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/feel-good-collection',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/hugo-boss',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/lacoste',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/michael-kors',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/oxydo',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/police',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/ray-ban',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/superdry',
                                        'https://www.feelgoodcontacts.com/sunglasses/brand/versace'

                                    ]
                    
                        })

        df['changefreq'] = 'monthly'

        df['priority'] = 0.8

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

        tree.write(r"D:\Python_Deployments\FGC_Sitemap_XML\fgc_sitemap_auto_generated_xmls\auto_generated_xmls\sitemap_catalogue.xml")