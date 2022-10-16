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
                            P0.UKOrderRev UK_TOT_REV,
                            P1.IEOrderRev IE_TOT_REV,
                            P2.FROrderRev FR_TOT_REV
                            
                        FROM
                        (
                        SELECT 
                            Order_Date,
                            SUM(Order_Rev) UKOrderRev
                            
                        FROM
                            (
                        SELECT 
                            CAST(A.CreatedOn AS DATE) Order_Date,
                            ROUND(SUM(A.NetPayable),2) Order_Rev
                            
                        FROM 
                            [feelgood.live].dbo.FG_Order A
                        WHERE 
                            CAST(A.CreatedOn AS DATE) BETWEEN CAST('01-01-2021' AS DATE) AND CAST(GETDATE() - 1 AS DATE)
                            AND A.CurrencyId = 1 
                            AND A.PaymentTransactionStatus = 1
                            AND A.ParentOrderID is null
                            AND A.OrderStatusId not in (1, 44)
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
                            SUM(Order_Rev) IEOrderRev
                        FROM
                            (
                        SELECT 
                            CAST(A.CreatedOn AS DATE) Order_Date,
                            ROUND(SUM(A.NetPayable),2) Order_Rev
                        FROM 
                            [feelgood.live].dbo.FG_Order A
                        WHERE 
                            CAST(A.CreatedOn AS DATE) BETWEEN CAST('01-01-2021' AS DATE) AND CAST(GETDATE() - 1 AS DATE)
                            AND A.CurrencyId = 2 
                            AND A.PaymentTransactionStatus = 1
                            AND A.ParentOrderID is null
                            AND A.OrderStatusId not in (1, 44)
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
                            SUM(Order_Rev) FROrderRev
                        FROM
                            (
                        SELECT 
                            CAST(A.CreatedOn AS DATE) Order_Date,
                            ROUND(SUM(A.GrandTotalAmount),2) Order_Rev
                        FROM 
                            [feelgood.french].dbo.FG_Order A
                        WHERE 
                            CAST(A.CreatedOn AS DATE) BETWEEN CAST('01-01-2021' AS DATE) AND CAST(GETDATE() - 1 AS DATE)
                            AND A.CurrencyId = 2 
                            AND A.PaymentTransactionStatus = 1
                            AND A.ParentOrderID is null
                            AND A.OrderStatusId not in (1, 44)
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

    cursor.close()

    engine = sqlalchemy.create_engine(f"mssql+pymssql://DevUser3:flgT!9585@217.174.248.77:3689/feelgood.reports")

    connect_1 = engine.connect() 

    table_name = 'fgc_tot_revenue'

    df.to_sql(table_name, connect_1, if_exists = 'replace', method = 'multi', chunksize = 10000, index = False)

    connect_1.close()


if __name__ == '__main__':
    read_query()




