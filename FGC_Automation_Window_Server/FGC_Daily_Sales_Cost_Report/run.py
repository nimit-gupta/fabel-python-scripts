import Royal_Mail_Break_Down
import Cost_Of_Delivery
import Cost_Of_Sales
import Sales_By_Region
import Sales_By_Product
import Cost_Acquisition
import Cost_Labour
import Cost_Refund
import Dashboard
import Profit_Loss

def run_reports_script():
    
    try:
       Royal_Mail_Break_Down.read_query()
    except:
       pass

    try:
       Cost_Of_Delivery.read_query()
    except:
       pass

    try:
       Cost_Of_Sales.read_query()
    except:
       pass

    try:
       Sales_By_Region.read_query()
    except:
       pass

    try:
       Sales_By_Product.read_query_3()
    except:
        pass

    try:
       Cost_Acquisition.read_query()
    except:
       pass

    try:
       Cost_Labour.read_query()
    except:
       pass

    try:
       Cost_Refund.read_query()
    except:
       pass

    try:
       Dashboard.read_google_sheet()
    except:
       pass

    try:
       Profit_Loss.read_google_sheet()
    except:
       pass

if __name__ == '__main__':
    run_reports_script()