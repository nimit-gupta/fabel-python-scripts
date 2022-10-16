#! /usr/bin/env python

'''
Feel Good Contacts - Daily Escalation Report.

'''

from IPython.display import display
import pandas as pd
import pymssql
import pygsheets
from datetime import datetime

def read_query():

    con = pymssql.connect(host = r'217.174.248.81', port =49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    sql = '''
              with cte as
                    (	select distinct 
                            rr.Orderid ,
                            Status as OrderStatus, 
                            Comments, 
                            rr.createdon as OrderDate, 
                            (select top 1 ShippingDate from fg_orderShipmentTracking where orderid = rr.OrderId order by 1 desc) as ShippingDate,   
                            isnull(
                            (	select isnull(es.CarrierName, crr.CarrierName) as CarrierName
                                from 
                                    fg_ordershipmentTracking gg with (nolock) 
                                inner join 
                                    FG_Shipping_Carrier crr with (nolock) on gg.carrierid = crr.carrierid
                                left join 
                                    FG_ApicodeDeliveryCostPrices es with (nolock) on gg.APICode = es.APICode 
                                where gg.orderid = rr.orderid 
                            ), '') as CarrierName
                        from 
                            fg_order rr with (nolock)
                        inner join 
                            [feelgood.stock].dbo.FG_OrderEscalationDetails ordes  with (nolock) on rr.orderid = ordes.orderid 
                        inner join 
                            FG_OrderStatus ss on rr.OrderStatusId = ss.OrderStatusId 
                        where 
                            convert(date, rr.createdOn, 103) = DATEADD(day, DATEDIFF(day, 1, GETDATE()), 0)  
                            and isnull(rr.EyeglassesParentOrderid, 0) = 0 
                            and ParentOrderID is null
                            and rr.OrderStatusId not in (1, 44)
                            and CurrencyId = 1
                    ) 

                    select distinct 
                        cc.Orderid,  
                        OrderStatus, 
                        isnull(
                        (	select string_agg(comments, '; ') 
                            from (select distinct comments from cte where orderid = cc.orderid and len(comments) > 0) as aa 
                        ), '') as Comments, 
                        convert(date, OrderDate, 103) OrderDate,
                        convert(date,ShippingDate, 103) ShippingDate,
                        CarrierName, 

                        isnull(
                        (	select string_agg(Category, ', ') from
                            (	select distinct [description] as Category 
                                from fg_cscasecategory yy 
                                inner join fg_cscase ee with (nolock) on yy.casecategoryid = ee.casecategoryid
                                where ee.orderid = cc.orderid  
                            ) as aa 
                        ), '') as Category, 

                        isnull(
                        (	select string_agg(SubCategory, ', ') from
                            (	select distinct CSSubCategory as SubCategory 
                                from fg_cssubcategory yy 
                                inner join fg_cscase ee with (nolock) on yy.CSSubCategoryID = ee.CSSubCategoryID
                                where ee.orderid = cc.orderid  
                            ) as aa 
                        ), '') as SubCategory  

                    from cte cc 
                    order by 
                        OrderDate, 
                        ShippingDate


          '''

    df = pd.read_sql_query(sql, con)

    now = datetime.now()
    
    dt_string = now.strftime("%A %d/%m/%Y %H:%M:%S")

    client = pygsheets.authorize(service_account_file= "D:/Python_Deployments/FGC_Automation_Window_Server/FGC_Daily_Escalation_Report/client_secret.json")

    googlesheet = client.open("FGC_Daily_Escalation_Report_2021_22")

    worksheet = googlesheet.worksheet('title', 'Daily_Escalation_Orders_Details')

    read_df = worksheet.get_as_df(has_header = True, start = 'A2')
    
    app_df = pd.concat([read_df, df], axis = 0)
    
    worksheet.rows = app_df.shape[0]

    worksheet.clear(start = 'A1', end = None)
    
    worksheet.update_value('A1', 'Updated on - ' + dt_string)
    
    worksheet.set_dataframe(app_df, "A2", fit = True)

if __name__ == '__main__':
    read_query()

