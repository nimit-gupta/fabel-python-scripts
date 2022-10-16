#! usr/bin/env python310

from IPython.core.display import display
import pandas as pd 
import pymssql
import pygsheets 

def read_query():

    con = pymssql.connect(host = r'217.174.248.81', port =49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    sql =  '''
    
              exec USP_Auto_DailyRefundedData

           '''

    df = pd.read_sql_query(sql, con)

    df['TotalAmountRefund'] = df['UkRefunded'] + df['IERefunded'] + df['FRRefunded']

    client = pygsheets.authorize(service_account_file= "D:/Python_Deployments/FGC_Automation_Window_Server/FGC_Daily_Sales_Cost_Report/client_secret.json")

    sh = client.open('FGC-Daily Sales & Costs-2021-22')

    wks = sh.worksheet('title', 'Cost Refund')

    read_df = wks.get_as_df(has_header = True, start = 'A2')
    
    app_df = pd.concat([read_df, df], axis = 0)
    
    wks.rows = app_df.shape[0]

    wks.clear(start = 'A2', end = None)
    
    wks.set_dataframe(app_df, "A2", fit = True)




