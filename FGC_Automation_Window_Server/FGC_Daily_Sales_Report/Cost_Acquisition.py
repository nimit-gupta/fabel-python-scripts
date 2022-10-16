from IPython.display import display
import pandas as pd
import pymssql
import pygsheets

import warnings
warnings.filterwarnings("ignore") 

def read_query():
    
    con = pymssql.connect(host = r'217.174.248.81',
                          port = 49559,
                          user = r'DevUser3',
                          password = r'flgT!9585',
                          database = r'feelgood.live'
                         )
    sql = '''
            SELECT AcquistionCostDate, Website, Google, Bing, Facebook FROM FG_Daily_Acquisition_Cost fdac2  
            
          '''
    df = pd.read_sql_query(sql, con)
    
    #pvt = pd.pivot_table(data = df, index = 'AcquistionCostDate', columns = ['Google','Bing','Facebook'], values = 'Website',  )
    
    df['Total'] = ((df.iloc[:,[2,3,4]].sum(axis = 1, numeric_only = True)).mul(1.1)).round(2)
      
    pvt = pd.pivot_table(data = df, index = 'AcquistionCostDate', values = ['Google','Bing','Facebook','Total'], columns = 'Website')
    
    pvt = pvt.swaplevel(0,1, axis=1).sort_index(axis=1)
    
    pvt = pvt.reset_index()
    
    pvt.columns = ['_'.join(tup).rstrip('_') for tup in pvt.columns.values]
    
    df1 = pvt.iloc[:, [0, 11, 9, 10, 12, 7, 5, 6, 8, 3, 1, 2, 4]]
    
    df1.insert(1, 'TTTUK', df1['UK_Total'])
    
    df1.insert(2, 'TTIE', df1['IE_Total'])
    
    df1.insert(3, 'TTFR', df1['FR_Total'])
    
    df1.insert(4, 'Total', df1.iloc[:,[1,2,3]].sum(axis = 1, numeric_only = True))
    
    df1.rename(columns = {'AcquistionCostDate':'Date',
                          'TTTUK':'UK',
                          'TTIE':'IE',
                          'TTFR':'FR',
                          'UK_Google':'Google',
                          'UK_Bing':'Bing',
                          'UK_Facebook':'Facebook',
                          'UK_Total':'Total',
                          'IE_Google':'Google',
                          'IE_Bing':'Bing',
                          'IE_Facebook':'Facebook',
                          'IE_Total':'Total',
                          'FR_Google':'Google',
                          'FR_Bing':'Bing',
                          'FR_Facebook':'Facebook',
                          'FR_Total':'Total',
                         }, inplace = True)
    
    client = pygsheets.authorize(service_file= 'D:/Python_Deployments/FGC_Automation_Window_Server/FGC_Daily_Sales_Report/client_secret.json')

    sh = client.open('FGC-Daily Sales & Costs-2021')

    wks = sh.worksheet('title','Cost Acquisition')
       
    wks.clear(start = 'A3', end = None)
    
    wks.set_dataframe(df1, "A3", fit = True)