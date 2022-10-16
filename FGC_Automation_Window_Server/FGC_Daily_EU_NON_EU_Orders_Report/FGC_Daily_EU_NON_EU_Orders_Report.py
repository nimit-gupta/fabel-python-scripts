#! /usr/bin/env python

'''
Feel Good Contacts - Daily EU Orders Report.

'''

from IPython.display import display
import pandas as pd
import pymssql
import pygsheets
from datetime import datetime

def read_query():

    con = pymssql.connect(host = r'217.174.248.81', port =49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    sql = '''
             select 
                   convert(date, createdon, 103) as OrderDate,
                   Country,
                   count(ord.OrderId) as OrderCount   
             from
                  [feelgood.live]..FG_ORDER ORD
             inner join
                  [feelgood.live]..FG_OrderCountryLink ORL on ORD.OrderId = ORL.Orderid
             inner join
                  [feelgood.live]..FG_Country ry on orl.CountryId = ry.CountryId
             where
                  convert(date, ord.CreatedOn, 103) = DATEADD(day, DATEDIFF(day, 1, GETDATE()), 0) 
                  and ORD.PaymentTransactionStatus = 1
                  and ORD.ParentOrderID is null
                  and ORD.OrderStatusId not in (1, 44)
                  and ORL.CountryId NOT IN (1, 2, 10)      
             group by
                  convert(date, createdon, 103), Country
             order by 1
          '''

    df = pd.read_sql_query(sql, con)

    now = datetime.now()
    
    dt_string = now.strftime("%A %d/%m/%Y %H:%M:%S")

    client = pygsheets.authorize(service_account_file= "D:/Python_Deployments/FGC_Automation_Window_Server/FGC_Daily_EU_NON_EU_Orders_Report/client_secret.json")

    googlesheet = client.open("FGC_Daily_EU_NON_EU_Orders_Report_2021_22")

    worksheet = googlesheet.worksheet("title", "Daily_EU_NON_EU_Orders_Details")

    read_df = worksheet.get_as_df(has_header = True, start = 'A2')
    
    app_df = pd.concat([read_df, df], axis = 0)
    
    worksheet.rows = app_df.shape[0]

    worksheet.clear(start = 'A1', end = None)
    
    worksheet.update_value('A1', 'Updated on - ' + dt_string)
    
    worksheet.set_dataframe(app_df, "A2", fit = True)

if __name__ == '__main__':
    read_query()

