from datetime import datetime
from IPython.display import display
from isoweek import Week
from numpy import int64
import pandas as pd
import pygsheets

import warnings
warnings.filterwarnings('ignore')

def read_google_sheet():

    client = pygsheets.authorize(service_file = 'D:/Python_Deployments/FGC_Automation_Window_Server/FGC_Daily_Sales_Cost_Report/client_secret.json')

    googlesheet = client.open('FGC-Daily Sales & Costs-2021-22')

    worksheet = googlesheet.worksheet('title','Sales by Product')

    df = worksheet.get_as_df(has_header = True, start = 'A2', include_tailing_empty = False, include_tailing_empty_rows = False, numerize=True)

    df = df.iloc[:, [0,2,3,4,5]]

    df['Year'] = pd.to_datetime(df['Date']).dt.year

    df['Date'] = pd.to_datetime(df['Date']).dt.week

    df["start_of_wk"] = df.apply(lambda x: Week(x['Year'], x['Date']).monday(), axis=1)

    df["end_of_wk"] = df.apply(lambda x: Week(x['Year'], x['Date']).sunday(), axis=1)

    df["start_of_wk"] = pd.to_datetime(df["start_of_wk"]).apply(lambda x: x.strftime('%d-%m-%Y'))

    df["end_of_wk"] = pd.to_datetime(df["end_of_wk"]).apply(lambda x: x.strftime('%d-%m-%Y'))

    df['WeekRange'] = df['start_of_wk'].astype(str) + ' >> ' + df['end_of_wk'].astype(str)

    #df['WeekRange'] = df['WeekRange'].str.replace("-","")

    df = df.replace({r'\£':''}, regex = True)

    df = df.replace({r'\,':''}, regex = True)

    df['Date'] = pd.to_numeric(df['Date'])

    #df['WeekRange'] = pd.to_numeric(df['WeekRange'])

    df['Contact Lenses'] = pd.to_numeric(df['Contact Lenses'])

    df['Glasses'] = pd.to_numeric(df['Glasses'])

    df['Sunglasses'] = pd.to_numeric(df['Sunglasses'])

    df['Delivery'] = pd.to_numeric(df['Delivery'])

    #df_grp = df.groupby('Date')[['Contact Lenses','Glasses','Sunglasses','Delivery']].sum().reset_index()

    df_grp = df.groupby(['Date','WeekRange'])[['Contact Lenses','Glasses','Sunglasses','Delivery']].sum().reset_index()

    ##############################################################################################################################################################################

    
    client_1 = pygsheets.authorize(service_file = 'D:/Python_Deployments/FGC_Automation_Window_Server/FGC_Daily_Sales_Cost_Report/client_secret.json')

    googlesheet_1 = client_1.open('FGC-Daily Sales & Costs-2021-22')

    worksheet_1 = googlesheet_1.worksheet('title','Cost of Sales')

    df_1 = worksheet_1.get_as_df(has_header = True, start = 'A2', include_tailing_empty = False, include_tailing_empty_rows = False, numerize=True)

    df_1 = df_1.iloc[:, 0:7]

    df_1['Date'] = pd.to_datetime(df_1['Date']).dt.week

    df_1 = df_1.replace({r'\£':''}, regex = True)

    df_1 = df_1.replace({r'\,':''}, regex = True)

    df_1['Date'] = pd.to_numeric(df_1['Date'])

    df_1['CLs & solution'] = pd.to_numeric(df_1['CLs & solution'])

    df_1['Sunglasses'] = pd.to_numeric(df_1['Sunglasses'])

    df_1['Glasses'] = pd.to_numeric(df_1['Glasses'])

    df_1['Packaging'] = pd.to_numeric(df_1['Packaging'])

    df_1['Deliveries'] = pd.to_numeric(df_1['Deliveries'])

    df_1['GlazingCost'] = pd.to_numeric(df_1['GlazingCost'])

    df_grp_1 = df_1.groupby('Date')[['CLs & solution','Sunglasses','Glasses','Packaging', 'Deliveries','GlazingCost']].sum().reset_index()

    ##########################################################################################################################################################################

    client_2 = pygsheets.authorize(service_file = 'D:/Python_Deployments/FGC_Automation_Window_Server/FGC_Daily_Sales_Cost_Report/client_secret.json')

    googlesheet_2 = client_2.open('FGC-Daily Sales & Costs-2021-22')

    worksheet_2 = googlesheet_2.worksheet('title','Cost Acquisition')

    df_2 = worksheet_2.get_as_df(has_header = True, start = 'A3', include_tailing_empty = False, include_tailing_empty_rows = False, numerize=True)

    df_2 = df_2.iloc[:,[0,5, 9, 13, 6, 10, 14]]

    df_2['Date'] = pd.to_datetime(df_2['Date']).dt.week

    df_2 = df_2.replace({r'\£':''}, regex = True)

    df_2 = df_2.replace({r'\,':''}, regex = True)

    df_2.iloc[:,1] = pd.to_numeric(df_2.iloc[:,1])

    df_2.iloc[:,2] = pd.to_numeric(df_2.iloc[:,2])

    df_2.iloc[:,3] = pd.to_numeric(df_2.iloc[:,3])

    df_2.iloc[:,4] = pd.to_numeric(df_2.iloc[:,4])

    df_2.iloc[:,5] = pd.to_numeric(df_2.iloc[:,5])

    df_2.iloc[:,6] = pd.to_numeric(df_2.iloc[:,6])

    df_2.insert(7, 'Google Total', df_2.iloc[:,[1,2,3]].sum(axis = 1))

    df_2.insert(8, 'Bing Total', df_2.iloc[:,[4,5,6]].sum(axis = 1))

    df_2.insert(9, 'TOTAL_ACQUISITION', df_2['Google Total'].add(df_2['Bing Total']))

    df_2.drop([df_2.columns[1],df_2.columns[2], df_2.columns[3], df_2.columns[4], df_2.columns[5],df_2.columns[6]], axis = 1, inplace = True)

    df_grp_2 = df_2.groupby('Date')[['Google Total', 'Bing Total', 'TOTAL_ACQUISITION']].sum().reset_index()

    #display(df_grp_2)

    ##############################################################################################################################################################################

    client_3 = pygsheets.authorize(service_file = 'D:/Python_Deployments/FGC_Automation_Window_Server/FGC_Daily_Sales_Cost_Report/client_secret.json')

    googlesheet_3 = client_3.open('FGC-Daily Sales & Costs-2021-22')

    worksheet_3 = googlesheet_3.worksheet('title','Cost Labour')

    df_3 = worksheet_3.get_as_df(has_header = True, start = 'A2', include_tailing_empty = False, include_tailing_empty_rows = False, numerize=True)

    df_3 = df_3.iloc[:,[0, 5]]

    df_3['Date'] = pd.to_datetime(df_3['Date']).dt.week

    df_3 = df_3.replace({r'\£':''}, regex = True)

    df_3 = df_3.replace({r'\,':''}, regex = True)

    df_3.iloc[:,1] = pd.to_numeric(df_3.iloc[:,1])

    df_3.rename(columns = {'Total':'Total Payroll'}, inplace = True)

    df_grp_3 = df_3.groupby('Date')[['Total Payroll']].sum().reset_index()

    ##############################################################################################################################################################################

    df_merge_1 = df_grp.merge(df_grp_1, on = 'Date', how = 'inner')

    df_merge_2 = df_merge_1.merge(df_grp_2, on = 'Date', how = 'inner')

    df_merge_3 = df_merge_2.merge(df_grp_3, on = 'Date', how = 'inner')

    #display(df_merge_3)

    ##############################################################################################################################################################################

    df_merge_4 = df_merge_3.copy()

    df_merge = df_merge_4.iloc[:,[0,1,2,3,4,6,7,8,9,11]]

    df_merge.insert(5, 'Total_SALES', df_merge.iloc[:,[2,3,4]].sum(axis = 1))

    df_merge.insert(11,'Total_COGS',  df_merge.iloc[:,[6,7,8,9,10]].sum(axis = 1))

    df_merge.insert(12, 'GP (exc shipping)', df_merge['Total_SALES'].sub(df_merge['Total_COGS']))

    df_merge.insert(13, 'Percentage of GP(exc shipping)/Sales', (df_merge['GP (exc shipping)'].div(df_merge['Total_SALES'])).mul(100).round(2))

    df_merge.insert(14, 'ShippingIncome', df_merge_3['Delivery'])

    df_merge.insert(15, 'Shipping Expenses', df_merge_3['Deliveries'])

    df_merge.insert(16, 'Total Shipping', df_merge_3['Delivery'].sub(df_merge_3['Deliveries']))

    df_merge.insert(17, 'GP (inc shipping', df_merge['GP (exc shipping)'].add(df_merge['Total Shipping']))

    df_merge.insert(18, 'Percentage of GP inc Shipping/Sales', (df_merge['GP (inc shipping'].div(df_merge['Total_SALES'])).mul(100).round(2))

    df_merge.insert(19, 'Google', df_merge_3['Google Total'])

    df_merge.insert(20, 'Bing', df_merge_3['Bing Total'])

    df_merge.insert(21, 'Total Acquisition', df_merge['Google'].add(df_merge['Bing']))

    df_merge.insert(22, 'Payroll', df_merge_3['Total Payroll'])

    df_merge.insert(23, 'Summary GP Inc Shipping', df_merge['GP (inc shipping'])

    df_merge.insert(24, 'Summary Percentage of GP inc Shipping/Sales', df_merge['Percentage of GP inc Shipping/Sales'])

    df_merge.insert(25, 'Net Income', df_merge['GP (exc shipping)'] - (df_merge['Total Acquisition'] + df_merge['Payroll']))

    df_merge.insert(26, 'Percentage of Net Income to Total Sales', (df_merge['Net Income'].div(df_merge['Total_SALES'])).mul(100).round(2))

    df_merge.insert(27, 'Acquisition Performance (>11%)', (df_merge['Total Acquisition'].div(df_merge['Total_SALES'])).mul(100).round(2))

    df_merge.insert(28, 'Payroll Performance (>2.30%)', (df_merge['Payroll'].div(df_merge['Total_SALES'])).mul(100).round(2))

    df_merge = df_merge.sort_values(by = 'Date', ascending = False)

    df_merge.insert(2, 'SALES', ' ')

    df_merge.insert(7, 'COST OF GOODS SOLD', ' ')

    df_merge.insert(16, 'SHIPPING PROFIT', ' ')

    df_merge.insert(22, 'COST OF ACQUISITION', ' ')

    df_merge.insert(26, 'PAYROLL', ' ')

    df_merge.insert(28, ' ', ' ')

    df_merge.insert(33, 'PERFORMANCE', ' ')

    df_merge['Percentage of GP(exc shipping)/Sales'] = df_merge['Percentage of GP(exc shipping)/Sales'].map("{:,.2f}%".format)

    df_merge['Percentage of GP inc Shipping/Sales'] = df_merge['Percentage of GP inc Shipping/Sales'].map("{:,.2f}%".format)

    df_merge['Summary Percentage of GP inc Shipping/Sales'] = df_merge['Summary Percentage of GP inc Shipping/Sales'].map("{:,.2f}%".format)

    df_merge['Percentage of Net Income to Total Sales'] = df_merge['Percentage of Net Income to Total Sales'].map("{:,.2f}%".format)

    df_merge['Acquisition Performance (>11%)'] = df_merge['Acquisition Performance (>11%)'].map("{:,.2f}%".format)

    df_merge['Payroll Performance (>2.30%)'] = df_merge['Payroll Performance (>2.30%)'].map("{:,.2f}%".format)

    #display(df_merge)

    df_transpose = df_merge.transpose()

    df_transpose.rename(columns=df_transpose.iloc[0], inplace = True)

    df_transpose.drop(df_transpose.index[0], inplace = True)

    df_transpose = df_transpose

    #display(df_transpose)

    #df_transpose.to_excel(r"C:\Users\Nimit\Desktop\profit_loss_Sample.xlsx")

    ######################################################################################################################################################################################
  
    client_4 = pygsheets.authorize(service_file = 'D:/Python_Deployments/FGC_Automation_Window_Server/FGC_Daily_Sales_Cost_Report/client_secret.json')

    googlesheet_4 = client_4.open('FGC-Daily Sales & Costs-2021-22')

    worksheet_4 = googlesheet_4.worksheet('title','Profit & Loss')

    worksheet_4.clear(start = 'B2', end = None)
    
    worksheet_4.set_dataframe(df_transpose, "B2", fit = True)



    