#! /usr/bin/env python310
#coding:utf-8

'''
@author - Nimit Gupta

'''

from IPython.core.display import display
from datetime import datetime
import pandas as pd
import pygsheets
import pymssql

pd.set_option("display.max_columns", 100)

def read_query():

    connect = pymssql.connect( host = r'217.174.248.77',
                               port = 3689,
                               user = r'DevUser3',
                               password = r'flgT!9585',
                               database = r'feelgood.reports')

    cursor = connect.cursor()

    cursor.execute('''
                    SELECT 
                        CAST(fgc_all_gads.GDATE AS DATE) "Date",
                        ISNULL(fgc_all_gads.UK_IMPRESSIONS_GOOGLE + fgc_all_gads.IE_IMPRESSIONS_GOOGLE + fgc_all_gads.FR_IMPRESSIONS_GOOGLE, 0) "Impressions(G)",
                        ISNULL(fgc_all_gads.UK_CLICKS_GOOGLE + fgc_all_gads.IE_CLICKS_GOOGLE + fgc_all_gads.FR_CLICKS_GOOGLE, 0) "Clicks(G)",
                        ISNULL(fgc_all_gads.UK_COSTS_GOOGLE + fgc_all_gads.IE_COSTS_GOOGLE + fgc_all_gads.FR_COSTS_GOOGLE, 0) "Cost(G)",
                        ISNULL(ROUND(fgc_all_gads.UK_CONVERSIONS_GOOGLE + fgc_all_gads.IE_CONVERSIONS_GOOGLE + fgc_all_gads.FR_CONVERSIONS_GOOGLE, 0),0) "Conversions(G)",
                        ISNULL(CAST(REPLACE(fgc_all_gads.UK_REVENUE_GOOGLE,',','') AS FLOAT) + CAST(REPLACE(fgc_all_gads.IE_REVENUE_GOOGLE,',','') AS FLOAT) + CAST(REPLACE(fgc_all_gads.FR_REVENUE_GOOGLE,',','') AS FLOAT), 0) "PPCRev(G)",
                        ISNULL(fgc_all_mads.UK_IMPRESSIONS_BING + fgc_all_mads.IE_IMPRESSIONS_BING + fgc_all_mads.FR_IMPRESSIONS_BING, 0) "Impressions(B)",
                        ISNULL(fgc_all_mads.UK_CLICKS_BING + fgc_all_mads.IE_CLICKS_BING + fgc_all_mads.FR_CLICKS_BING, 0)  "Clicks(B)",
                        ISNULL(fgc_all_mads.UK_COSTS_BING + fgc_all_mads.IE_COSTS_BING + fgc_all_mads.FR_COSTS_BING, 0) "Cost(B)",
                        ISNULL(ROUND(fgc_all_mads.UK_CONVERSIONS_BING + fgc_all_mads.IE_CONVERSIONS_BING + fgc_all_mads.FR_CONVERSIONS_BING, 0),0) "Conversions(B)",
                        ISNULL(CAST(REPLACE(fgc_all_mads.UK_REVENUE_BING,',','') AS FLOAT) + CAST(REPLACE(fgc_all_mads.IE_REVENUE_BING,',','') AS FLOAT) + CAST(REPLACE(fgc_all_mads.FR_REVENUE_BING,',','') AS FLOAT), 0) "PPCRev(B)",
                        ISNULL(fgc_tot_new_reg.UK_NEW_TOT_CUST + fgc_tot_new_reg.IE_NEW_TOT_CUST + fgc_tot_new_reg.FR_NEW_TOT_CUST, 0) "Total New Reg",
                        ISNULL(fgc_tot_new_orders.UK_TOT_NEW_ORDER + fgc_tot_new_orders.IE_TOT_NEW_ORDER + fgc_tot_new_orders.FR_TOT_NEW_ORDER, 0) "Total New Ord",
                        ISNULL(fgc_tot_all_orders.UK_TOT_ALL_ORDERS + fgc_tot_all_orders.IE_TOT_ALL_ORDERS + fgc_tot_all_orders.FR_TOT_ALL_ORDERS, 0) "Total Ords",
                        ISNULL(ROUND(CAST(fgc_tot_revenue.UK_TOT_REV AS FLOAT) + CAST(fgc_tot_revenue.IE_TOT_REV AS FLOAT) + CAST(fgc_tot_revenue.FR_TOT_REV AS FLOAT),2),0) "Total Rev"
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
                    LEFT JOIN 
                        fgc_all_mob_orders ON (CAST(fgc_tot_all_orders.ORDER_DATE AS DATE) = CAST(fgc_all_mob_orders.ORDER_DATE AS DATE))
                    LEFT JOIN 
                        fgc_all_non_mob_orders ON (CAST(fgc_all_mob_orders.ORDER_DATE AS DATE) = CAST(fgc_all_non_mob_orders.ORDER_DATE AS DATE))
                    ORDER BY
                        CAST(fgc_all_gads.GDATE AS DATE)

                  ''')


    df = pd.DataFrame([{name: row[i] for i, name in enumerate([ col[0] for col in cursor.description])} for row in cursor.fetchall()])

    #Index(['Date', 'Impression(G)', 'Clicks(G)', 'Cost(G)', 'Conversions(G)','PPCRev(G)', 'Impression(B)', 'Clicks(B)', 'Cost(B)', 'Conversions(B)',
    # 'PPCRev(B)', 'Total New Reg', 'Total New Ord', 'Total Ords','Total Rev'], dtype='object')

    df.insert(loc = 3, column = 'CTR(G)', value = df['Clicks(G)'].div(df['Impressions(G)']).mul(100).round(2))

    df.insert(loc = 4, column = 'AvgCPC(G)', value = df['Cost(G)'].div(df['Clicks(G)']).round(2))

    df.insert(loc = 7, column = 'CPC(G)', value = df['Cost(G)'].div(df['Conversions(G)']).round(2))

    df.insert(loc = 8, column = 'CR(G)', value = df['Conversions(G)'].div(df['Clicks(G)']).mul(100).round(2))

    df.insert(loc = 11, column = 'CTR(B)', value = df['Clicks(B)'].div(df['Impressions(B)']).mul(100).round(2))

    df.insert(loc = 12, column = 'AvgCPC(B)', value = df['Cost(B)'].div(df['Clicks(B)']).round(2))

    df.insert(loc = 15, column = 'CPC(B)', value = df['Cost(B)'].div(df['Conversions(B)']).round(2))

    df.insert(loc = 16, column = 'CR(B)', value = df['Conversions(B)'].div(df['Clicks(B)']).mul(100).round(2))

    df.insert(loc = 18, column = 'TotalImpressions', value = df['Impressions(G)'].add(df['Impressions(B)']))

    df.insert(loc = 19, column = 'TotalClicks', value = df['Clicks(G)'].add(df['Clicks(B)']))

    df.insert(loc = 20, column = 'TotalCTR', value = (df['TotalClicks'].div(df['TotalImpressions'])).mul(100).round(2))

    df.insert(loc = 21, column = 'TotalAverageCPC', value = (df['Cost(G)'].add(df['Cost(B)'])).div(df['Clicks(G)'].add(df['Clicks(B)'])).round(2))

    df.insert(loc = 22, column = 'TotalCost', value = df['Cost(G)'].add(df['Cost(B)']))

    df.insert(loc = 23, column = 'TotalConversions', value = df['Conversions(G)'].add(df['Conversions(B)']))

    df.insert(loc = 24, column = 'TotalCPA', value = df['TotalCost'].div(df['TotalConversions']).round(2))

    df.insert(loc = 25, column = 'TotalCR', value = (df['TotalConversions'].div(df['TotalClicks'])).mul(100).round(2))

    #display(df)

    df['CTR(G)'] = df['CTR(G)'].map("{:,.2f}%".format)

    df['CR(G)'] = df['CR(G)'].map("{:,.2f}%".format)

    df['CTR(B)'] = df['CTR(B)'].map("{:,.2f}%".format)

    df['CR(B)'] = df['CR(B)'].map("{:,.2f}%".format)

    df['TotalCTR'] = df['TotalCTR'].map("{:,.2f}%".format)

    df['TotalCR'] = df['TotalCR'].map("{:,.2f}%".format)

    now = datetime.now()
    
    dt_string = now.strftime("%A %d/%m/%Y")
    
    client = pygsheets.authorize(service_file= 'D:/Python_Deployments/FGC_FGCL_REPORT/Universal_Client_Secret.json')

    sh = client.open('FGC_FGCL_REPORT_2021_22')
    
    wks = sh.worksheet('title', 'Account_Report_All_Geo')
    
    wks.rows = df.shape[0]
    
    wks.clear(start = 'A1', end = None)
    
    wks.update_value('A1', 'Updated on - ' + dt_string)
    
    wks.set_dataframe(df, "B4", fit = True)

    cursor.close()

if __name__ == '__main__':
    read_query()