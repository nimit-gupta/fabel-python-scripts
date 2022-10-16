#!/usr/bin/env python
#-*- coding:utf-8 -*-

from IPython.core.display import display
import pandas as pd
import pymssql
import sqlalchemy 

def read_query():

    con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585')

    query = '''
               SELECT 
                    A.[DATE] GDATE, 
                    A.Impressions UK_IMPRESSIONS_GOOGLE,
                    A.Clicls UK_CLICKS_GOOGLE,
                    A.CTR UK_CTR_GOOGLE, 
                    A.Average_Cpc UK_AVERAGE_CPC_GOOGLE, 
                    A.Costs UK_COSTS_GOOGLE,
                    A.Conversions UK_CONVERSIONS_GOOGLE, 
                    A.Cost_Per_Conversion UK_COST_PER_CONVERSION_GOOGLE,
                    A.Conversion_Rate UK_CONVERSION_RATE_GOOGLE,
                    A.Revenue UK_REVENUE_GOOGLE, 
                    B.Impressions IE_IMPRESSIONS_GOOGLE,
                    B.Clicls IE_CLICKS_GOOGLE,
                    B.CTR IE_CTR_GOOGLE, 
                    B.Average_Cpc IE_AVERAGE_CPC_GOOGLE, 
                    B.Costs IE_COSTS_GOOGLE,
                    B.Conversions IE_CONVERSIONS_GOOGLE, 
                    B.Cost_Per_Conversion IE_COST_PER_CONVERSION_GOOGLE,
                    B.Conversion_Rate IE_CONVERSION_RATE_GOOGLE,
                    B.Revenue IE_REVENUE_GOOGLE,
                    C.Impressions FR_IMPRESSIONS_GOOGLE,
                    C.Clicls FR_CLICKS_GOOGLE,
                    C.CTR FR_CTR_GOOGLE, 
                    C.Average_Cpc FR_AVERAGE_CPC_GOOGLE, 
                    C.Costs FR_COSTS_GOOGLE,
                    C.Conversions FR_CONVERSIONS_GOOGLE, 
                    C.Cost_Per_Conversion FR_COST_PER_CONVERSION_GOOGLE,
                    C.Conversion_Rate FR_CONVERSION_RATE_GOOGLE,
                    C.Revenue FR_REVENUE_GOOGLE 
                FROM 
                    [feelgood.reports].dbo.fgc_uk_gads A
                LEFT JOIN 
                    [feelgood.reports].dbo.fgc_ie_gads B ON A.[DATE] = B.[DATE]
                LEFT JOIN 
                    [feelgood.reports].dbo.fgc_fr_gads C ON B.[DATE] = C.[DATE]
                

            '''

    df = pd.read_sql_query(query, con)

    display(df)

    engine = sqlalchemy.create_engine(f"mssql+pymssql://DevUser3:flgT!9585@217.174.248.77:3689/feelgood.reports")

    con = engine.connect() 

    table_name = 'fgc_all_gads'

    df.to_sql(table_name, con, if_exists = 'replace', method = 'multi', chunksize = 10000, index = False)


    
    
    
    