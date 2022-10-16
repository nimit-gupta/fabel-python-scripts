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
                        UK_Order_Date ORDER_DATE,
                        UK_New_Order UK_TOT_NEW_ORDER,
                        IE_New_Order IE_TOT_NEW_ORDER,
                        FR_New_Order FR_TOT_NEW_ORDER    
                    FROM
                            (

                            SELECT
                                  UK_Order_Date,
                                  SUM(UK_New_Order) UK_New_Order
                            FROM
                                (
                            SELECT 
                                CAST(CreatedOn AS DATE) UK_Order_Date,
                                COUNT(DISTINCT OrderId) UK_New_Order
                            FROM
                                [feelgood.live].dbo.FG_ORDER   
                            WHERE 
                                CAST(CreatedOn AS DATE) BETWEEN CAST('01-01-2021' AS DATE) AND CAST(GETDATE() - 1 AS DATE)
                                AND CurrencyId = 1
                                AND PaymentTransactionStatus = 1
                                AND ParentOrderID is null
                                AND OrderStatusId not in (1, 44) 
                                AND OrderCount = 1
                            GROUP BY 
                                CreatedOn 
                               ) S1
                            GROUP BY 
                               UK_Order_Date
                            ) SQ1
                    LEFT JOIN
                            (
                            SELECT
                                  IE_Order_Date,
                                  SUM(IE_New_Order) IE_New_Order
                            FROM
                                (
                            SELECT 
                                CAST(CreatedOn AS DATE) IE_Order_Date,
                                COUNT(DISTINCT OrderId) IE_New_Order
                            FROM
                                [feelgood.live].dbo.FG_ORDER   
                            WHERE 
                                CAST(CreatedOn AS DATE) BETWEEN CAST('01-01-2021' AS DATE) AND CAST(GETDATE() - 1 AS DATE)
                                AND CurrencyId = 2
                                AND PaymentTransactionStatus = 1
                                AND ParentOrderID is null
                                AND OrderStatusId not in (1, 44) 
                                AND OrderCount = 1
                            GROUP BY 
                                CreatedOn 
                               ) S2
                            GROUP BY 
                               IE_Order_Date
                            ) SQ2 ON (SQ1.UK_Order_Date = SQ2.IE_Order_date)
                    LEFT JOIN
                            (
                            SELECT
                                  FR_Order_Date,
                                  SUM(FR_New_Order) FR_New_Order
                            FROM
                                (
                            SELECT 
                                CAST(CreatedOn AS DATE) FR_Order_Date,
                                COUNT(DISTINCT OrderId) FR_New_Order
                            FROM
                                [feelgood.french].dbo.FG_ORDER   
                            WHERE 
                                CAST(CreatedOn AS DATE) BETWEEN CAST('01-01-2021' AS DATE) AND CAST(GETDATE() - 1 AS DATE)
                                AND CurrencyId = 2
                                AND PaymentTransactionStatus = 1
                                AND ParentOrderID is null
                                AND OrderStatusId not in (1, 44) 
                                AND OrderCount = 1
                            GROUP BY 
                                CreatedOn 
                               ) S1
                            GROUP BY 
                               FR_Order_Date
                            ) SQ3 ON (SQ2.IE_Order_Date = SQ3.FR_Order_Date)
                    ORDER BY 
                        ORDER_DATE
	
                    '''
                   )

    df = pd.DataFrame([{name : row[i] for i, name in enumerate([col[0] for col in cursor.description])} for row in cursor.fetchall()])

    display(df)

    cursor.close()

    engine = sqlalchemy.create_engine(f"mssql+pymssql://DevUser3:flgT!9585@217.174.248.77:3689/feelgood.reports")

    connect_1 = engine.connect() 

    table_name = 'fgc_tot_new_orders'

    df.to_sql(table_name, connect_1, if_exists = 'replace', method = 'multi', chunksize = 10000, index = False)

    connect_1.close()


if __name__ == '__main__':
    read_query()




