import blog_xml
import catalogue_xml
import category_xml
import ech_xml
import convert_xml
import sitemap_general_xml
import sitemap_xml
import send_email

def run():

        blog_xml.read_query()
        catalogue_xml.read_query()
        category_xml.read_query()
        ech_xml.read_query()
        convert_xml.read_query()
        sitemap_general_xml.read_query()
        sitemap_xml.read_query()
        send_email.send_email()

    
if __name__ == '__main__':
    run()