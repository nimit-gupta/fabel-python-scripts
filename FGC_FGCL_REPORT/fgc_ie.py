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
                        fgc_all_gads.IE_IMPRESSIONS_GOOGLE "Impression(G)",
                        fgc_all_gads.IE_CLICKS_GOOGLE "Clicks(G)",
                        fgc_all_gads.IE_CTR_GOOGLE "CTR(G)",
                        fgc_all_gads.IE_AVERAGE_CPC_GOOGLE "AverageCPC(G)",
                        fgc_all_gads.IE_COSTS_GOOGLE "Cost(G)",
                        fgc_all_gads.IE_CONVERSIONS_GOOGLE "Conversions(G)",
                        fgc_all_gads.IE_COST_PER_CONVERSION_GOOGLE "CPA(G)",
                        fgc_all_gads.IE_CONVERSION_RATE_GOOGLE "CR(G)",
                        fgc_all_gads.IE_REVENUE_GOOGLE "PPC Rev(G)",
                        
                            
                        fgc_all_mads.IE_IMPRESSIONS_BING "Impression(B)",
                        fgc_all_mads.IE_CLICKS_BING "Clicks(B)",
                        CAST(REPLACE(fgc_all_mads.IE_CTR_BING,'%','') AS FLOAT) "CTR(B)",
                        fgc_all_mads.IE_AVERAGE_CPC_BING "AverageCPC(B)",
                        fgc_all_mads.IE_COSTS_BING "Cost(B)",
                        fgc_all_mads.IE_CONVERSIONS_BING "Conversions(B)",
                        fgc_all_mads.IE_COSTPERCONVERSION_BING "CPA(B)",
                        CAST(REPLACE(fgc_all_mads.IE_CONVERSION_RATE_BING,'%','') AS FLOAT) "CR(B)",
                        fgc_all_mads.IE_REVENUE_BING "PPC Rev(B)",
                        
                        (fgc_all_gads.IE_IMPRESSIONS_GOOGLE + fgc_all_mads.IE_IMPRESSIONS_BING) "Total Impressions",
                        (fgc_all_gads.IE_CLICKS_GOOGLE + fgc_all_mads.IE_CLICKS_BING) TotalClicks,
                        (CAST((fgc_all_gads.IE_CLICKS_GOOGLE + fgc_all_mads.IE_CLICKS_BING) AS DECIMAL(10,0)) / (fgc_all_gads.IE_IMPRESSIONS_GOOGLE + fgc_all_mads.IE_IMPRESSIONS_BING)) "Total CTR",
                        ((fgc_all_gads.IE_COSTS_GOOGLE + fgc_all_mads.IE_COSTS_BING) / (fgc_all_gads.IE_CLICKS_GOOGLE + fgc_all_mads.IE_CLICKS_BING)) "Total AverageCPC",
                        (fgc_all_gads.IE_COSTS_GOOGLE + fgc_all_mads.IE_COSTS_BING) "Total Cost",
                        (fgc_all_gads.IE_CONVERSIONS_GOOGLE + fgc_all_mads.IE_CONVERSIONS_BING) "Total Conversions",
                        ((fgc_all_gads.IE_COSTS_GOOGLE + fgc_all_mads.IE_COSTS_BING) / (fgc_all_gads.IE_CONVERSIONS_GOOGLE + fgc_all_mads.IE_CONVERSIONS_BING)) "Total CPA",
                        ((fgc_all_gads.IE_CONVERSIONS_GOOGLE + fgc_all_mads.IE_CONVERSIONS_BING) / (fgc_all_gads.IE_CLICKS_GOOGLE + fgc_all_mads.IE_CLICKS_BING)) "Total CR",
                        (CAST(REPLACE(fgc_all_gads.IE_REVENUE_GOOGLE,',','') AS FLOAT) + CAST(REPLACE(fgc_all_mads.IE_REVENUE_BING,',','') AS FLOAT)) "Total PPC",
                        fgc_tot_new_reg.IE_NEW_TOT_CUST "Total New Reg",
                        fgc_tot_new_orders.IE_TOT_NEW_ORDER "Total New Ord",
                        fgc_tot_all_orders.IE_TOT_ALL_ORDERS "Total Ords",
                        fgc_tot_revenue.IE_TOT_REV "Total Rev"
                                
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
       
                 '''

                  )

    df = pd.DataFrame([{name: row[i] for i, name in enumerate([col[0] for col in cursor.description])} for row in cursor.fetchall()])

    #display(df)

    df['CTR(G)'] = df['CTR(G)'].map("{:,.2f}%".format)

    df['CR(G)'] = df['CR(G)'].map("{:,.2f}%".format)

    df['CTR(B)'] = df['CTR(B)'].map("{:,.2f}%".format)

    df['CR(B)'] = df['CR(B)'].map("{:,.2f}%".format)

    display(df)

    now = datetime.now()
    
    dt_string = now.strftime("%A %d/%m/%Y")
    
    client = pygsheets.authorize(service_file= 'D:/Python_Deployments/FGC_FGCL_REPORT/Universal_Client_Secret.json')

    sh = client.open('FGC_FGCL_REPORT_2021_22')
    
    wks = sh.worksheet('title', 'FGC_IE')
    
    wks.rows = df.shape[0]
    
    wks.clear(start = 'A1', end = None)
    
    wks.update_value('A1', 'Updated on - ' + dt_string)
    
    wks.set_dataframe(df, "B4", fit = True)

if __name__ == '__main__':
    read_query()