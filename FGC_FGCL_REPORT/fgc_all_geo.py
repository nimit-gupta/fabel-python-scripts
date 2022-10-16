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
                        SUM(fgc_all_gads.UK_IMPRESSIONS_GOOGLE) + SUM(fgc_all_gads.IE_IMPRESSIONS_GOOGLE) + SUM(fgc_all_gads.FR_IMPRESSIONS_GOOGLE) + SUM(fgc_all_mads.UK_IMPRESSIONS_BING) + SUM(fgc_all_mads.IE_IMPRESSIONS_BING) + SUM(fgc_all_mads.FR_IMPRESSIONS_BING) "TotalImpressions",
                        SUM(fgc_all_gads.UK_CLICKS_GOOGLE) + SUM(fgc_all_gads.IE_CLICKS_GOOGLE) + SUM(fgc_all_gads.FR_CLICKS_GOOGLE) + SUM(fgc_all_mads.UK_CLICKS_BING) + SUM(fgc_all_mads.IE_CLICKS_BING) + SUM(fgc_all_mads.FR_CLICKS_BING) "TotalClicks",
                        SUM(fgc_all_gads.UK_COSTS_GOOGLE) + SUM(fgc_all_gads.IE_COSTS_GOOGLE) + SUM(fgc_all_gads.FR_COSTS_GOOGLE) + SUM(fgc_all_mads.UK_COSTS_BING) + SUM(fgc_all_mads.IE_COSTS_BING) + SUM(fgc_all_mads.FR_COSTS_BING) AS "TotalCost",
                        ROUND(SUM(fgc_all_gads.UK_CONVERSIONS_GOOGLE) + SUM(fgc_all_gads.IE_CONVERSIONS_GOOGLE) + SUM(fgc_all_gads.FR_CONVERSIONS_GOOGLE)  + SUM(fgc_all_mads.UK_CONVERSIONS_BING) + SUM(fgc_all_mads.IE_CONVERSIONS_BING) + SUM(fgc_all_mads.FR_CONVERSIONS_BING),0) "TotalConversions",
                        SUM(fgc_tot_new_reg.UK_NEW_TOT_CUST) + SUM(fgc_tot_new_reg.IE_NEW_TOT_CUST) + SUM(fgc_tot_new_reg.FR_NEW_TOT_CUST) "TotalNewReg",
                        SUM(fgc_tot_new_orders.UK_TOT_NEW_ORDER) + SUM(fgc_tot_new_orders.IE_TOT_NEW_ORDER) + SUM(fgc_tot_new_orders.FR_TOT_NEW_ORDER) "TotalNewOrd",
                        SUM(fgc_tot_all_orders.UK_TOT_ALL_ORDERS) + SUM(fgc_tot_all_orders.IE_TOT_ALL_ORDERS) + SUM(fgc_tot_all_orders.FR_TOT_ALL_ORDERS) "TotalOrds",
                        SUM(fgc_all_mob_orders.UK_TOT_MOB_ORDERS) + SUM(fgc_all_mob_orders.IE_TOT_MOB_ORDERS) + SUM(ISNULL(CAST(fgc_all_mob_orders.FR_TOT_MOB_ORDERS AS FLOAT),0)) "TotalMobOrd",
                        SUM(fgc_all_non_mob_orders.UK_TOT_NON_MOB_ORDERS) + SUM(fgc_all_non_mob_orders.IE_TOT_NON_MOB_ORDERS) + SUM(fgc_all_non_mob_orders.FR_TOT_NON_MOB_ORDERS) "TotalNonMobOrd",
                        ROUND(SUM(CAST(REPLACE(fgc_all_gads.UK_REVENUE_GOOGLE,',','') AS FLOAT)) + SUM(CAST(REPLACE(fgc_all_gads.IE_REVENUE_GOOGLE,',','') AS FLOAT)) + SUM(CAST(REPLACE(fgc_all_gads.FR_REVENUE_GOOGLE,',','') AS FLOAT)) + SUM(CAST(REPLACE(fgc_all_mads.UK_REVENUE_BING,',','') AS FLOAT)) + SUM(CAST(REPLACE(fgc_all_mads.IE_REVENUE_BING,',','') AS FLOAT)) + SUM(CAST(REPLACE(fgc_all_mads.FR_REVENUE_BING,',','') AS FLOAT)),2) "TotalPPC",
                        ROUND(SUM(CAST(fgc_tot_revenue.UK_TOT_REV AS FLOAT)) + SUM(CAST(fgc_tot_revenue.IE_TOT_REV AS FLOAT)) + SUM(CAST(fgc_tot_revenue.FR_TOT_REV AS FLOAT)),2) "TotalRev",
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

    #display(df.columns)

    #Index(['Date', 'TotalImpressions', 'TotalClicks', 'TotalCost', 'TotalConversions', 'TotalNewReg','TotalNewOrd', 'TotalOrds', 'TotalMobOrd', 'TotalNonMobOrd', 'PPCRev',
    #'TotalRev', 'DayNo'],dtype='object')


    df.insert(loc = 3, column = 'TotalCTR', value = df['TotalClicks'].div(df['TotalImpressions']).mul(100).round(2))

    df.insert(loc = 4, column = 'TotalAvgCPC', value = df['TotalCost'].div(df['TotalClicks']).round(2))

    df.insert(loc = 7, column = 'TotalCPC', value = df['TotalCost'].div(df['TotalConversions']).round(2))

    df.insert(loc = 8, column = 'TotalCR', value = df['TotalConversions'].div(df['TotalClicks']).mul(100).round(2))

    #display(df.columns)    

   #Index(['Date', 'TotalImpressions', 'TotalClicks', 'TotalCTR', 'TotalAvgCPC','TotalCost', 'TotalConversions', 'TotalCPC', 'TotalCR', 'TotalNewReg',
   #'TotalNewOrd', 'TotalOrds', 'TotalMobOrd', 'TotalNonMobOrd', 'PPCRev','TotalRev', 'DayNo'],

    df.insert(loc = 14, column = 'AvgNewCust', value = df['TotalNewOrd'].div(df['DayNo']).round(0))

    df.insert(loc = 15, column = 'AvgOrd', value = df['TotalOrds'].div(df['DayNo']).round(0))

    df.insert(loc = 17, column = 'SeoDirectEmailAffMobApp', value = df['TotalRev'].sub(df['TotalPPC']))

    df.insert(loc = 19, column = 'AvgBskVal', value = df['TotalRev'].div(df['TotalOrds']).round(2))

    df.insert(loc = 20, column = 'PPCOrder%', value = df['TotalConversions'].div(df['TotalOrds']).mul(100).round(2))

    df.insert(loc = 21, column = 'PPCOrd', value = df['TotalCost'].div(df['TotalRev'].div(1.13)).mul(100).round(2))

    df.insert(loc = 22, column = 'CPATotOrd', value = df['TotalCost'].div(df['TotalOrds']).round(2))

    df1 = df.iloc[:,0:23].copy(deep = True)

    #display(df1.columns)

    df1.rename(columns = {'TotalImpressions': 'Impressions',
                          'TotalClicks': 'Clicks',
                          'TotalCTR': 'CTR',
                          'TotalAvgCPC':'Avg.CPC',
                          'TotalCost':'Cost',
                          'TotalConversions':'Conv.',
                          'TotalCPC':'CPA',
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

    #display(df1.columns)

    df1['CTR'] = df1['CTR'].map("{:,.2f}%".format)

    df1['Avg.CPC'] = df1['Avg.CPC'].map("£{:.1f}".format)

    df1['Cost'] = df1['Cost'].map("£{:.1f}".format)

    df1['CPA'] = df1['CPA'].map("£{:.1f}".format)

    df1['CR'] = df1['CR'].map("{:,.2f}%".format)

    df1['PPC Order %'] = df1['PPC Order %'].map("{:,.2f}%".format)

    df1['Spend %'] = df1['Spend %'].map("{:,.2f}%".format)

    df1['Total Revenue'] = df1['Total Revenue'].map("£{:.1f}".format)

    df1['CPA Total Orders'] = df1['CPA Total Orders'].map("{:,.2f}%".format)

    df1['Paid Search Revenue'] = df1['Paid Search Revenue'].map("£{:.1f}".format)

    df1['Seo/Direct Email/Aff/Mob App'] = df1['Seo/Direct Email/Aff/Mob App'].map("£{:.1f}".format)

    df1['Avg. Basket Value'] = df1['Avg. Basket Value'].map("£{:.1f}".format)

    now = datetime.now()
    
    dt_string = now.strftime("%A %d/%m/%Y")
    
    client = pygsheets.authorize(service_file= 'D:/Python_Deployments/FGC_FGCL_REPORT/Universal_Client_Secret.json')

    sh = client.open('FGC_FGCL_REPORT_2021_22')
    
    wks = sh.worksheet('title', 'All_Geo')
    
    wks.rows = df1.shape[0]
    
    wks.clear(start = 'A1', end = None)
    
    wks.update_value('A1', 'Updated on - ' + dt_string)
    
    wks.set_dataframe(df1, "B4", fit = False)
 
    cursor.close()

if __name__ == '__main__':
    read_query()