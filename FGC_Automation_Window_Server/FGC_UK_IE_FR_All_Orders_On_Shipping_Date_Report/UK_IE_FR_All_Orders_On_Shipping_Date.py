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

    con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585')
    
    sql = '''
                declare @getdate datetime = getdate() - 3 

                declare @month as int = month(@getdate) , @year as int = year(@getdate)   

                select 
                    convert(date, rr.createdon, 103) as OrderDate,
                    rr.Orderid,
                    Orderref, 
                    case 
                        when (left(orderref,3) = 'FG-' or left(orderref,4) = 'FGR-') then 'CS Order'
                        when (left(orderref,2) = 'RM') then 'Reshipped Order'
                        when (left(orderref,3) = 'FGO') then 'Web Order'
                        when (left(orderref,4) = 'FGAR') then 'Auto-replenish Order'
                        when (left(orderref,3) = 'FGM') then 'App Order'
                        when (left(orderref,4) = 'UKSR') then 'SMS Order'  
                    end as OrderType, 
                    status as OrderStatus, 
                    NetPayable as GrandtotalAmount,  
                    iif(rr.currencyid = 1 , 'UK', 'IE') as Website ,  
                    iif(isnull ((select OrderCount from [feelgood.live].dbo.fg_order with (nolock) where orderid = isnull(rr.EyeglassesParentOrderid, 0)),OrderCount) = 1, 'Yes', 'No') as NewCustomer ,

                    isnull(er.CarrierName, ll.CarrierName)  as CarrierName,

                    convert(date, ng.ShippingDate, 103) as ShippingDate, 
                    yy.name as Country
                    --iif(isnull(APICode, '') = 'CRL1', 'LBT Non-Tracked', '')

                from 
                    [feelgood.live].dbo.fg_order rr 
                inner join 
                    [feelgood.live].dbo.fg_orderstatus ss on rr.orderstatusid = ss.Orderstatusid  
                inner join 
                    [feelgood.live].dbo.fg_shipping_detail LL on rr.shippingId = ll.shippingid 
                inner join 
                    [feelgood.live].dbo.FG_OrderShipmentTracking ng on rr.OrderId = ng.OrderID 
                inner join 
                    [feelgood.live].dbo.fg_address ss1 on rr.DeliveryAddressId = ss1.AddressId 
                inner join 
                    [feelgood.live].dbo.FG_Country yy on ss1.CountryId = yy.CountryId
                left join  
                     [feelgood.live].dbo.FG_ApicodeDeliveryCostPrices er on ng.APICode = er.APICode 
                where  
                    month(ng.ShippingDate) = @month and year(ng.ShippingDate) = @year       
                    --and PaymentTransactionStatus = 1  
                    --AND ParentOrderID IS NULL
                    --AND rr.OrderStatusId in (4, 32, 43) -- shipped/shipped next day/ready for collecion 

                union

                select 
                    convert(date, rr.createdon, 103) as OrderDate,
                    rr.Orderid,
                    Orderref, 
                    case 
                        when (left(orderref,3) = 'FG-' or left(orderref,4) = 'FGR-') then 'CS Order'
                        when (left(orderref,2) = 'RM') then 'Reshipped Order'
                        when (left(orderref,3) = 'FGO') then 'Web Order'
                        when (left(orderref,4) = 'FRAR') then 'Auto-replenish Order'
                        when (left(orderref,3) = 'FGM') then 'App Order'
                        when (left(orderref,4) = 'UKSR') then 'SMS Order'  
                    end as OrderType, 
                    status as OrderStatus, 
                    GrandtotalAmount,  
                    iif(rr.currencyid = 1 , 'UK', 'FR') as Website,  
                    iif(OrderCount = 1, 'Yes', 'No') as NewCustomer  ,  

                    isnull(er.CarrierName, ll.CarrierName)  as CarrierName,

                    convert(date, ng.ShippingDate, 103) as ShippingDate, 
                    yy.name as Country

                from 
                    [feelgood.french].dbo.fg_order rr 
                inner join 
                    [feelgood.french].dbo.fg_orderstatus ss on rr.orderstatusid = ss.Orderstatusid and ss.cultureid = 1 
                inner join 
                    [feelgood.french].dbo.fg_shipping_detail LL on rr.shippingId = ll.shippingid
                inner join 
                    [feelgood.french].dbo.FG_Shipping_Carrier crr on ll.carrierid = crr.carrierid
                inner join 
                    [feelgood.french].dbo.FG_OrderShipmentTracking ng on rr.OrderId = ng.OrderID
                inner join 
                    [feelgood.french].dbo.fg_address ss1 on rr.DeliveryAddressId = ss1.AddressId 
                inner join 
                    [feelgood.french].dbo.FG_Country yy on ss1.CountryId = yy.CountryId 
                left join  
                    [feelgood.live].dbo.FG_ApicodeDeliveryCostPrices er on crr.APICode = er.APICode 
                where  
                    month(ng.ShippingDate) = @month and year(ng.ShippingDate) = @year 
                    
                order by 10
               
            
        '''
    
    df = pd.read_sql_query(sql, con)

    df['OrderType'] = df['OrderType'].str.replace('Order', '')
  
    now = datetime.now()
    
    dt_string = now.strftime("%A %d/%m/%Y %H:%M:%S")
    
    client = pygsheets.authorize(service_file= 'D:/Python_Deployments/FGC_Automation_Window_Server/FGC_UK_IE_FR_All_Orders_On_Shipping_Date_Report/client_secret.json')

    sh = client.open('FGC_UK_IE_FR_All_Orders_On_Shipping_Date_Report_2021')
    
    wks = sh.worksheet('title', 'UK_IE_FR_All_Orders_On_Shipping_Date')

    wks.rows = df.shape[0]
    
    wks.clear(start = 'A1', end = None)
    
    wks.update_value('A1', 'Updated on - ' + dt_string)
    
    wks.set_dataframe(df, "A2", fit = True)
       
if __name__ == '__main__':
    read_query()
                