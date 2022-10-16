from IPython.display import display 
import pandas as pd
import pymssql
import pygsheets

pd.set_option('display.max_rows', 100000)

def read_query():
    
    con = pymssql.connect(host = r'217.174.248.81',
                          port = 49559,
                          user = r'DevUser3',
                          password = r'flgT!9585',
                          database = r'feelgood.live'
                         )
    sql = '''
            SELECT LabourCostDate Date, PickPack, Stock, HolidayPaid, Management FROM Fg_Daily_Labour_Costs 
            
          '''
    df = pd.read_sql_query(sql, con)
    
    df['Total'] = ((df.iloc[:,[1,2,3,4]].sum(axis = 1, numeric_only = True)).mul(1.1)).round(2)
    
    client = pygsheets.authorize(service_file= 'D:/Python_Deployments/FGC_Automation_Window_Server/FGC_Daily_Sales_Report/client_secret.json')

    sh = client.open('FGC-Daily Sales & Costs-2021')

    wks = sh.worksheet('title','Costs Labour')
       
    wks.clear(start = 'A2', end = None)
    
    wks.set_dataframe(df, "A2", fit = True)