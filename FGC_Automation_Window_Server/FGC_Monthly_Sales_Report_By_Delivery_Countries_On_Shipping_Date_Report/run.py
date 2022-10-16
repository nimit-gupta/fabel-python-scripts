#! /usr/bin/env python

import Monthly_Sales_Report_UK
import Monthly_Sales_Report_IE
import Monthly_Sales_Report_FR
import Monthly_Sales_Report_EU

def run_sales_report():

    Monthly_Sales_Report_UK.read_query()
    Monthly_Sales_Report_IE.read_query()
    Monthly_Sales_Report_FR.read_query()
    Monthly_Sales_Report_EU.read_query()

if __name__ == '__main__':
    run_sales_report()

