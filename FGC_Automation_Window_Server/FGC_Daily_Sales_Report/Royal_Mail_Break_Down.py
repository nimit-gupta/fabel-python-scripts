import pandas as pd
import numpy
import pymssql
from functools import reduce
import xlsxwriter
import pygsheets
from datetime import datetime

import warnings
warnings.filterwarnings("ignore", category=FutureWarning) 

pd.set_option('display.max_columns', 1000)
pd.set_option('display.max_rows', 1000)

def read_query():

    conn = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585',database = r'feelgood.live')
    
    cursor = conn.cursor()
    
    cursor.execute(
                   '''
                    exec USP_Auto_DailyCostsforRM 
                   '''
                  )
    
    rows = cursor.fetchall()
    
    column_names = [col[0] for col in cursor.description] 
    
    df0_data = []
    for row in rows:
        df0_data.append({name: row[i] for i, name in enumerate(column_names)})
        
    cursor.nextset()
    
    column_names = [col[0] for col in cursor.description] 
      
    df1_data = []
    for row in cursor.fetchall():
        df1_data.append({name: row[i] for i, name in enumerate(column_names)})

    cursor.nextset()
    
    column_names = [col[0] for col in cursor.description] 
    
    df2_data = []
    for row in cursor.fetchall():
        df2_data.append({name: row[j] for j, name in enumerate(column_names)})
        
    cursor.nextset()
    
    column_names = [col[0] for col in cursor.description] 
    
    df3_data = []
    for row in cursor.fetchall():
        df3_data.append({name: row[k] for k, name in enumerate(column_names)})
        
    cursor.nextset()
    
    column_names = [col[0] for col in cursor.description] 
    
    df4_data = []
    for row in cursor.fetchall():
        df4_data.append({name: row[l] for l, name in enumerate(column_names)})
        
    cursor.nextset()
    
    column_names = [col[0] for col in cursor.description] 
    
    df5_data = []
    for row in cursor.fetchall():
        df5_data.append({name: row[m] for m, name in enumerate(column_names)})
        
    cursor.nextset()
    
    column_names = [col[0] for col in cursor.description] 
    
    df6_data = []
    for row in cursor.fetchall():
        df6_data.append({name: row[n] for n, name in enumerate(column_names)})
        
    cursor.nextset()
    
    column_names = [col[0] for col in cursor.description] 
    
    df7_data = []
    for row in cursor.fetchall():
        df7_data.append({name: row[o] for o, name in enumerate(column_names)})
        
    cursor.nextset()
    
    column_names = [col[0] for col in cursor.description] 
    
    df8_data = []
    for row in cursor.fetchall():
        df8_data.append({name: row[q] for q, name in enumerate(column_names)})

    cursor.close()

    df0 = pd.DataFrame(df0_data)
    df1 = pd.DataFrame(df1_data)
    df2 = pd.DataFrame(df2_data)
    df3 = pd.DataFrame(df3_data)
    df4 = pd.DataFrame(df4_data)
    df5 = pd.DataFrame(df5_data)
    df6 = pd.DataFrame(df6_data)
    df7 = pd.DataFrame(df7_data)
    
    df0['Total'] = df0['FullCostPrice'].mul(df0['OrderCount'])
    df1['Total'] = df1['FullCostPrice'].mul(df1['OrderCount'])
    df2['Total'] = df2['FullCostPrice'].mul(df2['OrderCount'])
    df3['Total'] = df3['FullCostPrice'].mul(df3['OrderCount'])
    df4['Total'] = df4['FullCostPrice'].mul(df4['OrderCount'])
    df5['Total'] = df5['FullCostPrice'].mul(df5['OrderCount'])
    df6['Total'] = df6['FullCostPrice'].mul(df6['OrderCount'])
    df7['Total'] = df7['FullCostPrice'].mul(df7['OrderCount'])
    
    
    data_frames = [df0, df1, df2, df3, df4, df5, df6, df7]
    
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['ShippingDate'],
                                            how='inner'), data_frames)
    
    
    df_merged.drop(['CarrierName_x', 'CarrierName_y'], axis = 1, inplace = True)
    
    df_merged.rename(columns = {'FullCostPrice_x':'Rate','OrderCount_x':'Qty','Total_x':'Total',\
                                'FullCostPrice_y':'Rate','OrderCount_y':'Qty','Total_y':'Total'
                               }, inplace = True)
    
    client = pygsheets.authorize(service_file = 'D:/Python_Deployments/FGC_Automation_Window_Server/FGC_Daily_Sales_Report/client_secret.json')

    sh = client.open('FGC-Daily Sales & Costs-2021')

    wks = sh.worksheet('title', 'Royal Mail Breakdown')
          
    ext_df = wks.get_as_df(has_header = False, start = 'A3', include_tailing_empty = True, include_tailing_empty_rows = False, numerize=True)
             
    ext_df_new = ext_df.iloc[:, 0:25]
     
    app_df = pd.DataFrame(numpy.vstack((ext_df_new, df_merged)))
    
    app_df.columns = app_df.iloc[0] 

    app_df = app_df[1:]
    
    app_df['Date'] = pd.to_datetime(app_df['Date']).dt.date
          
    wks.clear(start = 'A3', end = None)
    
    wks.set_dataframe(app_df, "A3", fit = True)