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
                            SUM(fgc_tot_new_reg.UK_NEW_TOT_CUST) "TotalNewReg",
                            SUM(fgc_tot_new_orders.UK_TOT_NEW_ORDER) "TotalNewOrd",
                            SUM(fgc_tot_all_orders.UK_TOT_ALL_ORDERS) "TotalOrds",
                            SUM(fgc_all_mob_orders.UK_TOT_MOB_ORDERS) "TotalMobOrd",
                            SUM(fgc_all_non_mob_orders.UK_TOT_NON_MOB_ORDERS) "TotalNonMobOrd",
                            ROUND(SUM(CAST(REPLACE(fgc_all_gads.UK_REVENUE_GOOGLE,',','') AS FLOAT)) + SUM(CAST(REPLACE(fgc_all_mads.UK_REVENUE_BING,',','') AS FLOAT)),2) "TotalPPC",
                            ROUND(SUM(CAST(fgc_tot_revenue.UK_TOT_REV AS FLOAT)),2) "TotalRev",
                            SUM(fgc_tot_all_orders.DayNo) AS "DayNo"
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
                        GROUP BY 
                            DATENAME( Month,fgc_all_gads.GDATE) + ' ' + DATENAME( Year,fgc_all_gads.GDATE)
                        ORDER BY
                            MAX(fgc_all_gads.GDATE)

                  ''')


    df = pd.DataFrame([{name: row[i] for i, name in enumerate([ col[0] for col in cursor.description])} for row in cursor.fetchall()])


    
    df.insert(loc = 9, column = 'TotalImpressions', value = df['Impressions(G)'].add(df['Impressions(B)']))

    df.insert(loc = 10, column = 'TotalClicks', value = df['Clicks(G)'].add(df['Clicks(B)']))

    df.insert(loc = 11, column = 'TotalCTR', value = (df['TotalClicks'].div(df['TotalImpressions'])).mul(100).round(2))

    df.insert(loc = 12, column = 'TotalAverageCPC', value = (df['Cost(G)'].add(df['Cost(B)'])).div(df['Clicks(G)'].add(df['Clicks(B)'])).round(2))

    df.insert(loc = 13, column = 'TotalCost', value = df['Cost(G)'].add(df['Cost(B)']))

    df.insert(loc = 14, column = 'TotalConversions', value = df['Conversions(G)'].add(df['Conversions(B)']))

    df.insert(loc = 15, column = 'TotalCPA', value = df['TotalCost'].div(df['TotalConversions']).round(2))

    df.insert(loc = 16, column = 'TotalCR', value = (df['TotalConversions'].div(df['TotalClicks'])).mul(100).round(2))

    df1 = df.iloc[:,[0,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]].copy(deep = True)

    #display(df1.columns)

    #Index(['Date', 'TotalImpressions', 'TotalClicks', 'TotalCTR',
    #       'TotalAverageCPC', 'TotalCost', 'TotalConversions', 'TotalCPA',
    #       'TotalCR', 'TotalNewReg', 'TotalNewOrd', 'TotalOrds', 'TotalMobOrd',
    #       'TotalNonMobOrd', 'TotalPPC', 'TotalRev', 'DayNo'],
    #       dtype='object')

    df1.insert(loc = 14, column = 'AvgNewCust', value = df1['TotalNewOrd'].div(df1['DayNo']).round(0))

    df1.insert(loc = 15, column = 'AvgOrd', value = df1['TotalOrds'].div(df1['DayNo']).round(0))

    df1.insert(loc = 17, column = 'SeoDirectEmailAffMobApp', value = df1['TotalRev'].sub(df1['TotalPPC']))

    df1.insert(loc = 19, column = 'AvgBskVal', value = df1['TotalRev'].div(df1['TotalOrds']).round(2))

    df1.insert(loc = 20, column = 'PPCOrder%', value = df1['TotalConversions'].div(df1['TotalOrds']).mul(100).round(2))

    df1.insert(loc = 21, column = 'PPCOrd', value = df1['TotalCost'].div(df1['TotalRev'].div(1.13)).mul(100).round(2))

    df1.insert(loc = 22, column = 'CPATotOrd', value = df1['TotalCost'].div(df1['TotalOrds']).round(2))

    df2 = df1.iloc[:,0:23].copy(deep = False)

    #display(df2.columns)

    df2.rename(columns = {'TotalImpressions': 'Impressions',
                          'TotalClicks': 'Clicks',
                          'TotalCTR': 'CTR',
                          'TotalAverageCPC':'Avg.CPC',
                          'TotalCost':'Cost',
                          'TotalConversions':'Conv.',
                          'TotalCPA':'CPA',
                          'TotalCR': 'CR',
                          'TotalNewReg':'Total Reg.',
                          'TotalNewOrd':'New Reg. & Ordered',
                          'TotalOrds':'Orders',
                          'TotalMobOrd':'Mobile App Order',
                          'TotalNonMobOrd':'Order without mobile App',
                          'AvgNewCust':'Avg. New Customers',
                          'AvgOrd':'Avg. Orders',
                          'TotalPPC':'Paid Search Revenue',
                          'SeoDirectEmailAffMobApp':'Seo/Direct Email/Aff/Mob App',
                          'TotalRev':'Total Revenue',
                          'AvgBskVal':'Avg. Basket Value',
                          'PPCOrder%':'PPC Order %',
                          'PPCOrd':'Spend %',
                          'CPATotOrd': 'CPA Total Orders'

                          }, inplace = True)

    df2['CTR'] = df2['CTR'].map("{:,.2f}%".format)

    df2['CPA'] = df2['CPA'].map("{:,.2f}%".format)

    df2['CR'] = df2['CR'].map("{:,.2f}%".format)

    df2['PPC Order %'] = df2['PPC Order %'].map("{:,.2f}%".format)

    df2['Spend %'] = df2['Spend %'].map("{:,.2f}%".format)
    
    now = datetime.now()
    
    dt_string = now.strftime("%A %d/%m/%Y")
    
    client = pygsheets.authorize(service_file= 'D:/Python_Deployments/FGC_FGCL_REPORT/Universal_Client_Secret.json')

    sh = client.open('FGC_FGCL_REPORT_2021_22')
    
    wks = sh.worksheet('title', 'UK_Topline')
    
    wks.rows = df2.shape[0]
    
    wks.clear(start = 'A1', end = None)
    
    wks.update_value('A1', 'Updated on - ' + dt_string)
    
    wks.set_dataframe(df2, "B4", fit = True)

    

if __name__ == '__main__':
    read_query()