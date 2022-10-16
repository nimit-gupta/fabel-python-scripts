import pandas as pd
import pymssql
from functools import reduce
import xlsxwriter
import pygsheets
from datetime import datetime
import numpy as np

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def read_query():

    conn = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585',database = r'feelgood.live')
    
    sql0 = '''
              exec USP_Auto_DailyOrdersReceived
           '''
    
    df0 = pd.read_sql_query(sql0, conn)
    
    sql1 = '''
              exec USP_Auto_DailySales_UKIE  1
           
           '''
    
    df1 = pd.read_sql_query(sql1, conn)
    
    df1['Total'] = df1.iloc[:,1] + df1.iloc[:,2] + df1.iloc[:,3] + df1.iloc[:, 4]
     
    sql2 = '''
              exec USP_Auto_DailySales_UKIE  2
           
           '''
    
    df2 = pd.read_sql_query(sql2, conn)
    
    df2['Total'] = df2.iloc[:,1] + df2.iloc[:,2] + df2.iloc[:,3] + df2.iloc[:, 4]
      
    sql3 = '''
             exec USP_Auto_DailySales_FR             
           '''
    df3 = pd.read_sql_query(sql3, conn)
    
    df3['Total'] = df3.iloc[:,1] + df3.iloc[:, 2]
     
    df_con = pd.concat([df0, df1, df2, df3], axis = 1)
    
    df_new = df_con.iloc[:, np.r_[0:2, 3:8, 9:14, 15:18]]
 
    df_new.insert(loc = 2, column =  'UK', value = df_new.iloc[:, 6])
    
    df_new.insert(loc = 3, column = 'IE', value = df_new.iloc[:, 12])
    
    df_new.insert(loc = 4, column = 'FR', value = df_new.iloc[:, 16])
    
    df_new.insert(loc = 5, column = 'UKIEFR', value = df_new.iloc[:,2] + df_new.iloc[:,3] + df_new.iloc[:,4])
    
    df_new.insert(loc = 6, column = 'Average Basket', value = df_new.iloc[:,5]/df_new.iloc[:,1])
     
    client = pygsheets.authorize(service_file= 'D:/Python_Deployments/FGC_Automation_Window_Server/FGC_Daily_Sales_Report/client_secret.json')

    sh = client.open('FGC-Daily Sales & Costs-2021')

    wks = sh.worksheet('title','Sales by Region ')
    
    ext_df = wks.get_as_df(has_header = False, start = 'A2', include_tailing_empty = True, include_tailing_empty_rows = False, numerize=True)
    
    ext_df_new = ext_df.iloc[:, 0:20]
   
    app_df = pd.DataFrame(np.vstack((ext_df_new, df_new)))
    
    app_df.columns = app_df.iloc[0] 

    app_df = app_df[1:]
    
    app_df['Date'] = pd.to_datetime(app_df['Date']).dt.date
    
    wks.clear(start = 'A2', end = None)
    
    wks.set_dataframe(app_df, "A2", fit = True)
    
