#!/usr/bin/env/ python310
#coding:utf-8

'''
@author - Nimit Gupta

'''

from IPython.core.display import display 
from datetime import datetime
import pandas as pd
import pymssql
import pygsheets 

def read_query():

    con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585')

    cursor = con.cursor()

    cursor.execute(
                   '''
                      /*SQL*/

                      SELECT 
                            *
                      FROM 
                           [feelgood.reports].dbo.fgc_all_gads
                      ORDER BY 
                           GDATE DESC
                   
                   '''

                  )

    df = pd.DataFrame([{name: row[i] for i, name in enumerate([col[0] for col in cursor.description])} for row in cursor.fetchall()])

    display(df)

    now = datetime.now()
    
    dt_string = now.strftime("%A %d/%m/%Y %H:%M:%S")
    
    client = pygsheets.authorize(service_file= 'D:/Python_Deployments/FGC_Google_Ads/Universal_Client_Secret.json')

    sh = client.open('FGC_All_Websites_Google_Adwords_Report')
    
    wks = sh.worksheet('title', 'FGC_All_Websites_Google_Adwords_Report')
    
    wks.rows = df.shape[0]
    
    wks.clear(start = 'A1', end = None)
    
    wks.update_value('A1', 'Updated on - ' + dt_string)
    
    wks.set_dataframe(df, "A2", fit = True)

if __name__ == '__main__':
    read_query()