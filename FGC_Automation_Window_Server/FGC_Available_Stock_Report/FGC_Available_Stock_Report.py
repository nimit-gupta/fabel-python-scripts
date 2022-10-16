


######################################################################################################################################################################

                                                                    #Available Stock Report#

######################################################################################################################################################################

import pandas as pd
import numpy as np
import pymssql as pym
import pygsheets as pyg
from datetime import datetime

import smtplib

def read_query():
    
    con = pym.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585',database = r'feelgood.stock')
    
    sql = '''
             select 
                    ProductType,
                    ProductCode, 
                    ProductName , 
                    MonthlySales_Web, 
                    MonthlySales_Alloc,  
                    AvailableBoxes ,
                    (	select  
                            isnull(sum(supit.boxes - isnull(supit.boxesreceived,0)) ,0) as  PipeLine  
                        from  fg_supplierorder supord
                            inner join fg_supplierorderitems supit on supord.orderid = supit.orderid and isnull(supit.boxesreceived,0) < supit.boxes
                            inner join fg_product pp on supit.skuid = pp.skuid and isnull(Discontinued, 0) = 0 
                        where pp.productcode = aa.productcode
                            and supord.createdon > getdate() - 180 
                            and isnull(supord.closed,0) = 0 
                            and isnull(supord.canceled,0) = 0  
                    ) as PipeLine, 

                    ShippingAreaCapacity, 
                    ShippingAreaBoxes, 
                    HoldingAreaBoxes,  
                    DL_Web, 
                    DL_Alloc 

                from 

                (	select 
                        ps.ProductType,
                        mr.ProductCode, 
                        mr.ProductName , 
                        sum(maxlevel) as MonthlySales_Web, 
                        sum(MEROnStock) as MonthlySales_Alloc,  
                        sum(tt.Boxes - (EngDB + FrDB) ) as AvailableBoxes , 

                        isnull(
                        (	select sum(isnull(psa.capacityboxes,0)) 
                            from FG_SkuPrescriptionAreaCodes  psa
                            where psa.ProductCode = mr.ProductCode 
                            and isnull(psa.shippingarea,0) = 1 

                        ),0) as ShippingAreaCapacity, 

                        isnull(
                        (	select sum(isnull(psa.boxes,0)) 
                            from FG_SkuPrescriptionAreaCodes  psa
                            where psa.ProductCode = mr.ProductCode 
                            and isnull(psa.shippingarea,0) = 1 

                        ),0) as ShippingAreaBoxes,

                        isnull(
                        (	select sum(isnull(psa.boxes,0)) 
                            from FG_SkuPrescriptionAreaCodes  psa
                            where psa.ProductCode = mr.ProductCode 
                            and isnull(psa.holdingarea,0) = 1 

                        ),0) as HoldingAreaBoxes , 

                        sum(desiredlevel) as DL_Web, 
                        sum(DlOnStock) as DL_Alloc   

                    from fg_product tt 
                    inner join fg_productMaster mr on tt.productCode = mr.ProductCode 
                    inner join fg_ordersreceived dd on tt.SKUid = dd.skuid 
                    inner join fg_productTypes ps on mr.ProductTypeid = ps.ProductTypeId 

                    where mr.ProductTypeId not in (4,8) and tt.enable = 1 and mr.enable = 1 

                    group by mr.ProductCode, mr.ProductName, ProductType
                ) as aa 
                
                --where 
                --		MonthlySales_Web <> 0 
                --	and	MonthlySales_Alloc <> 0
                --	and AvailableBoxes <> 0

                order by 1 
            '''
    
    df = pd.read_sql_query(sql, con)
    
    now = datetime.now()
    
    dt_string = now.strftime("%A %d/%m/%Y %H:%M:%S")
    
    client = pyg.authorize(service_file= 'D:/Python_Deployments/FGC_Automation_Window_Server/FGC_Available_Stock_Report/client_secret.json')

    sh = client.open('FGC_Available_Stock_Report_2021')

    wks = sh.worksheet('title', 'Available_Stock_Report')

    wks.rows = df.shape[0]
    
    wks.clear(start = 'A1', end = None)
    
    wks.update_value('A1', 'Updated on - ' + dt_string)
    
    wks.set_dataframe(df, "A2", fit = True)

    ######### Sending Email #############

    body = 'Subject: FGC_Available_Stock_Report Status!' + '\n\n' + 'Sprints on  ' + ' - ' + dt_string + '\n\n' + 'By Windows Task Scheduler'

    smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
        
    smtpObj.ehlo()

    smtpObj.starttls()

    smtpObj.login('nimit@fabelservices.net', "Gupta@854") 

    smtpObj.sendmail('nimit@fabelservices.net', 'nimit@fabelservices.net', body) 

    smtpObj.quit()

    pass
    
if __name__ == '__main__':
    read_query()
