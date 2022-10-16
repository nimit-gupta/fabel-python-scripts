#!/usr/bin/env python310
#coding:utf-8
'''
@author - Nimit Gupta

'''

from IPython.core.display import display
import pandas as pd
import sqlalchemy
import pymssql 

def read_query():

    connect_0 = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585')

    cursor = connect_0.cursor()

    cursor.execute(
                   '''
                        SELECT 
                            P0.Order_Date ORDER_DATE,
                            P0.UKOrderNo UK_TOT_NON_MOB_ORDERS,
                            P1.IEOrderNo IE_TOT_NON_MOB_ORDERS,
                            P2.FROrderNo FR_TOT_NON_MOB_ORDERS
                        FROM
                        (
                        SELECT 
                            Order_Date,
                            SUM(Order_No) UKOrderNo
                        FROM
                            (
                        SELECT 
                            CAST(A.CreatedOn AS DATE) Order_Date,
                            COUNT(DISTINCT A.OrderId) Order_No
                        FROM 
                            [feelgood.live].dbo.FG_Order A
                        WHERE 
                            CAST(A.CreatedOn AS DATE) BETWEEN CAST('01-01-2021' AS DATE) AND CAST(GETDATE() - 1 AS DATE)
                            AND A.CurrencyId = 1 
                            AND A.PaymentTransactionStatus = 1
                            AND A.ParentOrderID is null
                            AND A.OrderStatusId not in (1, 44)
                            AND LEFT(A.OrderRef ,3) <> 'FGM'
                        GROUP BY 
                            A.CreatedOn
                            ) Q0
                        GROUP BY 
                            Order_date
                        ) P0

                        LEFT JOIN
                                (
                        SELECT 
                            Order_Date,
                            SUM(Order_No) IEOrderNo
                        FROM
                            (
                        SELECT 
                            CAST(A.CreatedOn AS DATE) Order_Date,
                            COUNT(DISTINCT A.OrderId) Order_No
                        FROM 
                            [feelgood.live].dbo.FG_Order A
                        WHERE 
                            CAST(A.CreatedOn AS DATE) BETWEEN CAST('01-01-2021' AS DATE) AND CAST(GETDATE() - 1 AS DATE)
                            AND A.CurrencyId = 2 
                            AND A.PaymentTransactionStatus = 1
                            AND A.ParentOrderID is null
                            AND A.OrderStatusId not in (1, 44)
                            AND LEFT(A.OrderRef ,3) <> 'FGM'
                        GROUP BY 
                            A.CreatedOn
                            ) Q1
                        GROUP BY 
                            Order_date
                            ) P1 ON (P0.Order_Date = P1.Order_Date)

                        LEFT JOIN
                            (
                        SELECT 
                            Order_Date,
                            SUM(Order_No) FROrderNo
                        FROM
                            (
                        SELECT 
                            CAST(A.CreatedOn AS DATE) Order_Date,
                            COUNT( DISTINCT A.OrderId) Order_No
                        FROM 
                            [feelgood.french].dbo.FG_Order A
                        WHERE 
                            CAST(A.CreatedOn AS DATE) BETWEEN CAST('01-01-2021' AS DATE) AND CAST(GETDATE() - 1 AS DATE)
                            AND A.CurrencyId = 2  
                            AND A.PaymentTransactionStatus = 1
                            AND A.ParentOrderID is null
                            AND A.OrderStatusId not in (1, 44)
                            AND LEFT(A.OrderRef ,3) <> 'FGM'
                        GROUP BY 
                            A.CreatedOn
                            ) Q2
                        GROUP BY 
                            Order_date
                        ) P2 ON (P1.Order_Date = P2.Order_Date)
                    ORDER BY 
                        ORDER_DATE
                        
                   '''
                   )

    df = pd.DataFrame([{name : row[i] for i, name in enumerate([col[0] for col in cursor.description])} for row in cursor.fetchall()])

    display(df)

    connect_0.close()

    engine = sqlalchemy.create_engine(f"mssql+pymssql://DevUser3:flgT!9585@217.174.248.77:3689/feelgood.reports")

    connect_1 = engine.connect() 

    table_name = 'fgc_all_non_mob_orders'

    df.to_sql(table_name, connect_1, if_exists = 'replace', method = 'multi', chunksize = 10000, index = False)

    connect_1.close()

if __name__ == '__main__':
    read_query()




