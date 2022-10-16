import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time
import os

def send_email():

        sender = 'reports@feelgoodcontacts.com'

        reciever = ['nimit@fabelservices.net','dip@fabelservices.net']
        

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = ", ".join(reciever)
        msg['Subject'] = 'FGC Sitemap XMLs Auto Generated'

        #email content
        message = """
                    <html>
                        <body>
                        Hi,
                        <br></br>
                        Please find the FGC Sitemap XMLs attached with this email, thank you.
                        <br><br>
                        by - FGC Automate Email Bot
                        </body>
                    </html>
                    
                   """

        msg.attach(MIMEText(message, 'html'))

        files = [
                 r'D:\Python_Deployments\FGC_Sitemap_XML\fgc_sitemap_auto_generated_xmls\auto_generated_xmls\sitemap_products.xml',
                 r'D:\Python_Deployments\FGC_Sitemap_XML\fgc_sitemap_auto_generated_xmls\auto_generated_xmls\sitemap_category.xml',
                 r'D:\Python_Deployments\FGC_Sitemap_XML\fgc_sitemap_auto_generated_xmls\auto_generated_xmls\sitemap_catalogue.xml',
                 r'D:\Python_Deployments\FGC_Sitemap_XML\fgc_sitemap_auto_generated_xmls\auto_generated_xmls\sitemap_general.xml',
                 r'D:\Python_Deployments\FGC_Sitemap_XML\fgc_sitemap_auto_generated_xmls\auto_generated_xmls\sitemap_ech.xml',
                 r'D:\Python_Deployments\FGC_Sitemap_XML\fgc_sitemap_auto_generated_xmls\auto_generated_xmls\sitemap_blog.xml',
                 r'D:\Python_Deployments\FGC_Sitemap_XML\fgc_sitemap_auto_generated_xmls\auto_generated_xmls\sitemap.xml'
            ]

        for a_file in files:
            attachment = open(a_file, 'rb')
            file_name = os.path.basename(a_file)
            part = MIMEBase('application','octet-stream')
            part.set_payload(attachment.read())
            part.add_header('Content-Disposition',
                            'attachment',
                            filename=file_name)
            encoders.encode_base64(part)
            msg.attach(part)

        #sends email

        smtpserver = smtplib.SMTP('smtp.office365.com', 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.login('reports@feelgoodcontacts.com', 'Juza3181')
        smtpserver.sendmail(sender, reciever, msg.as_string())
        smtpserver.quit()

if __name__ == '__main__':
    send_email()