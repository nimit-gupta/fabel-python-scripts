
#!usr/bin/env python

##############################################################################################################################################################

                                                        ####FGC-Shipping-Details-Report####

##############################################################################################################################################################


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
				SELECT  DISTINCT 
						ORD.CreatedOn ORDER_DATE,
						ORD.OrderId ORDER_ID,
						ORD.OrderRef ORDER_REF,
						OSD.Status ORDER_STATUS,
						CASE 
						WHEN ORD.CurrencyId = 1 THEN 'UK'
						WHEN ORD.CurrencyId = 2 THEN 'IE'
						END AS WEBSITE,
						ISNULL(es.CarrierName, SCD.CarrierName) as CARRIER_NAME,  
						OST.ShippingDate SHIPPING_DATE,
						OST.TrackingNo TRACKING_NO,
						ORL.Country COUNTRY, 
						isnull(TotalWeight, 0) as TotalWeight,
						isnull(ORD.NetPayable, 0) as GrandTotal
				FROM 
						[feelgood.live].dbo.FG_ORDER ORD
				INNER JOIN 
						[feelgood.live].dbo.FG_OrderStatus OSD ON (ORD.OrderStatusId = OSD.OrderStatusId)
				INNER JOIN 
						[feelgood.live].dbo.FG_OrderShipmentTracking OST ON (ORD.OrderId = OST.OrderID)
				INNER JOIN 
						[feelgood.live].dbo.FG_Shipping_Carrier SCD ON (OST.CarrierId = SCD.CarrierId)
				LEFT JOIN 
						[feelgood.live].dbo.FG_ApicodeDeliveryCostPrices es with (nolock) on OST.APICode = es.APICode 
				INNER JOIN 
						[feelgood.live].dbo.FG_OrderCountryLink ORL ON (ORD.OrderId = ORL.Orderid)
				LEFT JOIN 
						[feelgood.live].dbo.FG_royalmail_Jobsubmission JN ON (ORD.OrderId = jn.Orderid)
				WHERE 
						CONVERT(DATE,OST.ShippingDate, 103) =  CONVERT(DATE, GETDATE() -1, 103)
						AND ORD.PaymentTransactionStatus = 1
						AND ORD.ParentOrderID is null
						AND ORD.OrderStatusId not in (1, 44)
							
								
				UNION 

				SELECT  DISTINCT
						ORD.CreatedOn ORDER_DATE,
						ORD.OrderId ORDER_ID,
						ORD.OrderRef ORDER_REF,
						OSD.Status ORDER_STATUS,
						'FR' AS WEBSITE , 
						ISNULL(es.CarrierName, SCD.CarrierName) as CARRIER_NAME ,
						OST.ShippingDate SHIPPING_DATE,
						OST.TrackingNo TRACKING_NO,
						ORL.Country COUNTRY, 
						isnull(TotalWeight, 0) as TotalWeight,
						isnull(ORD.GrandTotalAmount, 0) as GrandTotal
				FROM 
						[feelgood.french].dbo.FG_ORDER ORD
				INNER JOIN 
						[feelgood.french].dbo.FG_OrderStatus OSD ON (ORD.OrderStatusId = OSD.OrderStatusId)
				INNER JOIN 
						[feelgood.french].dbo.FG_OrderShipmentTracking OST ON (ORD.OrderId = OST.OrderID)
				INNER JOIN 
						[feelgood.french].dbo.FG_Shipping_Carrier SCD ON (OST.CarrierId = SCD.CarrierId) 
				LEFT JOIN 
						[feelgood.live].dbo.FG_ApicodeDeliveryCostPrices es with (nolock) on SCD.APICode = es.APICode 
				INNER JOIN 
						[feelgood.french].dbo.FG_OrderCountryLink ORL ON (ORD.OrderId = ORL.Orderid)
				LEFT JOIN 
						[feelgood.french].dbo.FG_royalmail_Jobsubmission JN ON (ORD.OrderId = jn.Orderid)
				WHERE 
						CONVERT(DATE,OST.ShippingDate, 103) =  CONVERT(DATE, GETDATE() -1, 103)
						AND ORD.PaymentTransactionStatus = 1
						AND ORD.ParentOrderID is null
						AND ORD.OrderStatusId not in (1, 44)
						AND OSD.CultureId = 1
				ORDER BY 
						7, 1, 5 DESC
    
          '''
    
    df = pd.read_sql_query(sql, con)
  
    now = datetime.now()
    
    dt_string = now.strftime("%A %d/%m/%Y %H:%M:%S")
    
    client = pygsheets.authorize(service_file= 'D:/Python_Deployments/FGC_Automation_Window_Server/FGC_Shipping_Details_Report/client_secret.json')

    sh = client.open('FGC_Shipping_Details_Report_2021')
    
    wks = sh.worksheet('title', 'Shipping_Details_Report')
    
    read_df = wks.get_as_df(has_header = True, start = 'A2')
    
    app_df = pd.concat([read_df, df], axis = 0)
    
    wks.rows = app_df.shape[0]
    
    wks.clear(start = 'A1', end = None)
    
    wks.update_value('A1', 'Updated on - ' + dt_string)
    
    wks.set_dataframe(app_df, "A2")

    
if __name__ == '__main__':
    read_query()
