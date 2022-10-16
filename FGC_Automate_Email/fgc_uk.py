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
                        (fgc_all_gads.UK_IMPRESSIONS_GOOGLE + fgc_all_mads.UK_IMPRESSIONS_BING) "Impressions",
                        (fgc_all_gads.UK_CLICKS_GOOGLE + fgc_all_mads.UK_CLICKS_BING) "Clicks",
                        ROUND(((CAST((fgc_all_gads.UK_CLICKS_GOOGLE + fgc_all_mads.UK_CLICKS_BING) AS DECIMAL(10,0)) / (fgc_all_gads.UK_IMPRESSIONS_GOOGLE + fgc_all_mads.UK_IMPRESSIONS_BING)) * 100), 2) "CTR",
                        ROUND(((fgc_all_gads.UK_COSTS_GOOGLE + fgc_all_mads.UK_COSTS_BING) / (fgc_all_gads.UK_CLICKS_GOOGLE + fgc_all_mads.UK_CLICKS_BING)),2) "Avg.CPC",
                        (fgc_all_gads.UK_COSTS_GOOGLE + fgc_all_mads.UK_COSTS_BING) "Cost",
                        ROUND((fgc_all_gads.UK_CONVERSIONS_GOOGLE + fgc_all_mads.UK_CONVERSIONS_BING),0) "Conversions",
                        ROUND(((fgc_all_gads.UK_COSTS_GOOGLE + fgc_all_mads.UK_COSTS_BING) / (fgc_all_gads.UK_CONVERSIONS_GOOGLE + fgc_all_mads.UK_CONVERSIONS_BING)),2) "CPA",
                        ROUND(((fgc_all_gads.UK_CONVERSIONS_GOOGLE + fgc_all_mads.UK_CONVERSIONS_BING) / (fgc_all_gads.UK_CLICKS_GOOGLE + fgc_all_mads.UK_CLICKS_BING)) * 100,2) "CR",
                        ROUND((CAST(REPLACE(fgc_all_gads.UK_REVENUE_GOOGLE,',','') AS FLOAT) + CAST(REPLACE(fgc_all_mads.UK_REVENUE_BING,',','') AS FLOAT)),2) "PPC Revenue",
                        ROUND(fgc_tot_new_reg.UK_NEW_TOT_CUST,0) "New Reg",
                        ROUND(fgc_tot_new_orders.UK_TOT_NEW_ORDER,0) "Total New",
                        ROUND(fgc_tot_all_orders.UK_TOT_ALL_ORDERS,0) "Orders",
                        ROUND(fgc_tot_revenue.UK_TOT_REV,0) "Total Revenue"
                                
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

    