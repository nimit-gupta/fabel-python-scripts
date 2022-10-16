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
               
                SELECT 
                    A.BRANDNAME		as Brand,
                    F.NAME			as Product_Category,
                    D.PRODUCTCODE	as Product_Code,
                    D.PRODUCTNAME	as Product_Name,
                    D.SKU			as Product_Sku,
                    D.[Power]		as [Power],
                    D.BaseCurve		as BaseCurve,
                    D.Diameter		as Diameter,
                    D.Color			as Color,
                    D.Axis			as Axis,
                    D.Cylinder		as Cylinder,
                    D.[Add]			as [Add],
                    D.ND			as ND,
                    D.MAXLEVEL		as Monthly_Sales_Web,
                    D.MERONSTOCK	as Monthly_Sales_Allocation,
                    D.BOXES			as Current_Avaiable_Boxes,
                    SUM(I.L3SALES)	as L3_Sales_Boxes,
                    SUM(J.L6SALES)	as L6_Sales_Boxes,
                    SUM(K.AS2021)	as Annual_Sales_Boxes_2021,
                    SUM(L.AS2020)	as Annual_Sales_Boxes_2020,
                    SUM(M.AS2019)	as Annual_Sales_Boxes_2019,
                    SUM(N.SL2021)	as Sales_Loss_Boxes_2021,
                    SUM(O.CO2021)	as Cancelled_Order_2021, 
                    SUM(DA.CapacityBoxes) as ShippingCapacity,
                    SUM(DB.HoldingBoxes) as HoldingBoxes
                FROM 
                    [feelgood.live].dbo.FG_Brand A with (nolock)
                INNER JOIN 
                    [feelgood.live].dbo.FG_ProductBrandJoin B with (nolock) ON A.BrandID = B.BrandID 
                INNER JOIN  
                    [feelgood.live].dbo.FG_Product C with (nolock) ON B.Productid = C.Productid 
                INNER JOIN
                    [feelgood.stock].dbo.FG_Product D with (nolock) ON C.ProductCode = D.ProductCode 
                    AND LEN(SKU) > 0
                INNER JOIN 
                    [feelgood.live].dbo.FG_Productcategoryjoin E with (nolock) ON C.productid = E.productid and isPrimary = 1 
                INNER JOIN 
                    [feelgood.live].dbo.fg_categorydescription F with (nolock) ON E.CategoryId = F.categoryid
                INNER JOIN 
                    [feelgood.stock].dbo.FG_Product_Instock G with (nolock) ON D.ProductCode = G.ProductCode and G.InStock = 1
                LEFT JOIN 
                    ( 
                    SELECT  
                            SKUid,
                            SUM(BOXES) L3SALES
                    FROM 
                        [feelgood.stock].dbo.FG_ShippedOrdersLog with (nolock)
                    WHERE 
                        CreatedOn BETWEEN '01-OCT-2021' AND '31-DEC-2021'
                        AND DBID IN (1,2)
                    GROUP BY 
                        SKUid 
                    ) I ON D.SKUid = I.SKUid
                LEFT JOIN 
                    ( 
                    SELECT  
                            SKUid,
                            SUM(BOXES) L6SALES
                    FROM 
                        [feelgood.stock].dbo.FG_ShippedOrdersLog with (nolock)
                    WHERE 
                        CreatedOn BETWEEN '01-JULY-2021' AND '31-DEC-2021'
                        AND DBID IN (1,2)
                    GROUP BY 
                        SKUid 
                    ) J ON D.SKUid = J.SKUid
                LEFT JOIN 
                    (
                    SELECT  
                            SKUid,
                            SUM(BOXES) AS2021
                    FROM 
                        [feelgood.stock].dbo.FG_ShippedOrdersLog with (nolock)
                    WHERE 
                        CreatedOn BETWEEN '01-JAN-2021' AND '31-DEC-2021'
                        AND DBID IN (1,2)
                    GROUP BY 
                        SKUid 
                    ) K ON D.SKUid = K.SKUid
                LEFT JOIN 
                    (
                    SELECT  
                            SKUid,
                            SUM(BOXES) AS2020
                    FROM 
                        [feelgood.stock].dbo.FG_ShippedOrdersLog with (nolock)
                    WHERE 
                        CreatedOn BETWEEN '01-JAN-2020' AND '31-DEC-2020'
                        AND DBID IN (1,2)
                    GROUP BY 
                        SKUid
                    ) L ON D.SKUid = L.SKUid
                LEFT JOIN 
                    (
                    SELECT  
                            SKUid,
                            SUM(BOXES) AS2019
                    FROM 
                        [feelgood.stock].dbo.FG_ShippedOrdersLog with (nolock)
                    WHERE 
                        CreatedOn BETWEEN '01-JAN-2019' AND '31-DEC-2019'
                        AND DBID IN (1,2)
                    GROUP BY 
                        SKUid 
                    ) M ON D.SKUid = M.SKUid
                LEFT JOIN 
                    (
                    SELECT 
                        SKUid,
                        SUM(Boxes) SL2021
                    FROM 
                        [feelgood.stock].dbo.FG_BackOrderDetails with (nolock) 
                    WHERE 
                        CreatedOn BETWEEN '01-JAN-2021' AND '31-DEC-2021'
                        AND DatabaseID IN (1,2)
                    GROUP BY 
                        SKUid
                    ) N ON D.SKUid = N.SKUid 
                LEFT JOIN 
                    (
                    SELECT 
                        SKUid,
                        SUM(BoxesOrdered) CO2021
                    FROM 
                        [feelgood.stock].dbo.FG_OrderDetails with (nolock)
                    WHERE 
                        CreatedOn BETWEEN '01-JAN-2021' AND '31-DEC-2021'
                        AND Edited > 0
                    GROUP BY 
                        SKUid
                    ) O ON D.SKUid = O.SKUid 
                LEFT JOIN
                (	SELECT 
                        skuid, 
                        sum(CapacityBoxes) as CapacityBoxes
                    FROM 
                        [feelgood.stock].dbo.FG_ProductStockAreaWise DA with (nolock)
                    INNER JOIN 
                        [feelgood.stock].dbo.FG_StockArea DB with (nolock) ON DA.AreaCode = DB.AreaCode    /*For Capacity*/
                        AND DB.ShippingArea = 1 
                    GROUP BY 
                        da.skuid
                ) DA on D.SKUid = DA.SKUid
                LEFT JOIN
                (	SELECT 
                        skuid, 
                        sum(Boxes) as HoldingBoxes
                    FROM 
                        [feelgood.stock].dbo.FG_ProductStockAreaWise DA with (nolock)
                    INNER JOIN 
                        [feelgood.stock].dbo.FG_StockArea DB with (nolock) ON DA.AreaCode = DB.AreaCode    /*For Holding*/ 
                        AND DB.HoldingArea = 1
                    GROUP BY 
                        da.skuid
                ) DB on D.SKUid = DB.SKUid
            
                GROUP BY 
                    A.BRANDNAME,
                    F.NAME,
                    D.PRODUCTCODE,
                    D.PRODUCTNAME,
                    D.SKU,
                    D.MAXLEVEL,
                    D.MERONSTOCK,
                    D.BOXES,
                    D.[Power],
                    D.BaseCurve,
                    D.Diameter,
                    D.Color,
                    D.Axis,
                    D.Cylinder,
                    D.[Add],
                    D.ND             
    '''

    df = pd.read_sql_query(query, con)

    df = df.fillna('0')

    df['Product_Sku'] = df['Product_Sku'].str.zfill(13)

    df['Product_Sku'] = "'" + df['Product_Sku']

    df['Power'] = "'" + df['Power']

    display(df)
 
    now = datetime.now()
    
    dt_string = now.strftime("%A %d/%m/%Y %H:%M:%S")
    
    client = pygsheets.authorize(service_file= 'D:/Python_Deployments/Miscellaneous Scripts/FGC_DSL_Validation_Data/Universal_Client_Secret.json')

    sh = client.open('DSL_Validation_Data')
    
    wks = sh.worksheet('title', 'DSL_Validation_Data')
    
    wks.rows = df.shape[0]
    
    wks.clear(start = 'A1', end = None)
    
    wks.update_value('A1', 'Updated on - ' + dt_string)
    
    wks.set_dataframe(df, "A3", fit = True)

    
if __name__ == '__main__':
    read_query()



