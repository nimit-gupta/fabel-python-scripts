#!/usr/bin/env python39 python310
#coding:utf-8

from IPython.core.display import display
from datetime import datetime
import pandas as pd
import pygsheets
import pymssql

def read_query():

    connect = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = 'flgT!9585')

    cursor = connect.cursor()

    cursor.execute(
                   '''
                   /* SQL to retreive all row records and column records from reference table fgc_all_mads sort by mdate desc*/

                   SELECT 
                         *
                   FROM 
                        [feelgood.reports].dbo.fgc_all_mads 
                   ORDER BY 
                        MDate DESC  
                   '''
                  )

    df = pd.DataFrame([{name:row[i] for i, name in enumerate([col[0] for col in cursor.description])} for row in cursor.fetchall()])

    display(df)

    now = datetime.now()
    
    dt_string = now.strftime("%A %d/%m/%Y %H:%M:%S")
    
    client = pygsheets.authorize(service_file= 'D:/Python_Deployments/FGC_Microsoft_Ads/Universal_Client_Secret.json')

    sh = client.open('FGC_All_Websites_Microsoft_Ads_Report')
    
    wks = sh.worksheet('title', 'FGC_All_Websites_Microsoft_Ads_Report')
    
    wks.rows = df.shape[0]
    
    wks.clear(start = 'A1', end = None)
    
    wks.update_value('A1', 'Updated on - ' + dt_string)
    
    wks.set_dataframe(df, "A2", fit = True)

if __name__ == '__main__':
    read_query()