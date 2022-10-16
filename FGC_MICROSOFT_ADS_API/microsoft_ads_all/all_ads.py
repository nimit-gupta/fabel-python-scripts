#!/usr/bin/env python310
#coding:utf-8

from IPython.core.display import display
import pandas as pd
import sqlalchemy
import pymssql 

def read_database():

    con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = 'flgT!9585')

    cursor = con.cursor()

    cursor.execute('''
                        SELECT 
                                A.[Time Period] MDate,
                                A.Impressions UK_IMPRESSIONS_BING,
                                A.Clicks UK_CLICKS_BING,
                                A.CTR UK_CTR_BING,
                                A.AVG_CPC UK_AVERAGE_CPC_BING,
                                A.Spend UK_COSTS_BING,
                                A.Conversions UK_CONVERSIONS_BING,
                                A.CPC UK_COSTPERCONVERSION_BING,
                                A.Conversion_Rate UK_CONVERSION_RATE_BING,
                                A.Revenue UK_REVENUE_BING,
                                B.Impressions IE_IMPRESSIONS_BING,
                                B.Clicks IE_CLICKS_BING,
                                B.CTR IE_CTR_BING,
                                B.AVG_CPC IE_AVERAGE_CPC_BING,
                                B.Spend IE_COSTS_BING,
                                B.Conversions IE_CONVERSIONS_BING,
                                B.CPC IE_COSTPERCONVERSION_BING,
                                B.Conversion_Rate IE_CONVERSION_RATE_BING,
                                B.Revenue IE_REVENUE_BING,
                                C.Impressions FR_IMPRESSIONS_BING,
                                C.Clicks FR_CLICKS_BING,
                                C.CTR FR_CTR_BING,
                                C.AVG_CPC FR_AVERAGE_CPC_BING,
                                C.Spend FR_COSTS_BING,
                                C.Conversions FR_CONVERSIONS_BING,
                                C.CPC FR_COSTPERCONVERSION_BING,
                                C.Conversion_Rate FR_CONVERSION_RATE_BING,
                                C.Revenue FR_REVENUE_BING
                                
                            FROM 
                                [feelgood.reports].dbo.fgc_uk_mads A
                            LEFT JOIN 
                                [feelgood.reports].dbo.fgc_ie_mads B ON (A.[Time Period] = B.[Time Period])
                            LEFT JOIN 
                                [feelgood.reports].dbo.fgc_fr_mads C ON (B.[Time Period] = C.[Time Period])
    
                   ''')
    
    df = pd.DataFrame([{name:row[i] for i, name in enumerate([col[0] for col in cursor.description])} for row in cursor.fetchall()])

    display(df)

    engine = sqlalchemy.create_engine(f"mssql+pymssql://DevUser3:flgT!9585@217.174.248.77:3689/feelgood.reports")

    con = engine.connect() 

    table_name = 'fgc_all_mads'

    df.to_sql(table_name, con, if_exists = 'replace', method = 'multi', chunksize = 10000, index = False)

if __name__ == '__main__':
    read_database()