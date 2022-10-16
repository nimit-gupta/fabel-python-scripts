#! /usr/bin/env python

import pandas as pd
import numpy
import pymssql
import pygsheets
from datetime import datetime
from IPython.display import display

def read_query():

    con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585',database = r'feelgood.live')
    
    sql = '''
             exec [Report].[Usp_SalesReport_UK_AllSites_onShippingDate] 
          '''
    df = pd.read_sql_query(sql, con)
    
    df['Computed'] = df.iloc[:,7:16].sum(axis = 1)
    
    df['Differences'] = df['GrandTotalAmount'].sub(df['Computed'])
    
    df['Differences'] = df['Differences'].apply(lambda x: '%.5f' % x)
    
    #display(df)
    
    now = datetime.now()
    
    dt_string = now.strftime("%A %d/%m/%Y %H:%M:%S")
    
    client = pygsheets.authorize(service_file= 'D:/Python_Deployments/FGC_Automation_Window_Server/FGC_Sales_Report_By_Delivery_Countries_On_Shipping_Date_Report/client_secret.json')

    sh = client.open('FGC_Sales_Report_By_Delivery_Countries_On_Shipping_Date_Report_2021')
    
    wks = sh.worksheet('title', 'UK')

    read_df = wks.get_as_df(has_header = True, start = 'A2')
    
    app_df = pd.concat([read_df, df], axis = 0)
    
    wks.rows = app_df.shape[0]
    
    wks.clear(start = 'A1', end = None)
    
    wks.update_value('A1', 'Updated on - ' + dt_string)
    
    wks.set_dataframe(app_df, "A2", fit = True)
    
    #wks.clear(start = 'A1', end = None)
    
    #wks.rows = df.shape[0]
    
    #wks.update_value('A1', 'Updated on - ' + dt_string)
    
    #wks.set_dataframe(df, "A2", fit = True)