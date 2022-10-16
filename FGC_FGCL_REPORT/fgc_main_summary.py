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

#pd.set_option("display.max_columns", 100)

def read_query():

    connect = pymssql.connect( host = r'217.174.248.77',
                               port = 3689,
                               user = r'DevUser3',
                               password = r'flgT!9585',
                               database = r'feelgood.reports')

    cursor0 = connect.cursor()

    cursor0.execute('''
                       SELECT
                            DATENAME(Month, fgc_all_gads.GDATE) + ' ' + DATENAME(Year, fgc_all_gads.GDATE) + '(A)' AS "Date",
                            ROUND(SUM(fgc_all_gads.UK_CONVERSIONS_GOOGLE),0) "SALES(G)",
                            SUM(fgc_all_gads.UK_COSTS_GOOGLE) "Cost(G)",
                            ROUND(SUM(fgc_all_mads.UK_CONVERSIONS_BING),0) "SALES(B)",
                            SUM(fgc_all_mads.UK_COSTS_BING) "Cost(B)",
                            '0' AS "Sales(F)",
                            '0' AS "Costs(F)",
                            ROUND(SUM(fgc_all_gads.UK_CONVERSIONS_GOOGLE) + SUM(fgc_all_mads.UK_CONVERSIONS_BING),0) AS "PPCSALES",
                            ROUND(SUM(fgc_all_gads.UK_COSTS_GOOGLE) + SUM(fgc_all_mads.UK_COSTS_BING), 0) AS "PPCCOSTS",
                            SUM(fgc_tot_new_reg.UK_NEW_TOT_CUST) "TotalNewReg",
                            SUM(fgc_tot_all_orders.UK_TOT_ALL_ORDERS) "TotalOrds",
                            ROUND(((SUM(fgc_all_gads.UK_CONVERSIONS_GOOGLE) + SUM(fgc_all_mads.UK_CONVERSIONS_BING))/SUM(fgc_tot_all_orders.UK_TOT_ALL_ORDERS)) *  SUM(CAST(fgc_tot_revenue.UK_TOT_REV AS FLOAT)),0) AS "PPCREVENUE",
                            ROUND(((SUM(fgc_all_gads.UK_COSTS_GOOGLE) + SUM(fgc_all_mads.UK_COSTS_BING)) / (((SUM(fgc_all_gads.UK_CONVERSIONS_GOOGLE) + SUM(fgc_all_mads.UK_CONVERSIONS_BING))/SUM(fgc_tot_all_orders.UK_TOT_ALL_ORDERS)) *  SUM(CAST(fgc_tot_revenue.UK_TOT_REV AS FLOAT)))) * 100, 2) AS "PERCENT",
                            ROUND(SUM(CAST(fgc_tot_revenue.UK_TOT_REV AS FLOAT)),2) "TotalRev"
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
                        WHERE 
                           CAST(fgc_all_gads.GDATE AS DATE) BETWEEN CAST(DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0) AS DATE) AND CAST(GETDATE() - 1 AS DATE)
                        GROUP BY 
                             DATENAME(Month, fgc_all_gads.GDATE) + ' ' + DATENAME(Year, fgc_all_gads.GDATE) 

                        
                             
                  ''')


    df0 = pd.DataFrame([{name: row[i] for i, name in enumerate([ col[0] for col in cursor0.description])} for row in cursor0.fetchall()])

    df0 = pd.DataFrame(df0.transpose().squeeze())

    cursor1 = connect.cursor()

    cursor1.execute('''
                       SELECT
                            DATENAME(Month, fgc_all_gads.GDATE) + ' ' + DATENAME(Year, fgc_all_gads.GDATE) + '(A)' AS "Date",
                            ROUND(SUM(fgc_all_gads.IE_CONVERSIONS_GOOGLE),0) "SALES(G)",
                            SUM(fgc_all_gads.IE_COSTS_GOOGLE) "Cost(G)",
                            ROUND(SUM(fgc_all_mads.IE_CONVERSIONS_BING),0) "SALES(B)",
                            SUM(fgc_all_mads.IE_COSTS_BING) "Cost(B)",
                            '0' AS "Sales(F)",
                            '0' AS "Costs(F)",
                            ROUND(SUM(fgc_all_gads.IE_CONVERSIONS_GOOGLE) + SUM(fgc_all_mads.IE_CONVERSIONS_BING),0) AS "PPCSALES",
                            ROUND(SUM(fgc_all_gads.IE_COSTS_GOOGLE) + SUM(fgc_all_mads.IE_COSTS_BING), 0) AS "PPCCOSTS",
                            SUM(fgc_tot_new_reg.IE_NEW_TOT_CUST) "TotalNewReg",
                            SUM(fgc_tot_all_orders.IE_TOT_ALL_ORDERS) "TotalOrds",
                            ROUND(((SUM(fgc_all_gads.IE_CONVERSIONS_GOOGLE) + SUM(fgc_all_mads.IE_CONVERSIONS_BING))/SUM(fgc_tot_all_orders.IE_TOT_ALL_ORDERS)) *  SUM(CAST(fgc_tot_revenue.IE_TOT_REV AS FLOAT)),0) AS "PPCREVENUE",
                            ROUND(((SUM(fgc_all_gads.IE_COSTS_GOOGLE) + SUM(fgc_all_mads.IE_COSTS_BING)) / (((SUM(fgc_all_gads.IE_CONVERSIONS_GOOGLE) + SUM(fgc_all_mads.IE_CONVERSIONS_BING))/SUM(fgc_tot_all_orders.IE_TOT_ALL_ORDERS)) *  SUM(CAST(fgc_tot_revenue.IE_TOT_REV AS FLOAT)))) * 100, 2) AS "PERCENT",
                            ROUND(SUM(CAST(fgc_tot_revenue.IE_TOT_REV AS FLOAT)),2) "TotalRev"
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
                        WHERE 
                           CAST(fgc_all_gads.GDATE AS DATE) BETWEEN CAST(DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0) AS DATE) AND CAST(GETDATE() - 1 AS DATE)
                        GROUP BY 
                             DATENAME(Month, fgc_all_gads.GDATE) + ' ' + DATENAME(Year, fgc_all_gads.GDATE) 
                                    
                  ''')

    df1 = pd.DataFrame([{name: row[i] for i, name in enumerate([ col[0] for col in cursor1.description])} for row in cursor1.fetchall()])

    df1 = pd.DataFrame(df1.transpose().squeeze())

    cursor2 = connect.cursor()

    cursor2.execute('''
                        SELECT
                            DATENAME(Month, fgc_all_gads.GDATE) + ' ' + DATENAME(Year, fgc_all_gads.GDATE) + '(A)' AS "Date",
                            ROUND(SUM(fgc_all_gads.FR_CONVERSIONS_GOOGLE),0) "SALES(G)",
                            SUM(fgc_all_gads.FR_COSTS_GOOGLE) "Cost(G)",
                            ROUND(SUM(fgc_all_mads.FR_CONVERSIONS_BING),0) "SALES(B)",
                            SUM(fgc_all_mads.FR_COSTS_BING) "Cost(B)",
                            '0' AS "Sales(F)",
                            '0' AS "Costs(F)",
                            ROUND(SUM(fgc_all_gads.FR_CONVERSIONS_GOOGLE) + SUM(fgc_all_mads.FR_CONVERSIONS_BING),0) AS "PPCSALES",
                            ROUND(SUM(fgc_all_gads.FR_COSTS_GOOGLE) + SUM(fgc_all_mads.FR_COSTS_BING), 0) AS "PPCCOSTS",
                            SUM(fgc_tot_new_reg.FR_NEW_TOT_CUST) "TotalNewReg",
                            SUM(fgc_tot_all_orders.FR_TOT_ALL_ORDERS) "TotalOrds",
                            ROUND(((SUM(fgc_all_gads.FR_CONVERSIONS_GOOGLE) + SUM(fgc_all_mads.FR_CONVERSIONS_BING))/SUM(fgc_tot_all_orders.FR_TOT_ALL_ORDERS)) *  SUM(CAST(fgc_tot_revenue.FR_TOT_REV AS FLOAT)),0) AS "PPCREVENUE",
                            ROUND(((SUM(fgc_all_gads.FR_COSTS_GOOGLE) + SUM(fgc_all_mads.FR_COSTS_BING)) / (((SUM(fgc_all_gads.FR_CONVERSIONS_GOOGLE) + SUM(fgc_all_mads.FR_CONVERSIONS_BING))/SUM(fgc_tot_all_orders.FR_TOT_ALL_ORDERS)) *  SUM(CAST(fgc_tot_revenue.FR_TOT_REV AS FLOAT)))) * 100, 2) AS "PERCENT",
                            ROUND(SUM(CAST(fgc_tot_revenue.FR_TOT_REV AS FLOAT)),2) "TotalRev"
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
                        WHERE 
                           CAST(fgc_all_gads.GDATE AS DATE) BETWEEN CAST(DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0) AS DATE) AND CAST(GETDATE() - 1 AS DATE)
                        GROUP BY 
                             DATENAME(Month, fgc_all_gads.GDATE) + ' ' + DATENAME(Year, fgc_all_gads.GDATE)  
                                    
                  ''')

    df2 = pd.DataFrame([{name: row[i] for i, name in enumerate([ col[0] for col in cursor2.description])} for row in cursor2.fetchall()])

    df2 = pd.DataFrame(df2.transpose().squeeze())
  
    cursor00 = connect.cursor()

    cursor00.execute('''
                        SELECT 
                           DATENAME(Month, GETDATE()) + ' ' + DATENAME(Year, GETDATE()) + '(P)' AS "Date",
                           ROUND(([SALES(G)]/NoDays) * MDays,0) AS "SALES(G)",
                           ROUND(([COST(G)]/NoDays) * MDays ,0) AS "Cost(G)",
                           ROUND(([SALES(B)]/NoDays) * MDays,0) AS "SALES(B)",
                           ROUND(([Cost(B)]/NoDays) * MDays,0) AS "Cost(B)",
                           [Sales(F)] AS "Sales(F)",
                           [Costs(F)] AS "Costs(F)",
                           ROUND(((([SALES(G)] + [SALES(B)])/NoDays) * MDays),0) AS "PPCSALES",
                           ROUND(((([COST(G)] + [Cost(B)])/NoDays) * MDays),0) AS "PPCCOSTS",
                           ROUND(((TotalNewReg/NoDays)* MDays),0) AS "TotalNewReg",
                           ROUND(((TotalOrds/NoDays)*MDays),0) AS "TotalOrds",
                           ROUND(((((([SALES(G)] + [SALES(B)])/TotalOrds) * TotalRev)/NoDays) * MDays), 0) AS "PPCREVENUE",
                           ROUND((((([COST(G)] + [Cost(B)])/((([SALES(G)] + [SALES(B)])/TotalOrds) * TotalRev))/NoDays) * MDays) *100,2) AS "PERCENT",
                           ROUND(((TotalRev/NoDays)*MDays),0) AS "TotalRev"       
                      FROM
                      (
                      
                      SELECT
                            DATENAME(Month,fgc_all_gads.GDATE) + ' ' + DATENAME(Year, fgc_all_gads.GDATE) AS "Date",
                            ROUND(SUM(fgc_all_gads.UK_CONVERSIONS_GOOGLE),0) "SALES(G)",
                            SUM(fgc_all_gads.UK_COSTS_GOOGLE) "Cost(G)",
                            ROUND(SUM(fgc_all_mads.UK_CONVERSIONS_BING),0) "SALES(B)",
                            SUM(fgc_all_mads.UK_COSTS_BING) "Cost(B)",
                            '0' AS "Sales(F)",
                            '0' AS "Costs(F)",
                            ROUND(SUM(fgc_all_gads.UK_CONVERSIONS_GOOGLE) + SUM(fgc_all_mads.UK_CONVERSIONS_BING),0) AS "PPCSALES",
                            ROUND(SUM(fgc_all_gads.UK_COSTS_GOOGLE) + SUM(fgc_all_mads.UK_COSTS_BING), 0) AS "PPCCOSTS",
                            SUM(fgc_tot_new_reg.UK_NEW_TOT_CUST) "TotalNewReg",
                            SUM(fgc_tot_all_orders.UK_TOT_ALL_ORDERS) "TotalOrds",
                            ROUND(((SUM(fgc_all_gads.UK_CONVERSIONS_GOOGLE) + SUM(fgc_all_mads.UK_CONVERSIONS_BING))/SUM(fgc_tot_all_orders.UK_TOT_ALL_ORDERS)) *  SUM(CAST(fgc_tot_revenue.UK_TOT_REV AS FLOAT)),0) AS "PPCREVENUE",
                            ROUND(((SUM(fgc_all_gads.UK_COSTS_GOOGLE) + SUM(fgc_all_mads.UK_COSTS_BING)) / (((SUM(fgc_all_gads.UK_CONVERSIONS_GOOGLE) + SUM(fgc_all_mads.UK_CONVERSIONS_BING))/SUM(fgc_tot_all_orders.UK_TOT_ALL_ORDERS)) *  SUM(CAST(fgc_tot_revenue.UK_TOT_REV AS FLOAT)))) * 100, 2) AS "PERCENT",
                            ROUND(SUM(CAST(fgc_tot_revenue.UK_TOT_REV AS FLOAT)),2) "TotalRev",
                            SUM(fgc_tot_all_orders.DayNo) "NoDays",
                            DAY(EOMONTH(GETDATE())) "MDays"       
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
                        WHERE 
                           CAST(fgc_all_gads.GDATE AS DATE) BETWEEN CAST(DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0) AS DATE) AND CAST(GETDATE() - 1 AS DATE)
                        GROUP BY 
                           DATENAME(Month,fgc_all_gads.GDATE) + ' ' + DATENAME(Year, fgc_all_gads.GDATE)
                        ) S 
                                    
                  ''')

    df00 = pd.DataFrame([{name: row[i] for i, name in enumerate([ col[0] for col in cursor00.description])} for row in cursor00.fetchall()])  

    df00 = df00.transpose().squeeze()

    dfct0 = pd.concat([df0,df00], axis = 1)

    dfct0.columns = dfct0.iloc[0]
 
    dfct0 = dfct0[1:]

    dfct0.rename({'Date':'Months',"SALES(G)": "Google Sales","Cost(G)":"Google Cost" \
                  ,"SALES(B)":"Bing Sales","Cost(B)":"Bing Cost" , "Sales(F)": "Sales Facebook" \
                  ,"Costs(F)" : "Costs Facebook","PPCSALES":"PPC Sales","PPCCOSTS" :"PPC Cost" \
                  ,"TotalNewReg" : "New Reg", "TotalOrds" : "Orders", "PPCREVENUE" : "PPC Revenue" \
                  ,"PERCENT" : "Percent", "TotalRev":"Revenue"}, inplace = True
                )

    dfct0 = dfct0.reset_index()

    #display(dfct0)

    cursor11 = connect.cursor()

    cursor11.execute('''
                         SELECT 
                           DATENAME(Month, GETDATE()) + ' ' + DATENAME(Year, GETDATE()) + '(P)' AS "Date",
                           ROUND(([SALES(G)]/NoDays) * MDays,0) AS "SALES(G)",
                           ROUND(([COST(G)]/NoDays) * MDays ,0) AS "Cost(G)",
                           ROUND(([SALES(B)]/NoDays) * MDays,0) AS "SALES(B)",
                           ROUND(([Cost(B)]/NoDays) * MDays,0) AS "Cost(B)",
                           [Sales(F)] AS "Sales(F)",
                           [Costs(F)] AS "Costs(F)",
                           ROUND(((([SALES(G)] + [SALES(B)])/NoDays) * MDays),0) AS "PPCSALES",
                           ROUND(((([COST(G)] + [Cost(B)])/NoDays) * MDays),0) AS "PPCCOSTS",
                           ROUND(((TotalNewReg/NoDays)* MDays),0) AS "TotalNewReg",
                           ROUND(((TotalOrds/NoDays)*MDays),0) AS "TotalOrds",
                           ROUND(((((([SALES(G)] + [SALES(B)])/TotalOrds) * TotalRev)/NoDays) * MDays), 0) AS "PPCREVENUE",
                           ROUND((((([COST(G)] + [Cost(B)])/((([SALES(G)] + [SALES(B)])/TotalOrds) * TotalRev))/NoDays) * MDays) *100,2) AS "PERCENT",
                           ROUND(((TotalRev/NoDays)*MDays),0) AS "TotalRev"       
                      FROM
                      (
                      
                      SELECT
                            DATENAME(Month,fgc_all_gads.GDATE) + ' ' + DATENAME(Year, fgc_all_gads.GDATE) AS "Date",
                            ROUND(SUM(fgc_all_gads.IE_CONVERSIONS_GOOGLE),0) "SALES(G)",
                            SUM(fgc_all_gads.IE_COSTS_GOOGLE) "Cost(G)",
                            ROUND(SUM(fgc_all_mads.IE_CONVERSIONS_BING),0) "SALES(B)",
                            SUM(fgc_all_mads.IE_COSTS_BING) "Cost(B)",
                            '0' AS "Sales(F)",
                            '0' AS "Costs(F)",
                            ROUND(SUM(fgc_all_gads.IE_CONVERSIONS_GOOGLE) + SUM(fgc_all_mads.IE_CONVERSIONS_BING),0) AS "PPCSALES",
                            ROUND(SUM(fgc_all_gads.IE_COSTS_GOOGLE) + SUM(fgc_all_mads.IE_COSTS_BING), 0) AS "PPCCOSTS",
                            SUM(fgc_tot_new_reg.IE_NEW_TOT_CUST) "TotalNewReg",
                            SUM(fgc_tot_all_orders.IE_TOT_ALL_ORDERS) "TotalOrds",
                            ROUND(((SUM(fgc_all_gads.IE_CONVERSIONS_GOOGLE) + SUM(fgc_all_mads.IE_CONVERSIONS_BING))/SUM(fgc_tot_all_orders.IE_TOT_ALL_ORDERS)) *  SUM(CAST(fgc_tot_revenue.IE_TOT_REV AS FLOAT)),0) AS "PPCREVENUE",
                            ROUND(((SUM(fgc_all_gads.IE_COSTS_GOOGLE) + SUM(fgc_all_mads.IE_COSTS_BING)) / (((SUM(fgc_all_gads.IE_CONVERSIONS_GOOGLE) + SUM(fgc_all_mads.IE_CONVERSIONS_BING))/SUM(fgc_tot_all_orders.IE_TOT_ALL_ORDERS)) *  SUM(CAST(fgc_tot_revenue.IE_TOT_REV AS FLOAT)))) * 100, 2) AS "PERCENT",
                            ROUND(SUM(CAST(fgc_tot_revenue.IE_TOT_REV AS FLOAT)),2) "TotalRev",
                            SUM(fgc_tot_all_orders.DayNo) "NoDays",
                            DAY(EOMONTH(GETDATE())) "MDays"       
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
                        WHERE 
                           CAST(fgc_all_gads.GDATE AS DATE) BETWEEN CAST(DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0) AS DATE) AND CAST(GETDATE() - 1 AS DATE)
                        GROUP BY 
                           DATENAME(Month,fgc_all_gads.GDATE) + ' ' + DATENAME(Year, fgc_all_gads.GDATE)
                        ) S 
                                    
                  ''')

    df11 = pd.DataFrame([{name: row[i] for i, name in enumerate([ col[0] for col in cursor11.description])} for row in cursor11.fetchall()])  

    df11 = pd.DataFrame(df11.transpose().squeeze())

    dfct1 = pd.concat([df1,df11], axis = 1)

    dfct1.columns = dfct1.iloc[0]
 
    dfct1 = dfct1[1:]

    dfct1.rename({'Date':'Months',"SALES(G)": "Google Sales","Cost(G)":"Google Cost" \
                  ,"SALES(B)":"Bing Sales","Cost(B)":"Bing Cost" , "Sales(F)": "Sales Facebook" \
                  ,"Costs(F)" : "Costs Facebook","PPCSALES":"PPC Sales","PPCCOSTS" :"PPC Cost" \
                  ,"TotalNewReg" : "New Reg", "TotalOrds" : "Orders", "PPCREVENUE" : "PPC Revenue" \
                  ,"PERCENT" : "Percent", "TotalRev":"Revenue"}, inplace = True
                )

    dfct1 = dfct1.reset_index()

    #display(dfct1)

    cursor22 = connect.cursor()

    cursor22.execute('''
                         SELECT 
                           DATENAME(Month, GETDATE()) + ' ' + DATENAME(Year, GETDATE()) + '(P)' AS "Date",
                           ROUND(([SALES(G)]/NoDays) * MDays,0) AS "SALES(G)",
                           ROUND(([COST(G)]/NoDays) * MDays ,0) AS "Cost(G)",
                           ROUND(([SALES(B)]/NoDays) * MDays,0) AS "SALES(B)",
                           ROUND(([Cost(B)]/NoDays) * MDays,0) AS "Cost(B)",
                           [Sales(F)] AS "Sales(F)",
                           [Costs(F)] AS "Costs(F)",
                           ROUND(((([SALES(G)] + [SALES(B)])/NoDays) * MDays),0) AS "PPCSALES",
                           ROUND(((([COST(G)] + [Cost(B)])/NoDays) * MDays),0) AS "PPCCOSTS",
                           ROUND(((TotalNewReg/NoDays)* MDays),0) AS "TotalNewReg",
                           ROUND(((TotalOrds/NoDays)*MDays),0) AS "TotalOrds",
                           ROUND(((((([SALES(G)] + [SALES(B)])/TotalOrds) * TotalRev)/NoDays) * MDays), 0) AS "PPCREVENUE",
                           ROUND((((([COST(G)] + [Cost(B)])/((([SALES(G)] + [SALES(B)])/TotalOrds) * TotalRev))/NoDays) * MDays) *100,2) AS "PERCENT",
                           ROUND(((TotalRev/NoDays)*MDays),0) AS "TotalRev"       
                      FROM
                      (
                      
                      SELECT
                            DATENAME(Month,fgc_all_gads.GDATE) + ' ' + DATENAME(Year, fgc_all_gads.GDATE) AS "Date",
                            ROUND(SUM(fgc_all_gads.IE_CONVERSIONS_GOOGLE),0) "SALES(G)",
                            SUM(fgc_all_gads.IE_COSTS_GOOGLE) "Cost(G)",
                            ROUND(SUM(fgc_all_mads.IE_CONVERSIONS_BING),0) "SALES(B)",
                            SUM(fgc_all_mads.IE_COSTS_BING) "Cost(B)",
                            '0' AS "Sales(F)",
                            '0' AS "Costs(F)",
                            ROUND(SUM(fgc_all_gads.IE_CONVERSIONS_GOOGLE) + SUM(fgc_all_mads.IE_CONVERSIONS_BING),0) AS "PPCSALES",
                            ROUND(SUM(fgc_all_gads.IE_COSTS_GOOGLE) + SUM(fgc_all_mads.IE_COSTS_BING), 0) AS "PPCCOSTS",
                            SUM(fgc_tot_new_reg.IE_NEW_TOT_CUST) "TotalNewReg",
                            SUM(fgc_tot_all_orders.IE_TOT_ALL_ORDERS) "TotalOrds",
                            ROUND(((SUM(fgc_all_gads.IE_CONVERSIONS_GOOGLE) + SUM(fgc_all_mads.IE_CONVERSIONS_BING))/SUM(fgc_tot_all_orders.IE_TOT_ALL_ORDERS)) *  SUM(CAST(fgc_tot_revenue.IE_TOT_REV AS FLOAT)),0) AS "PPCREVENUE",
                            ROUND(((SUM(fgc_all_gads.IE_COSTS_GOOGLE) + SUM(fgc_all_mads.IE_COSTS_BING)) / (((SUM(fgc_all_gads.IE_CONVERSIONS_GOOGLE) + SUM(fgc_all_mads.IE_CONVERSIONS_BING))/SUM(fgc_tot_all_orders.IE_TOT_ALL_ORDERS)) *  SUM(CAST(fgc_tot_revenue.IE_TOT_REV AS FLOAT)))) * 100, 2) AS "PERCENT",
                            ROUND(SUM(CAST(fgc_tot_revenue.IE_TOT_REV AS FLOAT)),2) "TotalRev",
                            SUM(fgc_tot_all_orders.DayNo) "NoDays",
                            DAY(EOMONTH(GETDATE())) "MDays"       
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
                        WHERE 
                           CAST(fgc_all_gads.GDATE AS DATE) BETWEEN CAST(DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0) AS DATE) AND CAST(GETDATE() - 1 AS DATE)
                        GROUP BY 
                           DATENAME(Month,fgc_all_gads.GDATE) + ' ' + DATENAME(Year, fgc_all_gads.GDATE)
                        ) S 
                                    
                  ''')

    df22 = pd.DataFrame([{name: row[i] for i, name in enumerate([ col[0] for col in cursor22.description])} for row in cursor22.fetchall()])  

    df22 = pd.DataFrame(df22.transpose().squeeze())

    dfct2 = pd.concat([df2,df22], axis = 1)

    dfct2.columns = dfct2.iloc[0]
 
    dfct2 = dfct2[1:]

    dfct2.rename({'Date':'Months',"SALES(G)": "Google Sales","Cost(G)":"Google Cost" \
                  ,"SALES(B)":"Bing Sales","Cost(B)":"Bing Cost" , "Sales(F)": "Sales Facebook" \
                  ,"Costs(F)" : "Costs Facebook","PPCSALES":"PPC Sales","PPCCOSTS" :"PPC Cost" \
                  ,"TotalNewReg" : "New Reg", "TotalOrds" : "Orders", "PPCREVENUE" : "PPC Revenue" \
                  ,"PERCENT" : "Percent", "TotalRev":"Revenue"}, inplace = True
                )

    dfct2 = dfct2.reset_index()

    cursor4 = connect.cursor()

    cursor4.execute('''
                       SELECT
                            DATENAME(Month, fgc_all_gads.GDATE) + ' ' + DATENAME(Year, fgc_all_gads.GDATE) + '(A)' AS "Date",
                            ROUND(SUM(fgc_all_gads.UK_CONVERSIONS_GOOGLE + fgc_all_gads.IE_CONVERSIONS_GOOGLE + fgc_all_gads.FR_CONVERSIONS_GOOGLE),0) "SALES(G)",
                            SUM(fgc_all_gads.UK_COSTS_GOOGLE + fgc_all_gads.IE_COSTS_GOOGLE + fgc_all_gads.FR_COSTS_GOOGLE) "Cost(G)",
                            ROUND(SUM(fgc_all_mads.UK_CONVERSIONS_BING + fgc_all_mads.IE_CONVERSIONS_BING + fgc_all_mads.FR_CONVERSIONS_BING),0) "SALES(B)",
                            SUM(fgc_all_mads.UK_COSTS_BING + fgc_all_mads.IE_COSTS_BING + fgc_all_mads.FR_COSTS_BING) "Cost(B)",
                            '0' AS "Sales(F)",
                            '0' AS "Costs(F)",
                            ROUND(SUM(fgc_all_gads.UK_CONVERSIONS_GOOGLE + fgc_all_gads.IE_CONVERSIONS_GOOGLE + fgc_all_gads.FR_CONVERSIONS_GOOGLE) + SUM(fgc_all_mads.UK_CONVERSIONS_BING + fgc_all_mads.IE_CONVERSIONS_BING + fgc_all_mads.FR_CONVERSIONS_BING),0) AS "PPCSALES",
                            ROUND(SUM(fgc_all_gads.UK_COSTS_GOOGLE + fgc_all_gads.IE_COSTS_GOOGLE + fgc_all_gads.FR_COSTS_GOOGLE) + SUM(fgc_all_mads.UK_COSTS_BING + fgc_all_mads.IE_COSTS_BING + fgc_all_mads.FR_COSTS_BING), 0) AS "PPCCOSTS",
                            SUM(fgc_tot_new_reg.UK_NEW_TOT_CUST + fgc_tot_new_reg.IE_NEW_TOT_CUST + fgc_tot_new_reg.FR_NEW_TOT_CUST) "TotalNewReg",
                            SUM(fgc_tot_all_orders.UK_TOT_ALL_ORDERS + fgc_tot_all_orders.IE_TOT_ALL_ORDERS + fgc_tot_all_orders.FR_TOT_ALL_ORDERS) "TotalOrds",
                            ROUND(((SUM(fgc_all_gads.UK_CONVERSIONS_GOOGLE + fgc_all_gads.IE_CONVERSIONS_GOOGLE + fgc_all_gads.FR_CONVERSIONS_GOOGLE) + SUM(fgc_all_mads.UK_CONVERSIONS_BING + fgc_all_mads.IE_CONVERSIONS_BING + fgc_all_mads.FR_CONVERSIONS_BING))/SUM(fgc_tot_all_orders.UK_TOT_ALL_ORDERS + fgc_tot_all_orders.IE_TOT_ALL_ORDERS + fgc_tot_all_orders.FR_TOT_ALL_ORDERS)) *  SUM(CAST(fgc_tot_revenue.UK_TOT_REV AS FLOAT) + CAST(fgc_tot_revenue.IE_TOT_REV AS FLOAT) + CAST(fgc_tot_revenue.FR_TOT_REV AS FLOAT)),0) AS "PPCREVENUE",
                            ROUND(((SUM(fgc_all_gads.UK_COSTS_GOOGLE + fgc_all_gads.IE_COSTS_GOOGLE + fgc_all_gads.FR_COSTS_GOOGLE) + SUM(fgc_all_mads.UK_COSTS_BING + fgc_all_mads.IE_COSTS_BING + fgc_all_mads.FR_COSTS_BING)) / (((SUM(fgc_all_gads.UK_CONVERSIONS_GOOGLE + fgc_all_gads.IE_CONVERSIONS_GOOGLE + fgc_all_gads.FR_CONVERSIONS_GOOGLE) + SUM(fgc_all_mads.UK_CONVERSIONS_BING + fgc_all_mads.IE_CONVERSIONS_BING + fgc_all_mads.FR_CONVERSIONS_BING))/SUM(fgc_tot_all_orders.UK_TOT_ALL_ORDERS + fgc_tot_all_orders.IE_TOT_ALL_ORDERS + fgc_tot_all_orders.FR_TOT_ALL_ORDERS)) *  SUM(CAST(fgc_tot_revenue.UK_TOT_REV AS FLOAT) + CAST(fgc_tot_revenue.IE_TOT_REV AS FLOAT) + CAST(fgc_tot_revenue.FR_TOT_REV AS FLOAT)))) * 100, 2) AS "PERCENT",
                            ROUND(SUM(CAST(fgc_tot_revenue.UK_TOT_REV AS FLOAT) + CAST(fgc_tot_revenue.IE_TOT_REV AS FLOAT) + CAST(fgc_tot_revenue.FR_TOT_REV AS FLOAT)),2) "TotalRev"
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
                        WHERE 
                           CAST(fgc_all_gads.GDATE AS DATE) BETWEEN CAST(DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0) AS DATE) AND CAST(GETDATE() - 1 AS DATE)
                        GROUP BY 
                             DATENAME(Month, fgc_all_gads.GDATE) + ' ' + DATENAME(Year, fgc_all_gads.GDATE) 

                        
                             
                  ''')


    df4 = pd.DataFrame([{name: row[i] for i, name in enumerate([ col[0] for col in cursor4.description])} for row in cursor4.fetchall()])

    df4 = pd.DataFrame(df4.transpose().squeeze())

    cursor44 = connect.cursor()

    cursor44.execute(''' SELECT 
                           DATENAME(Month, GETDATE()) + ' ' + DATENAME(Year, GETDATE()) + '(P)' AS "Date",
                           ROUND(([SALES(G)]/NoDays) * MDays,0) AS "SALES(G)",
                           ROUND(([COST(G)]/NoDays) * MDays ,0) AS "Cost(G)",
                           ROUND(([SALES(B)]/NoDays) * MDays,0) AS "SALES(B)",
                           ROUND(([Cost(B)]/NoDays) * MDays,0) AS "Cost(B)",
                           [Sales(F)] AS "Sales(F)",
                           [Costs(F)] AS "Costs(F)",
                           ROUND(((([SALES(G)] + [SALES(B)])/NoDays) * MDays),0) AS "PPCSALES",
                           ROUND(((([COST(G)] + [Cost(B)])/NoDays) * MDays),0) AS "PPCCOSTS",
                           ROUND(((TotalNewReg/NoDays)* MDays),0) AS "TotalNewReg",
                           ROUND(((TotalOrds/NoDays)*MDays),0) AS "TotalOrds",
                           ROUND(((((([SALES(G)] + [SALES(B)])/TotalOrds) * TotalRev)/NoDays) * MDays), 0) AS "PPCREVENUE",
                           ROUND((((([COST(G)] + [Cost(B)])/((([SALES(G)] + [SALES(B)])/TotalOrds) * TotalRev))/NoDays) * MDays) *100,2) AS "PERCENT",
                           ROUND(((TotalRev/NoDays)*MDays),0) AS "TotalRev"       
                      FROM
                      (
                      
                      SELECT
                            DATENAME(Month, fgc_all_gads.GDATE) + ' ' + DATENAME(Year, fgc_all_gads.GDATE) "Date",
                            ROUND(SUM(fgc_all_gads.UK_CONVERSIONS_GOOGLE + fgc_all_gads.IE_CONVERSIONS_GOOGLE + fgc_all_gads.FR_CONVERSIONS_GOOGLE),0) "SALES(G)",
                            SUM(fgc_all_gads.UK_COSTS_GOOGLE + fgc_all_gads.IE_COSTS_GOOGLE + fgc_all_gads.FR_COSTS_GOOGLE) "Cost(G)",
                            ROUND(SUM(fgc_all_mads.UK_CONVERSIONS_BING + fgc_all_mads.IE_CONVERSIONS_BING + fgc_all_mads.FR_CONVERSIONS_BING),0) "SALES(B)",
                            SUM(fgc_all_mads.UK_COSTS_BING + fgc_all_mads.IE_COSTS_BING + fgc_all_mads.FR_COSTS_BING) "Cost(B)",
                            '0' AS "Sales(F)",
                            '0' AS "Costs(F)",
                            ROUND(SUM(fgc_all_gads.UK_CONVERSIONS_GOOGLE + fgc_all_gads.IE_CONVERSIONS_GOOGLE + fgc_all_gads.FR_CONVERSIONS_GOOGLE) + SUM(fgc_all_mads.UK_CONVERSIONS_BING + fgc_all_mads.IE_CONVERSIONS_BING + fgc_all_mads.FR_CONVERSIONS_BING),0) AS "PPCSALES",
                            ROUND(SUM(fgc_all_gads.UK_COSTS_GOOGLE + fgc_all_gads.IE_COSTS_GOOGLE + fgc_all_gads.FR_COSTS_GOOGLE) + SUM(fgc_all_mads.UK_COSTS_BING + fgc_all_mads.IE_COSTS_BING + fgc_all_mads.FR_COSTS_BING), 0) AS "PPCCOSTS",
                            SUM(fgc_tot_new_reg.UK_NEW_TOT_CUST + fgc_tot_new_reg.IE_NEW_TOT_CUST + fgc_tot_new_reg.FR_NEW_TOT_CUST) "TotalNewReg",
                            SUM(fgc_tot_all_orders.UK_TOT_ALL_ORDERS + fgc_tot_all_orders.IE_TOT_ALL_ORDERS + fgc_tot_all_orders.FR_TOT_ALL_ORDERS) "TotalOrds",
                            ROUND(((SUM(fgc_all_gads.UK_CONVERSIONS_GOOGLE + fgc_all_gads.IE_CONVERSIONS_GOOGLE + fgc_all_gads.FR_CONVERSIONS_GOOGLE) + SUM(fgc_all_mads.UK_CONVERSIONS_BING + fgc_all_mads.IE_CONVERSIONS_BING + fgc_all_mads.FR_CONVERSIONS_BING))/SUM(fgc_tot_all_orders.UK_TOT_ALL_ORDERS + fgc_tot_all_orders.IE_TOT_ALL_ORDERS + fgc_tot_all_orders.FR_TOT_ALL_ORDERS)) *  SUM(CAST(fgc_tot_revenue.UK_TOT_REV AS FLOAT) + CAST(fgc_tot_revenue.IE_TOT_REV AS FLOAT) + CAST(fgc_tot_revenue.FR_TOT_REV AS FLOAT)),0) AS "PPCREVENUE",
                            ROUND(((SUM(fgc_all_gads.UK_COSTS_GOOGLE + fgc_all_gads.IE_COSTS_GOOGLE + fgc_all_gads.FR_COSTS_GOOGLE) + SUM(fgc_all_mads.UK_COSTS_BING + fgc_all_mads.IE_COSTS_BING + fgc_all_mads.FR_COSTS_BING)) / (((SUM(fgc_all_gads.UK_CONVERSIONS_GOOGLE + fgc_all_gads.IE_CONVERSIONS_GOOGLE + fgc_all_gads.FR_CONVERSIONS_GOOGLE) + SUM(fgc_all_mads.UK_CONVERSIONS_BING + fgc_all_mads.IE_CONVERSIONS_BING + fgc_all_mads.FR_CONVERSIONS_BING))/SUM(fgc_tot_all_orders.UK_TOT_ALL_ORDERS + fgc_tot_all_orders.IE_TOT_ALL_ORDERS + fgc_tot_all_orders.FR_TOT_ALL_ORDERS)) *  SUM(CAST(fgc_tot_revenue.UK_TOT_REV AS FLOAT) + CAST(fgc_tot_revenue.IE_TOT_REV AS FLOAT) + CAST(fgc_tot_revenue.FR_TOT_REV AS FLOAT)))) * 100, 2) AS "PERCENT",
                            ROUND(SUM(CAST(fgc_tot_revenue.UK_TOT_REV AS FLOAT) + CAST(fgc_tot_revenue.IE_TOT_REV AS FLOAT) + CAST(fgc_tot_revenue.FR_TOT_REV AS FLOAT)),2) "TotalRev",
                            SUM(fgc_tot_all_orders.DayNo) "NoDays",
                            DAY(EOMONTH(GETDATE())) "MDays"       
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
                        WHERE 
                           CAST(fgc_all_gads.GDATE AS DATE) BETWEEN CAST(DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0) AS DATE) AND CAST(GETDATE() - 1 AS DATE)
                        GROUP BY 
                           DATENAME(Month,fgc_all_gads.GDATE) + ' ' + DATENAME(Year, fgc_all_gads.GDATE)
                        ) S 
                                    
                        
                                    
                  ''')

    df44 = pd.DataFrame([{name: row[i] for i, name in enumerate([ col[0] for col in cursor44.description])} for row in cursor44.fetchall()])  

    df44 = pd.DataFrame(df44.transpose().squeeze())

    dfct4 = pd.concat([df4,df44], axis = 1)

    dfct4.columns = dfct4.iloc[0]
 
    dfct4 = dfct4[1:]

    dfct4.rename({'Date':'Months',"SALES(G)": "Google Sales","Cost(G)":"Google Cost" \
                  ,"SALES(B)":"Bing Sales","Cost(B)":"Bing Cost" , "Sales(F)": "Sales Facebook" \
                  ,"Costs(F)" : "Costs Facebook","PPCSALES":"PPC Sales","PPCCOSTS" :"PPC Cost" \
                  ,"TotalNewReg" : "New Reg", "TotalOrds" : "Orders", "PPCREVENUE" : "PPC Revenue" \
                  ,"PERCENT" : "Percent", "TotalRev":"Revenue"}, inplace = True
                )

    dfct4 = dfct4.reset_index()



    #**************************************************************************************************************************************

    now = datetime.now()
    
    dt_string = now.strftime("%A %d/%m/%Y")
    
    client = pygsheets.authorize(service_file= 'D:/Python_Deployments/FGC_FGCL_REPORT/Universal_Client_Secret.json')

    sh = client.open('FGC_FGCL_REPORT_2021_22')
    
    wks = sh.worksheet('title', 'Main')
    
    #wks.rows = df.shape[0]
    
    wks.clear(start = 'A1', end = None)
    
    wks.update_value('A1', 'Updated on - ' + dt_string)
    
    wks.set_dataframe(dfct0, "B4")

    wks.set_dataframe(dfct1, "F4")

    wks.set_dataframe(dfct2, "J4")

    wks.set_dataframe(dfct4, "N4")

    wks.update_value("B3", "UK")

    wks.update_value("F3", "IE")

    wks.update_value("J3", "FR")

    wks.update_value("N3", "Top Line")

    

    #display(dfct0)

    #dfct0.to_excel(r'C:\Users\Nimit\Desktop\xx.xlsx')


if __name__ == '__main__':
    read_query()