import pandas as pd
import pymssql
from functools import reduce
import xlsxwriter
import pygsheets
from datetime import datetime
import numpy

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def read_query():

    conn = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585',database = r'feelgood.live')
    
    cursor = conn.cursor()
    
    cursor.execute('''
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
    
    cursor1 = conn.cursor()
    
    cursor1.execute(
                    '''
                    
                      USP_Auto_DailyCostsforAnpost
                      
                    '''
                   )
    
    rows = cursor1.fetchall()
    
    column_names = [col[0] for col in cursor1.description] 
    
    df8_data = []
    for row in rows:
        df8_data.append({name: row[i] for i, name in enumerate(column_names)})
        
    cursor1.nextset()
    
    column_names = [col[0] for col in cursor1.description] 
      
    df9_data = []
    for row in cursor1.fetchall():
        df9_data.append({name: row[i] for i, name in enumerate(column_names)})

    cursor1.nextset()
    
    sql10 = '''
                exec USP_Auto_DailyCostsforDHL
            '''
    
    df10 = pd.read_sql_query(sql10, conn)
  
    sql11 = '''
                exec USP_Auto_DailyCostsforFastway
            '''
    
    df11 = pd.read_sql_query(sql11, conn)
     
    sql12 = '''
                exec USP_Auto_DailyCostsforAsendia
            '''
    
    df12 = pd.read_sql_query(sql12, conn)
     
    sql13 = '''
                exec USP_Auto_DailyCostsforSameDayCity
            '''
    
    df13 = pd.read_sql_query(sql13, conn)
 
    df0 = pd.DataFrame(df0_data)
    df1 = pd.DataFrame(df1_data)
    df2 = pd.DataFrame(df2_data)
    df3 = pd.DataFrame(df3_data)
    df4 = pd.DataFrame(df4_data)
    df5 = pd.DataFrame(df5_data)
    df6 = pd.DataFrame(df6_data)
    df7 = pd.DataFrame(df7_data)
    df8 = pd.DataFrame(df8_data)
    df9 = pd.DataFrame(df9_data)
    
    df0['Total'] = df0['FullCostPrice'].mul(df0['OrderCount'])
    df1['Total'] = df1['FullCostPrice'].mul(df1['OrderCount'])
    df2['Total'] = df2['FullCostPrice'].mul(df2['OrderCount'])
    df3['Total'] = df3['FullCostPrice'].mul(df3['OrderCount'])
    df4['Total'] = df4['FullCostPrice'].mul(df4['OrderCount'])
    df5['Total'] = df5['FullCostPrice'].mul(df5['OrderCount'])
    df6['Total'] = df6['FullCostPrice'].mul(df6['OrderCount'])
    df7['Total'] = df7['FullCostPrice'].mul(df7['OrderCount'])
    
    df8.rename(columns = {'FullCostPrice':'Total'}, inplace = True)
    
    df9.rename(columns = {'FullCostPrice':'Total'}, inplace = True)
    
    df10.rename(columns = {'FullCostPrice':'Total'}, inplace = True)
    
    df11.rename(columns = {'FullCostPrice':'Total'}, inplace = True)
    
    df12.rename(columns = {'FullCostPrice':'Total'}, inplace = True)
    
    df13.rename(columns = {'FullCostPrice':'Total'}, inplace = True)
    
    data_frames = [df0, df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, df13]
     
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['ShippingDate'],how='inner'), data_frames)
     
    df_merged.drop(['CarrierName_x', 'CarrierName_y', 'FullCostPrice_x', 'FullCostPrice_y', 'OrderCount_x', 'OrderCount_y'], axis = 1, inplace = True)
       
    df_merged.rename(columns = {'Total_x':'Total','Total_y':'Total'}, inplace = True)
     
    '''
      df0: Non Tracked LBT
      df1: RM Next Day
      df2: Royal Mail Wordwide Standard
      df3: Royal Mail Wordwide tracked
      df4: Tracked 24 (Signed For)
      df5: Tracked 24
      df6: Tracked 24 LBT
      df7: Tracked 48 HV
      df8: Anpost Signed for
      df9: Anapost Tracked
      df10: DHL 50
      df11: Fastway
      df12: Asendia
      df13: Sameday
    
    '''
    
    df_merged = df_merged.iloc[:, [0,1,2,3,4,5,6,7,8,11,12,13,10,9,14]]
    
    df_new = pd.DataFrame(df_merged)
    
    df_new['Royal'] = df_new.iloc[:,1].astype(float) + df_new.iloc[:,2].astype(float) + df_new.iloc[:,3].astype(float) + df_new.iloc[:,4].astype(float) + df_new.iloc[:,5].astype(float) + df_new.iloc[:,6].astype(float) + df_new.iloc[:,7].astype(float) + df_new.iloc[:,8].astype(float)
    
    df_new['Other Couriers'] = df_new.iloc[:,11].astype(float) + df_new.iloc[:,12].astype(float) + df_new.iloc[:,13].astype(float) + df_new.iloc[:,10].astype(float) + df_new.iloc[:,9].astype(float) + df_new.iloc[:,14].astype(float)
    
    df_new['Total Royal'] = df_new['Royal']
    
    df_new['Total Other'] = df_new['Other Couriers']
    
    df_new['Total Royal & Total Other'] = df_new['Total Royal'].astype(float) + df_new['Total Other'].astype(float)
    
    df_new['DHL (Single Orders)'] = ' '
    
    df_new['Anpost Van'] = ' '
      
    df_new = df_new.iloc[:,[ 0, 17, 18, 19, 1, 2, 3, 4, 5, 6, 7, 8, 15, 9, 20, 10, 11, 12, 13, 21, 14, 16 ]]
       
    client = pygsheets.authorize(service_file= 'D:/Python_Deployments/FGC_Automation_Window_Server/FGC_Daily_Sales_Report/client_secret.json')

    sh = client.open('FGC-Daily Sales & Costs-2021')

    wks = sh.worksheet('title', 'Cost of Delivery')
    
    ext_df = wks.get_as_df(has_header = False, start = 'A2', include_tailing_empty = True, include_tailing_empty_rows = False, numerize=True)
     
    ext_df_new = ext_df.iloc[:, 0:22]
    
    #display(ext_df_new)
    
    app_df = pd.DataFrame(numpy.vstack((ext_df_new, df_new)))
    
    app_df.columns = app_df.iloc[0] 

    app_df = app_df[1:]
    
    app_df['Date'] = pd.to_datetime(app_df['Date']).dt.date
        
    wks.clear(start = 'A2', end = None)
    
    wks.set_dataframe(app_df, "A2", fit = True)