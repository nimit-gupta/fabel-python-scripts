
#!usr/bin/env python39 python310
#coding = utf-8

from IPython.core.display import display
from datetime import datetime
import pygsheets
import pandas as pd
import pymssql

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def read_query():

    con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585')
    
    sql = '''
				select  
                        SKU as SKU, 
                        MaxLevel as [MonthlySales on Web Orders],  
                        MEROnStock as [MonthlySales on Allocation], 

                        (	select sum(CustomerCount) as CustomerCount from 
                            (	select 'ukie' as website, count(distinct customerid ) as CustomerCount
                                from [feelgood.live].dbo.FG_Order rr with (nolock)
                                inner join [feelgood.stock].dbo.FG_OrderDetails ss with (nolock) on rr.Orderid = ss.Orderid and edited = 0 and databaseid = 1 
                                where ss.skuid = tt.skuid
                                      and convert(date, rr.createdon, 103) >= convert(date, getdate() - 365, 103)

                                union all 

                                select 'fr' as website, count(distinct customerid ) as CustomerCount
                                from [feelgood.french].dbo.FG_Order rr with (nolock)
                                inner join [feelgood.stock].dbo.FG_OrderDetails ss with (nolock) on rr.Orderid = ss.Orderid and edited = 0 and databaseid = 2 
                                where ss.skuid = tt.skuid  
                                    and convert(date, rr.createdon, 103) >= convert(date, getdate() - 365, 103)
                            ) as aa
                        ) as CustomerCount,
                        
                        isnull(
                        (	select sum(boxes) from [feelgood.stock].dbo.FG_ShippedOrdersLog with (nolock)
                            where skuid = tt.skuid and convert(date, createdon, 103) >= convert(date, getdate() - 91, 103)
                            and [DBId] in (1, 2) 
                        ), 0)  as [3 months scanned out], 

                        isnull(
                        (	select sum(boxes) from [feelgood.stock].dbo.FG_ShippedOrdersLog with (nolock)
                            where skuid = tt.skuid and convert(date, createdon, 103) >= convert(date, getdate() - 182, 103)
                            and [DBId] in (1, 2) 
                        ), 0)  as [6 months scanned out], 

                        isnull(
                        (	select sum(boxes) from [feelgood.stock].dbo.FG_ShippedOrdersLog with (nolock)
                            where skuid = tt.skuid and convert(date, createdon, 103) >= convert(date, getdate() - 365, 103)
                            and [DBId] in (1, 2) 
                        ), 0)  as [12 months scanned out]

                from 
                        [feelgood.stock].dbo.fg_product tt with (nolock)
                inner join 
                        [feelgood.stock].dbo.fg_productmaster mr with (nolock) on tt.ProductCode = mr.ProductCode 
                        and productTypeid in (1)
                where 
                        MEROnStock >= 1 and MEROnStock <= 7 
                        and MaxLevel >= 1 and MaxLevel <= 7  
                        and tt.Enable = 1 

    
          '''
    
    df = pd.read_sql_query(sql, con)

    df['SKU'] = df['SKU'].str.zfill(13)

    df['SKU'] = "'" + df['SKU']
  
    now = datetime.now()
    
    dt_string = now.strftime("%A %d/%m/%Y %H:%M:%S")
    
    client = pygsheets.authorize(service_file= 'D:/Python_Deployments/FGC_Automation_Window_Server/FGC_Low_Seller_Sku_Report/client_secret.json')

    sh = client.open('FGC_Low_Seller_Sku_Report_2021_22')
    
    wks = sh.worksheet('title', 'Low_Seller_Sku_Report')

    #read_df = wks.get_as_df(has_header = True, start = 'A2')
    
    #app_df = pd.concat([read_df, df], axis = 0)
    
    #wks.rows = app_df.shape[0]

    wks.rows = df.shape[0]
    
    wks.clear(start = 'A1', end = None)
    
    wks.update_value('A1', 'Updated on - ' + dt_string)
    
    #wks.set_dataframe(app_df, "A2")

    wks.set_dataframe(df, "A2")
   
if __name__ == '__main__':
    read_query()
