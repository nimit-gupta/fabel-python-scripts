import pandas as pd
from lxml import etree as et
from IPython.core.display import display

def read_query():

        df = pd.DataFrame({
                            'loc' : [ 
                                        'https://www.feelgoodcontacts.com/',
                                        'https://www.feelgoodcontacts.com/information/reason-to-feelgood',
                                        'https://www.feelgoodcontacts.com/price-match-guarantee',
                                        'https://www.feelgoodcontacts.com/guide-to-astigmatism',
                                        'https://www.feelgoodcontacts.com/contact-lens-specifications',
                                        'https://www.feelgoodcontacts.com/auto-replenish',
                                        'https://www.feelgoodcontacts.com/contact-us',
                                        'https://www.feelgoodcontacts.com/information/shipping',
                                        'https://www.feelgoodcontacts.com/help',
                                        'https://www.feelgoodcontacts.com/competition',
                                        'https://www.feelgoodcontacts.com/promotion',
                                        'https://www.feelgoodcontacts.com/introductory-offer',
                                        'https://www.feelgoodcontacts.com/manufacturer-guides',
                                        'https://www.feelgoodcontacts.com/student-discount',
                                        'https://www.feelgoodcontacts.com/mobile-app',
                                        'https://www.feelgoodcontacts.com/cookie-disclaimer',
                                        'https://www.feelgoodcontacts.com/press-hub',
                                        'https://www.feelgoodcontacts.com/driving-blind',
                                        'https://www.feelgoodcontacts.com/tools/vision-simulator',
                                        'https://www.feelgoodcontacts.com/about-us/careers',
                                        'https://www.feelgoodcontacts.com/information/trustpilot-reviews',
                                        'https://www.feelgoodcontacts.com/optical-advice-login',
                                        'https://www.feelgoodcontacts.com/information/reward-points',
                                        'https://www.feelgoodcontacts.com/for-our-heroes',
                                        'https://www.feelgoodcontacts.com/help/privacy-policy',
                                        'https://www.feelgoodcontacts.com/blog/christmas-challenges',
                                        'https://www.feelgoodcontacts.com/screen-time-countries',
                                        'https://www.feelgoodcontacts.com/information/click-collect',
                                        'https://www.feelgoodcontacts.com/information/refer-a-friend',
                                        'https://www.feelgoodcontacts.com/manufacturer-guides/air-optix',
                                        'https://www.feelgoodcontacts.com/information/refund-returns-policy',
                                        'https://www.feelgoodcontacts.com/information/secure-online-shopping',
                                        'https://www.feelgoodcontacts.com/uni-days-student-discount',
                                        'https://www.feelgoodcontacts.com/help/privacy-policy-history',
                                        'https://www.feelgoodcontacts.com/information/contact-lens-care',
                                        'https://www.feelgoodcontacts.com/optician/specsavers-contact-lenses',
                                        'https://www.feelgoodcontacts.com/information/terms-and-condition',
                                        'https://www.feelgoodcontacts.com/free-contact-lens-replacement'

                                    ]
                    
                        })

        df['changefreq'] = 'monthly'

        df['priority'] = 0.4

        df.loc[df['loc'] == 'https://www.feelgoodcontacts.com/', 'priority'] = 1

        df.loc[df['loc'] == 'https://www.feelgoodcontacts.com/', 'changefreq'] = 'daily'

        df.loc[df['loc'] == 'https://www.feelgoodcontacts.com/information/reason-to-feelgood', 'priority'] = 0.5

        df.loc[df['loc'] == 'https://www.feelgoodcontacts.com/price-match-guarantee', 'priority'] = 0.5

        df.loc[df['loc'] == 'https://www.feelgoodcontacts.com/guide-to-astigmatism', 'priority'] = 0.5

        df.loc[df['loc'] == 'https://www.feelgoodcontacts.com/contact-lens-specifications', 'priority'] = 0.5

        df.loc[df['loc'] == 'https://www.feelgoodcontacts.com/auto-replenish', 'priority'] = 0.5

        df.loc[df['loc'] == 'https://www.feelgoodcontacts.com/contact-us', 'priority'] = 0.5

        df.loc[df['loc'] == 'https://www.feelgoodcontacts.com/information/shipping', 'priority'] = 0.5

        df.loc[df['loc'] == 'https://www.feelgoodcontacts.com/help', 'priority'] = 0.5

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

        tree.write(r"D:\Python_Deployments\FGC_Sitemap_XML\fgc_sitemap_auto_generated_xmls\auto_generated_xmls\sitemap_general.xml")