#! /usr/bin/env python

import Sales_Report_UK
import Sales_Report_IE
import Sales_Report_FR
import Sales_Report_EU

def run_sales_report():

    Sales_Report_UK.read_query()
    Sales_Report_IE.read_query()
    Sales_Report_FR.read_query()
    Sales_Report_EU.read_query()

if __name__ == '__main__':
    run_sales_report()

