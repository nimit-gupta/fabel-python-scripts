#! /usr/bin/env python310
#coding:utf-8

'''
@author - Nimit Gupta

'''

from distutils.util import copydir_run_2to3
from IPython.core.display import display
from datetime import datetime
import pandas as pd
import pygsheets
import pymssql

import warnings
warnings.filterwarnings(action='ignore', category=FutureWarning)

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
                            DATENAME( Month,fgc_all_gads.GDATE) + ' ' + DATENAME( Year,fgc_all_gads.GDATE) FGCLDate,
                            'UK' AS 'UK',
                            ROUND(SUM(CAST(fgc_tot_revenue.UK_TOT_REV AS FLOAT)),2) "UKRev",
                            SUM(fgc_tot_all_orders.UK_TOT_ALL_ORDERS) "UKSales",
                            SUM(fgc_tot_new_orders.UK_TOT_NEW_ORDER) "UKNewReg",
                            ROUND(SUM(fgc_tot_all_orders.UK_TOT_ALL_ORDERS) / SUM(fgc_tot_all_orders.DayNo),0) "UKAvg",
                            ROUND(SUM(fgc_tot_new_orders.UK_TOT_NEW_ORDER) / SUM(fgc_tot_all_orders.DayNo),0) "UKNrAvg",
                            --,
                            ROUND((SUM(CAST(fgc_tot_revenue.UK_TOT_REV AS FLOAT))/SUM(fgc_tot_all_orders.DayNo)) * DAY(EOMONTH(GETDATE())),2) "UKPRev",
                            ROUND((SUM(fgc_tot_all_orders.UK_TOT_ALL_ORDERS)/SUM(fgc_tot_all_orders.DayNo)) * DAY(EOMONTH(GETDATE())),0) "UKPSales",
                            ROUND((SUM(fgc_tot_new_orders.UK_TOT_NEW_ORDER)/SUM(fgc_tot_all_orders.DayNo)) * DAY(EOMONTH(GETDATE())),0) "UKPNewReg",
                            ROUND((SUM(fgc_all_gads.UK_COSTS_GOOGLE + fgc_all_mads.UK_COSTS_BING)/SUM(fgc_tot_all_orders.DayNo)) * DAY(EOMONTH(GETDATE())), 2) "UKPSpnd",

                            'IE' AS 'IE',
                            ROUND(SUM(CAST(fgc_tot_revenue.IE_TOT_REV AS FLOAT)),2) "IERev",
                            SUM(fgc_tot_all_orders.IE_TOT_ALL_ORDERS) "IESales",
                            SUM(fgc_tot_new_orders.IE_TOT_NEW_ORDER) "IENewReg",
                            ROUND(SUM(fgc_tot_all_orders.IE_TOT_ALL_ORDERS) / SUM(fgc_tot_all_orders.DayNo),0) "IEAvg",
                            ROUND(SUM(fgc_tot_new_orders.IE_TOT_NEW_ORDER) / SUM(fgc_tot_all_orders.DayNo),0) "IENrAvg",
                            --,
                            ROUND((SUM(CAST(fgc_tot_revenue.IE_TOT_REV AS FLOAT))/SUM(fgc_tot_all_orders.DayNo)) * DAY(EOMONTH(GETDATE())),2) "IEPRev",
                            ROUND((SUM(fgc_tot_all_orders.IE_TOT_ALL_ORDERS)/SUM(fgc_tot_all_orders.DayNo)) * DAY(EOMONTH(GETDATE())),0) "IEPSales",
                            ROUND((SUM(fgc_tot_new_orders.IE_TOT_NEW_ORDER)/SUM(fgc_tot_all_orders.DayNo)) * DAY(EOMONTH(GETDATE())),0) "IEPNewReg",
                            ROUND((SUM(fgc_all_gads.IE_COSTS_GOOGLE + fgc_all_mads.IE_COSTS_BING)/SUM(fgc_tot_all_orders.DayNo)) * DAY(EOMONTH(GETDATE())), 2) "IEPSpnd",

                            'FR' AS 'FR',
                            ROUND(SUM(CAST(fgc_tot_revenue.FR_TOT_REV AS FLOAT)),2) "FRRev",
                            SUM(fgc_tot_all_orders.FR_TOT_ALL_ORDERS) "FRSales",
                            SUM(fgc_tot_new_orders.FR_TOT_NEW_ORDER) "FRNewReg",
                            ROUND(SUM(fgc_tot_all_orders.FR_TOT_ALL_ORDERS) / SUM(fgc_tot_all_orders.DayNo),0) "FRAvg",
                            ROUND(SUM(fgc_tot_new_orders.FR_TOT_NEW_ORDER) / SUM(fgc_tot_all_orders.DayNo),0) "FRNrAvg",
                            --,
                            ROUND((SUM(CAST(fgc_tot_revenue.FR_TOT_REV AS FLOAT))/SUM(fgc_tot_all_orders.DayNo)) * DAY(EOMONTH(GETDATE())),2) "FRPRev",
                            ROUND((SUM(fgc_tot_all_orders.FR_TOT_ALL_ORDERS)/SUM(fgc_tot_all_orders.DayNo)) * DAY(EOMONTH(GETDATE())),0) "FRPSales",
                            ROUND((SUM(fgc_tot_new_orders.FR_TOT_NEW_ORDER)/SUM(fgc_tot_all_orders.DayNo)) * DAY(EOMONTH(GETDATE())),0) "FRPNewReg",
                            ROUND((SUM(fgc_all_gads.FR_COSTS_GOOGLE + fgc_all_mads.FR_COSTS_BING)/SUM(fgc_tot_all_orders.DayNo)) * DAY(EOMONTH(GETDATE())), 2) "FRPSpnd"
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

    df = df.tail(n=3).copy(deep = True)

    df1 = df.tail(n=1).copy(deep = True)

    #display(df)

    #display(df1)

    df['UKRev'] = df['UKRev'].map("£{:.1f}".format)

    df['UKPRev'] = df['UKPRev'].map("£{:.1f}".format)

    df['UKPSpnd'] = df['UKPSpnd'].map("£{:.1f}".format)

    df['IERev'] = df['IERev'].map("€{:.1f}".format)

    df['IEPRev'] = df['IEPRev'].map("€{:.1f}".format)

    df['IEPSpnd'] = df['IEPSpnd'].map("€{:.1f}".format)

    df['FRRev'] = df['FRRev'].map("€{:.1f}".format)

    df['FRPRev'] = df['FRPRev'].map("€{:.1f}".format)

    df['FRPSpnd'] = df['FRPSpnd'].map("€{:.1f}".format)

    df1['UKRev'] = df1['UKRev'].map("£{:.1f}".format)

    df1['UKPRev'] = df1['UKPRev'].map("£{:.1f}".format)

    df1['UKPSpnd'] = df1['UKPSpnd'].map("£{:.1f}".format)

    df1['IERev'] = df1['IERev'].map("€{:.1f}".format)

    df1['IEPRev'] = df1['IEPRev'].map("€{:.1f}".format)

    df1['IEPSpnd'] = df1['IEPSpnd'].map("€{:.1f}".format)

    df1['FRRev'] = df1['FRRev'].map("€{:.1f}".format)

    df1['FRPRev'] = df1['FRPRev'].map("€{:.1f}".format)

    df1['FRPSpnd'] = df1['FRPSpnd'].map("€{:.1f}".format)

    #display(df)

    #display(df1)

    df['FGCLDate'] = (pd.to_datetime(df['FGCLDate']))

    df1['FGCLDate'] = (pd.to_datetime(df1['FGCLDate']))

    df['FGCLDate'] = df['FGCLDate'].dt.date

    df1['FGCLDate'] = df1['FGCLDate'].dt.date

    grp1 = df.groupby(['FGCLDate','UK'])[['UKRev', 'UKSales', 'UKAvg']].sum(numeric_only = False).rename(columns = {'UKRev': 'Revenue','UKSales':'Sales','UKAvg': 'Sales Avg./Day '})
  
    grpuk = grp1.unstack(0).swaplevel(0, 1, 1).sort_index(1).reset_index()

    #display(grpuk)

    grp2 = df.groupby(['FGCLDate','IE'])[['IERev', 'IESales', 'IEAvg']].sum(numeric_only = False).rename(columns = {'IERev': 'Revenue','IESales':'Sales','IEAvg': 'Sales Avg/Day '})

    grpie = grp2.unstack(0).swaplevel(0, 1, 1).sort_index(1).reset_index()

    #display(grpie)

    grp3 = df.groupby(['FGCLDate','FR'])[['FRRev', 'FRSales', 'FRAvg']].sum(numeric_only = False).rename(columns = {'FRRev': 'Revenue','FRSales':'Sales','FRAvg': 'Sales Avg/Day '})

    grpfr = grp3.unstack(0).swaplevel(0, 1, 1).sort_index(1).reset_index()

    #display(grpfr)

    grp4 = df.groupby(['FGCLDate','UK'])[['UKNewReg', 'UKNrAvg']].sum(numeric_only = False).rename(columns = {'UKNewReg': 'New Reg','UKNrAvg': 'New Reg Avg/Day '})

    grpuk1 = grp4.unstack(0).swaplevel(0, 1, 1).sort_index(1).reset_index()

    #display(grpuk1)

    grp5 = df.groupby(['FGCLDate','IE'])[['IENewReg', 'IENrAvg']].sum(numeric_only = False).rename(columns = {'IENewReg': 'New Reg','IENrAvg': 'New Reg Avg/Day '})

    grpie1 = grp5.unstack(0).swaplevel(0, 1, 1).sort_index(1).reset_index()

    #display(grpie1)

    grp6 = df.groupby(['FGCLDate','FR'])[['FRNewReg', 'FRNrAvg']].sum(numeric_only = False).rename(columns = {'FRNewReg': 'New Reg','FRNrAvg': 'New Reg Avg/Day '})

    grpfr1 = grp6.unstack(0).swaplevel(0, 1, 1).sort_index(1).reset_index()

    #display(grpfr1)

    grp7 = df1.groupby(['FGCLDate','UK'])[['UKPRev', 'UKPSales','UKPNewReg','UKPSpnd']].sum(numeric_only = False).rename(columns = {'UKPRev': 'Revenue','UKPSales': 'Orders','UKPNewReg':'NewReg', 'UKPSpnd':'Spend'})

    grpukp = grp7.unstack(0).swaplevel(0, 1, 1).sort_index(1).reset_index()

    #display(grpukp)

    grp8 = df1.groupby(['FGCLDate','IE'])[['IEPRev', 'IEPSales','IEPNewReg','IEPSpnd']].sum(numeric_only = False).rename(columns = {'IEPRev': 'Revenue','IEPSales': 'Orders','IEPNewReg':'NewReg', 'IEPSpnd':'Spend'})

    grpiep = grp8.unstack(0).swaplevel(0, 1, 1).sort_index(1).reset_index()

    #display(grpiep)

    grp9 = df1.groupby(['FGCLDate','FR'])[['FRPRev', 'FRPSales','FRPNewReg','FRPSpnd']].sum(numeric_only = False).rename(columns = {'FRPRev': 'Revenue','FRPSales': 'Orders','FRPNewReg':'NewReg', 'FRPSpnd':'Spend'})

    grpfrp = grp9.unstack(0).swaplevel(0, 1, 1).sort_index(1).reset_index()

    #display(grpfrp)

    cursor1 = connect.cursor()

    cursor1.execute(
                    '''
                       SELECT 
                             * 
                       FROM 
                            fgc_prediction_values 
                       WHERE CAST(MonthYear AS DATE) = DATEFROMPARTS(YEAR(GETDATE()),MONTH(GETDATE()),1);
                    
                    
                    '''
                  )

    df3 = pd.DataFrame([{name:row[i] for i, name in enumerate([ col[0] for col in cursor1.description])} for row in cursor1.fetchall()])

    #display(df3)

    uk_target_spend = df3['UKTargetSpend'].squeeze().astype(str)

    ie_target_spend = df3['IETargetSpend'].squeeze().astype(str)

    fr_target_spend = df3['FRTargetSpend'].squeeze().astype(str)

    uk_target_sales = df3['UKTargetSales'].squeeze().astype(str)

    ie_target_sales = df3['IETargetSales'].squeeze().astype(str)

    fr_target_sales = df3['FRTargetSales'].squeeze().astype(str)

    now = datetime.now()
    
    dt_string = now.strftime("%A %d/%m/%Y")

    client = pygsheets.authorize(service_file= 'D:/Python_Deployments/FGC_FGCL_REPORT/Universal_Client_Secret.json')

    sh = client.open('FGC_FGCL_REPORT_2021_22')
    
    wks = sh.worksheet('title', 'Summary')
    
    #wks.rows = df.shape[0]
    
    wks.clear(start = 'B4', end = None)
    
    wks.update_value('A1', 'Updated on - ' + dt_string)
    
    wks.set_dataframe(grpuk, "B4", fit = False)

    wks.set_dataframe(grpie, "B8", fit = False)

    wks.set_dataframe(grpfr, "B12", fit = False)

    wks.set_dataframe(grpuk1, "M4", fit = False)

    wks.set_dataframe(grpie1, "M8", fit = False)

    wks.set_dataframe(grpfr1, "M12", fit = False)

    wks.set_dataframe(grpukp, "U4", fit = False)

    wks.set_dataframe(grpiep, "U8", fit = False)

    wks.set_dataframe(grpfrp, "U12", fit = False)

    wks.clear(start = "B8", end = "K9")

    wks.clear(start = "B12", end = "K13")

    wks.delete_rows(7,3)

    wks.delete_rows(8,3)

    wks.clear(start = "B4", end = "B4")

    wks.clear(start = "M4", end = "M4")

    wks.clear(start = "U4", end = "U4")

    wks.update_value('Z5', 'Target Spend')

    wks.update_value('AA5', 'Target Orders')

    wks.update_value('Z6', uk_target_spend)

    wks.update_value('Z7', ie_target_spend)

    wks.update_value('Z8', fr_target_spend)

    wks.update_value('AA6', uk_target_sales)

    wks.update_value('AA7', ie_target_sales)
    
    wks.update_value('AA8', fr_target_sales)
     
    cursor1.close()

if __name__ == '__main__':
    read_query()