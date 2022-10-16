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
                            OQ0.REG_DATE REG_DATE,
                            OQ0.UK_CUST UK_NEW_TOT_CUST,
                            OQ1.IE_CUST IE_NEW_TOT_CUST,
                            OQ2.FR_CUST FR_NEW_TOT_CUST

                        FROM 
                            (

                                SELECT 
                                    REG_DATE,
                                    SUM(NO_CUST) UK_CUST
                                FROM
                                    (
                                SELECT 
                                    CAST(CreatedOn AS DATE) REG_DATE, 
                                    COUNT(CustomerId) NO_CUST
                                FROM 
                                    [feelgood.live].dbo.FG_Customer 
                                WHERE 
                                    CAST(CreatedOn AS DATE) BETWEEN CAST('01-01-2021' AS DATE) AND CAST(GETDATE() - 1 AS DATE)
                                    AND Enable = 1
                                    AND Active = 1
                                    AND Website ='UK'
                                GROUP BY 
                                    CreatedOn 
                                    ) IQ0
                                GROUP BY 
                                    REG_DATE
                                    
                            ) OQ0
                            
                        LEFT JOIN 
                            
                            (
                                
                                SELECT 
                                    REG_DATE,
                                    SUM(NO_CUST) IE_CUST
                                FROM
                                    (
                                SELECT 
                                    CAST(CreatedOn AS DATE) REG_DATE, 
                                    COUNT(CustomerId) NO_CUST
                                FROM 
                                    [feelgood.live].dbo.FG_Customer 
                                WHERE 
                                    CAST(CreatedOn AS DATE) BETWEEN CAST('01-01-2021' AS DATE) AND CAST(GETDATE() - 1 AS DATE)
                                    AND Enable = 1
                                    AND Active = 1
                                    AND Website ='IE'
                                GROUP BY 
                                    CreatedOn 
                                    ) IQ1
                                GROUP BY 
                                    REG_DATE
                                    
                            ) OQ1 ON (OQ0.REG_DATE = OQ1.REG_DATE)
                            
                        LEFT JOIN 
                        
                            (
                            
                                SELECT 
                                    REG_DATE,
                                    SUM(NO_CUST) FR_CUST
                                FROM
                                    (
                                SELECT 
                                    CAST(CreatedOn AS DATE) REG_DATE, 
                                    COUNT(CustomerId) NO_CUST
                                FROM 
                                    [feelgood.french].dbo.FG_Customer 
                                WHERE 
                                    CAST(CreatedOn AS DATE) BETWEEN CAST('01-01-2021' AS DATE) AND CAST(GETDATE() - 1 AS DATE)
                                    AND Enable = 1
                                    AND Active = 1
                                GROUP BY 
                                    CreatedOn 
                                    ) IQ2
                                GROUP BY 
                                    REG_DATE
                                    
                            ) OQ2 ON (OQ1.REG_DATE = OQ2.REG_DATE)
                        ORDER BY 
                            REG_DATE
	
 
                    '''
                   )

    df = pd.DataFrame([{name : row[i] for i, name in enumerate([col[0] for col in cursor.description])} for row in cursor.fetchall()])

    display(df)

    cursor.close()

    engine = sqlalchemy.create_engine(f"mssql+pymssql://DevUser3:flgT!9585@217.174.248.77:3689/feelgood.reports")

    connect_1 = engine.connect() 

    table_name = 'fgc_tot_new_reg'

    df.to_sql(table_name, connect_1, if_exists = 'replace', method = 'multi', chunksize = 10000, index = False)

    connect_1.close()


if __name__ == '__main__':
    read_query()




