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
                            DATENAME( Month,fgc_all_gads.GDATE) + ' ' + DATENAME( Year,fgc_all_gads.GDATE) Date,
                            SUM(fgc_all_gads.UK_IMPRESSIONS_GOOGLE) "Impressions(G)",
                            SUM(fgc_all_gads.UK_CLICKS_GOOGLE) "Clicks(G)",
                            SUM(fgc_all_gads.UK_COSTS_GOOGLE) "Cost(G)",
                            ROUND(SUM(fgc_all_gads.UK_CONVERSIONS_GOOGLE),0) "Conversions(G)",
                            SUM(fgc_all_mads.UK_IMPRESSIONS_BING) "Impressions(B)",
                            SUM(fgc_all_mads.UK_CLICKS_BING) "Clicks(B)",
                            SUM(fgc_all_mads.UK_COSTS_BING) "Cost(B)",
                            ROUND(SUM(fgc_all_mads.UK_CONVERSIONS_BING),0) "Conversions(B)",
                            SUM(fgc_tot_all_orders.UK_TOT_ALL_ORDERS) "TotalOrds"
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
                        GROUP BY 
                            DATENAME( Month,fgc_all_gads.GDATE) + ' ' + DATENAME( Year,fgc_all_gads.GDATE)
                        ORDER BY
                            MAX(fgc_all_gads.GDATE)

                  ''')

   

    df = pd.DataFrame([{name: row[i] for i, name in enumerate([ col[0] for col in cursor.description])} for row in cursor.fetchall()])

    #display(df)

    df.insert(loc = 3, column = 'CTR(G)', value = (df['Clicks(G)'].div(df['Impressions(G)'])).mul(100).round(2))

    df.insert(loc = 4, column = 'AverageCPC(G)', value = df['Cost(G)'].div(df['Clicks(G)']).round(2))

    df.insert(loc = 7, column = 'CPA(G)', value = df['Cost(G)'].div(df['Conversions(G)']).round(2))

    df.insert(loc = 8, column = 'CR(G)', value = (df['Conversions(G)'].div(df['Clicks(G)'])).mul(100).round(2))

    df.insert(loc = 11, column = 'CTR(B)', value = (df['Clicks(B)'].div(df['Impressions(B)'])).mul(100).round(2))

    df.insert(loc = 12, column = 'AverageCPC(B)', value = df['Cost(B)'].div(df['Clicks(B)']).round(2))

    df.insert(loc = 15, column = 'CPA(B)', value = df['Cost(B)'].div(df['Conversions(B)']).round(2))

    df.insert(loc = 16, column = 'CR(B)', value = (df['Conversions(B)'].div(df['Clicks(B)'])).mul(100).round(2))

    df.insert(loc = 17, column = 'TotalImpressions', value = df['Impressions(G)'].add(df['Impressions(B)']))

    df.insert(loc = 18, column = 'TotalClicks', value = df['Clicks(G)'].add(df['Clicks(B)']))

    df.insert(loc = 19, column = 'TotalCTR', value = (df['TotalClicks'].div(df['TotalImpressions'])).mul(100).round(2))

    df.insert(loc = 20, column = 'TotalAverageCPC', value = (df['Cost(G)'].add(df['Cost(B)'])).div(df['Clicks(G)'].add(df['Clicks(B)'])).round(2))

    df.insert(loc = 21, column = 'TotalCost', value = df['Cost(G)'].add(df['Cost(B)']))

    df.insert(loc = 22, column = 'TotalConversions', value = df['Conversions(G)'].add(df['Conversions(B)']))

    df.insert(loc = 23, column = 'TotalCPA', value = df['TotalCost'].div(df['TotalConversions']).round(2))

    df.insert(loc = 24, column = 'TotalCR', value = (df['TotalConversions'].div(df['TotalClicks'])).mul(100).round(2))

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
    
    wks = sh.worksheet('title', 'All_Time_UK')
    
    wks.rows = df.shape[0]
    
    wks.clear(start = 'A1', end = None)
    
    wks.update_value('A1', 'Updated on - ' + dt_string)
    
    wks.set_dataframe(df, "B4", fit = True)

    cursor.close()

if __name__ == '__main__':
    read_query()