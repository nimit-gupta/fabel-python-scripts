#!/usr/bin/env/ python310
#coding:utf-8

'''
@author - Nimit Gupta

'''

from IPython.core.display import display 
from datetime import datetime
import pandas as pd
import pymssql
import pygsheets 

def read_query():

    con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = 'feelgood.reports')

    cursor = con.cursor()

    cursor.execute(
                   '''
                    SELECT 

                        CAST(fgc_all_gads.GDATE AS DATE) "Date",
                        ISNULL((fgc_all_gads.FR_IMPRESSIONS_GOOGLE + fgc_all_mads.FR_IMPRESSIONS_BING),0) "Impressions",
                        ISNULL((fgc_all_gads.FR_CLICKS_GOOGLE + fgc_all_mads.FR_CLICKS_BING),0) "Clicks",
                        ISNULL(ROUND(((CAST((fgc_all_gads.FR_CLICKS_GOOGLE + fgc_all_mads.FR_CLICKS_BING) AS DECIMAL(10,0)) / (fgc_all_gads.FR_IMPRESSIONS_GOOGLE + fgc_all_mads.FR_IMPRESSIONS_BING)) * 100), 2) ,0) "CTR",
                        ISNULL(ROUND(((fgc_all_gads.FR_COSTS_GOOGLE + fgc_all_mads.FR_COSTS_BING) / (fgc_all_gads.FR_CLICKS_GOOGLE + fgc_all_mads.FR_CLICKS_BING)),2),0) "Avg.CPC",
                        ISNULL((fgc_all_gads.FR_COSTS_GOOGLE + fgc_all_mads.FR_COSTS_BING),0) "Cost",
                        ISNULL(ROUND((fgc_all_gads.FR_CONVERSIONS_GOOGLE + fgc_all_mads.FR_CONVERSIONS_BING),0),0) "Conversions",
                        ISNULL(ROUND(((fgc_all_gads.FR_COSTS_GOOGLE + fgc_all_mads.FR_COSTS_BING) / (fgc_all_gads.FR_CONVERSIONS_GOOGLE + fgc_all_mads.FR_CONVERSIONS_BING)),2),0) "CPA",
                        ISNULL(ROUND(((fgc_all_gads.FR_CONVERSIONS_GOOGLE + fgc_all_mads.FR_CONVERSIONS_BING) / (fgc_all_gads.FR_CLICKS_GOOGLE + fgc_all_mads.FR_CLICKS_BING)) * 100,2),0) "CR",
                        ISNULL(ROUND((CAST(REPLACE(fgc_all_gads.FR_REVENUE_GOOGLE,',','') AS FLOAT) + CAST(REPLACE(fgc_all_mads.FR_REVENUE_BING,',','') AS FLOAT)),2),0) "PPC Revenue",
                        ISNULL(ROUND(fgc_tot_new_reg.FR_NEW_TOT_CUST,0),0) "New Reg",
                        ISNULL(ROUND(fgc_tot_new_orders.FR_TOT_NEW_ORDER,0),0) "Total New",
                        ISNULL(ROUND(fgc_tot_all_orders.FR_TOT_ALL_ORDERS,0),0) "Orders",
                        ISNULL(ROUND(fgc_tot_revenue.FR_TOT_REV,0),0) "Total Revenue"
                                
                    FROM 
                        
                        fgc_all_gads
                        
                    LEFT JOIN 

                        fgc_all_mads ON (CAST(fgc_all_gads.GDATE AS DATE) =  CAST(fgc_all_mads.MDate AS DATE))
                        
                    LEFT JOIN 

                        fgc_tot_new_reg ON (CAST(fgc_tot_new_reg.REG_DATE AS DATE) = CAST(fgc_all_mads.MDate AS DATE))
                    LEFT JOIN 
                        
                        fgc_tot_new_orders ON (CAST(fgc_tot_new_orders.ORDER_DATE AS DATE) = CAST(fgc_tot_new_reg.REG_DATE AS DATE))
                        
                    LEFT JOIN 

                        fgc_tot_all_orders ON (CAST(fgc_tot_all_orders.ORDER_DATE AS DATE) = CAST(fgc_tot_new_orders.ORDER_DATE AS DATE))
                        
                    LEFT JOIN 
                        
                        fgc_tot_revenue ON (CAST(fgc_tot_revenue.ORDER_DATE AS DATE) = CAST(fgc_tot_all_orders.ORDER_DATE AS DATE))

                    WHERE 

                         CAST(fgc_all_gads.GDATE AS DATE) BETWEEN CAST(DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0) AS DATE) AND CAST(GETDATE() - 1 AS DATE)
                 '''

                  )

    df = pd.DataFrame([{name: row[i] for i, name in enumerate([col[0] for col in cursor.description])} for row in cursor.fetchall()])

    #display(df)

    df['CTR'] = df['CTR'].astype(float).round(2)

    df['CTR'] = df['CTR'].map("{:,.2f}%".format)

    df['CR'] = df['CR'].map("{:,.2f}%".format)

    df['Total Revenue'] = df['Total Revenue'].map("£{:.1f}".format)

    df['Cost'] = df['Cost'].map("£{:.1f}".format)

    df['CPA'] = df['CPA'].map("£{:.1f}".format)

    return df
    
