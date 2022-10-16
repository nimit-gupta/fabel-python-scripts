#!/usr/bin/env python
# -*- coding:utf-8 -*-

from IPython.core.display import display
from datetime import datetime
import pandas as pd
import pymssql 
import pygsheets

def read_query():

    con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585')

    query = '''
               	/*SQL QUERY*/

                SELECT
                    *, 
                    (Order_Qty - Rec_Qty) as Open_Qty
                FROM 
                (	SELECT 
                        A.SupplierName,
                        ISNULL(B.OrderRef, '')AS OrderRef,
                        CAST(B.CreatedOn AS DATE) AS Order_Date,
                        CAST(B.DeliveryDate AS DATE) AS Delivery_Date,
                        D.SKU,
                        D.ProductName,
                        D.Power,
                        D.BaseCurve,
                        D.Diameter,
                        D.Axis,
                        D.Cylinder,
                        D.[Add],
                        D.ND,
                        D.Color,
                        SUM(C.BOXES) Order_Qty,
                        isnull(SUM(C.BoxesReceived), 0) Rec_Qty
                    FROM 
                        [feelgood.stock].dbo.FG_Supplier A WITH (NOLOCK)
                    INNER JOIN 
                        [feelgood.stock].dbo.FG_SupplierOrder B WITH (NOLOCK) ON A.SupplierID = B.SupplierID and isnull(Canceled,0) = 0
                    INNER JOIN
                        [feelgood.stock].dbo.FG_SupplierOrderItems C WITH (NOLOCK) ON B.OrderID = C.OrderID
                    INNER JOIN 
                        [feelgood.stock].dbo.FG_Product D WITH (NOLOCK) ON C.SKUid = D.SKUid
                    WHERE 
                        B.CreatedOn BETWEEN '01-APR-2021' AND DATEADD(DAY, DATEDIFF(DAY, 0, GETDATE()), 0)
                    GROUP BY 
                        A.SupplierName,
                        B.OrderRef,
                        B.CreatedOn,
                        B.DeliveryDate,
                        D.SKU,
                        D.ProductName,
                        D.Power,
                        D.BaseCurve,
                        D.Diameter,
                        D.Axis,
                        D.Cylinder,
                        D.[Add],
                        D.ND,
                        D.Color
                ) AS AA 
                ORDER BY 3, 1, 6
                
                '''

    df = pd.read_sql_query(query, con)

    df = df.fillna(' ')

    df['SKU'] = df['SKU'].str.zfill(13)

    df['SKU'] = "'" + df['SKU']

    df['Power'] = "'" + df['Power']

    #display(df)
 
    now = datetime.now()
    
    dt_string = now.strftime("%A %d/%m/%Y %H:%M:%S")
    
    client = pygsheets.authorize(service_file= 'D:/Python_Deployments/FGC_Automation_Window_Server/FGC_Supplier_Stock_Report/client_secret.json')

    sh = client.open('FGC_Supplier_FollowUp_Report')
    
    wks = sh.worksheet('title', 'FGC_Supplier_FollowUp_Report')
    
    wks.rows = df.shape[0]
    
    wks.clear(start = 'A1', end = None)
    
    wks.update_value('A1', 'Updated on - ' + dt_string)
    
    wks.set_dataframe(df, "A2", fit = True)

    
if __name__ == '__main__':
    read_query()



