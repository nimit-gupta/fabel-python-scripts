from IPython.display import display
import pandas as pd
import pygsheets

import warnings
warnings.filterwarnings('ignore')

def read_google_sheet():

    client = pygsheets.authorize(service_file = 'D:/Python_Deployments/FGC_Automation_Window_Server/FGC_Daily_Sales_Cost_Report/client_secret.json')

    googlesheet = client.open('FGC-Daily Sales & Costs-2021-22')

    worksheet = googlesheet.worksheet('title','Sales by Region')

    df = worksheet.get_as_df(has_header = True, start = 'A2', include_tailing_empty = False, include_tailing_empty_rows = False, numerize=True)

    df = df.replace({r'\£':''}, regex = True)

    df = df.replace({r'\,':''}, regex = True)

    df = df.iloc[:,[0,5]]

    df.iloc[:,0] = pd.to_datetime(df.iloc[:,0])

    df.iloc[:,1] = pd.to_numeric(df.iloc[:,1])

    df.rename(columns = {df.columns[1]:'Sales Ex VAT'}, inplace = True)

    #display(df)

    ########################################################################################################################################################################

    client_1 = pygsheets.authorize(service_file = 'D:/Python_Deployments/FGC_Automation_Window_Server/FGC_Daily_Sales_Cost_Report/client_secret.json')

    googlesheet_1 = client_1.open('FGC-Daily Sales & Costs-2021-22')

    worksheet_1 = googlesheet.worksheet('title','Cost of Sales')

    df_1 = worksheet_1.get_as_df(has_header = True, start = 'A2', include_tailing_empty = False, include_tailing_empty_rows = False, numerize=True)

    df_1 = df_1.replace({r'\£':''}, regex = True)

    df_1 = df_1.replace({r'\,':''}, regex = True)

    df_1 = df_1.iloc[:,[0,7]]

    df_1.iloc[:,0] = pd.to_datetime(df_1.iloc[:,0])

    df_1.iloc[:,1] = pd.to_numeric(df_1.iloc[:,1])

    df_1.rename(columns = {df_1.columns[1]:'Cost of Sales Ex VAT'}, inplace = True)

    #display(df_1)

    ########################################################################################################################################################################

    client_2 = pygsheets.authorize(service_file = 'D:/Python_Deployments/FGC_Automation_Window_Server/FGC_Daily_Sales_Cost_Report/client_secret.json')

    googlesheet_2 = client_2.open('FGC-Daily Sales & Costs-2021-22')

    worksheet_2 = googlesheet_2.worksheet('title','Cost Labour')

    df_2 = worksheet_2.get_as_df(has_header = True, start = 'A2', include_tailing_empty = False, include_tailing_empty_rows = False, numerize=True)

    df_2 = df_2.replace({r'\£':''}, regex = True)

    df_2 = df_2.replace({r'\,':''}, regex = True)

    df_2 = df_2.iloc[:,[0,5]]

    df_2.iloc[:,0] = pd.to_datetime(df_2.iloc[:,0])

    df_2.iloc[:,1] = pd.to_numeric(df_2.iloc[:,1])

    df_2.rename(columns = {df_2.columns[1]:'Labour Cost'}, inplace = True)

    #display(df_2)

    #########################################################################################################################################################################

    client_3 = pygsheets.authorize(service_file = 'D:/Python_Deployments/FGC_Automation_Window_Server/FGC_Daily_Sales_Cost_Report/client_secret.json')

    googlesheet_3 = client_3.open('FGC-Daily Sales & Costs-2021-22')

    worksheet_3 = googlesheet_3.worksheet('title','Cost Acquisition')

    df_3 = worksheet_3.get_as_df(has_header = True, start = 'A3', include_tailing_empty = False, include_tailing_empty_rows = False, numerize=True)

    df_3 = df_3.replace({r'\£':''}, regex = True)

    df_3 = df_3.replace({r'\,':''}, regex = True)

    df_3 = df_3.iloc[:,[0,4]]

    df_3.iloc[:,0] = pd.to_datetime(df_3.iloc[:,0])

    df_3.iloc[:,1] = pd.to_numeric(df_3.iloc[:,1])

    df_3.rename(columns = {df_3.columns[1]:'Acquistion Cost'}, inplace = True)

    #display(df_3)

    ##########################################################################################################################################################################

    client_4 = pygsheets.authorize(service_file = 'D:/Python_Deployments/FGC_Automation_Window_Server/FGC_Daily_Sales_Cost_Report/client_secret.json')

    googlesheet_4 = client_4.open('FGC-Daily Sales & Costs-2021-22')

    worksheet_4 = googlesheet_4.worksheet('title','Cost Refund')

    df_4 = worksheet_4.get_as_df(has_header = True, start = 'A2', include_tailing_empty = False, include_tailing_empty_rows = False, numerize=True)

    df_4 = df_4.replace({r'\£':''}, regex = True)

    df_4 = df_4.replace({r'\,':''}, regex = True)

    df_4 = df_4.iloc[:,[0,5]]

    df_4.iloc[:,0] = pd.to_datetime(df_4.iloc[:,0])

    df_4.iloc[:,1] = pd.to_numeric(df_4.iloc[:,1])

    df_4.rename(columns = {df_4.columns[0]:'Date', df_4.columns[1]:'Refund Cost'}, inplace = True)

    #display(df_4)
    ##########################################################################################################################################################################
    
    df_merge_1 = df.merge(df_1, on = 'Date', how = 'inner')

    df_merge_2 = df_merge_1.merge(df_2, on = 'Date', how = 'inner')

    df_merge_3 = df_merge_2.merge(df_3, on = 'Date', how = 'inner')

    df_merge_4 = df_merge_3.merge(df_4, on = 'Date', how = 'inner')

    df_merge = df_merge_4
    
    #display(df_merge)

    df_merge.insert(3, 'GP', df_merge['Sales Ex VAT'].sub(df_merge['Cost of Sales Ex VAT']))

    df_merge.insert(7, 'Total Variable Cost', df_merge['Labour Cost'].add(df_merge['Acquistion Cost']).add(df_merge['Refund Cost']))

    df_merge.insert(8, 'Net Income', df_merge['GP'].sub(df_merge['Total Variable Cost']))

    df_merge.insert(9, 'GP%', (df_merge['GP'].div(df_merge['Sales Ex VAT'])).mul(100).round(2))

    df_merge.insert(10, 'Aquistion Performance Marker (> 11%)', (df_merge['Acquistion Cost'].div(df_merge['Sales Ex VAT'])).mul(100).round(2))

    df_merge.insert(11, 'Labour Performance Marker (>2.30%)', (df_merge['Labour Cost'].div(df_merge['Sales Ex VAT'])).mul(100).round(2))

    df_merge['GP%'] = df_merge['GP%'].map("{:,.2f}%".format)

    df_merge['Aquistion Performance Marker (> 11%)'] = df_merge['Aquistion Performance Marker (> 11%)'].map("{:,.2f}%".format)

    df_merge['Labour Performance Marker (>2.30%)'] = df_merge['Labour Performance Marker (>2.30%)'].map("{:,.2f}%".format)

    #display(df_merge)

    #############################################################################################################################################################################

    client_5 = pygsheets.authorize(service_file = 'D:/Python_Deployments/FGC_Automation_Window_Server/FGC_Daily_Sales_Cost_Report/client_secret.json')

    googlesheet_5 = client_5.open('FGC-Daily Sales & Costs-2021-22')

    worksheet_5 = googlesheet_5.worksheet('title','Dashboard')

    worksheet_5.clear(start = 'B2', end = None)
    
    worksheet_5.set_dataframe(df_merge, "B2", fit = True)



