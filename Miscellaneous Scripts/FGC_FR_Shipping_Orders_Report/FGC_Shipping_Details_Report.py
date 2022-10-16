
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
						   WHEN ORD.CurrencyId = 1 THEN 'UK->FR'
						   WHEN ORD.CurrencyId = 2 THEN 'IE->FR'
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
				INNER JOIN 
						[feelgood.live].dbo.FG_ApicodeDeliveryCostPrices es with (nolock) on OST.APICode = es.APICode 
				INNER JOIN 
						[feelgood.live].dbo.FG_OrderCountryLink ORL ON (ORD.OrderId = ORL.Orderid)
				INNER JOIN 
						[feelgood.live].dbo.FG_royalmail_Jobsubmission_backup JN ON (ORD.OrderId = jn.Orderid)
				WHERE 
						CONVERT(DATE,OST.ShippingDate, 103) BETWEEN '28-NOV-2021' AND '31-DEC-2021'
						AND ORD.PaymentTransactionStatus = 1
						AND ORD.ParentOrderID is null
						AND ORD.OrderStatusId not in (1, 44)
                        AND ORL.CountryId = 2
    
          '''
    
    df = pd.read_sql_query(sql, con)
  
    now = datetime.now()
    
    dt_string = now.strftime("%A %d/%m/%Y %H:%M:%S")
    
    client = pygsheets.authorize(service_file= 'C:/Users/Nimit/Desktop/Standlone Scripts/FGC_FR_Shipping_Orders_Report/Universal_Client_Secret.json')

    sh = client.open('FGC_FR_Shipping_Orders_Details')
    
    wks = sh.worksheet('title', 'FGC_FR_Shipping_Orders_Details')
    
    #read_df = wks.get_as_df(has_header = True, start = 'A2')
    
    #app_df = pd.concat([read_df, df], axis = 0)
    
    #wks.rows = app_df.shape[0]

    wks.rows = df.shape[0]
    
    wks.clear(start = 'A1', end = None)
    
    wks.update_value('A1', 'Updated on - ' + dt_string)
    
    #wks.set_dataframe(app_df, "A2")

    wks.set_dataframe(df, "A2", fit = True)

    
if __name__ == '__main__':
    read_query()
