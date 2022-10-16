#!/usr/bin/env python310
#coding:utf-8
'''
@author - Nimit Gupta

'''

from IPython.core.display import display
import fgc_all_mobile_orders
import fgc_all_non_mobile_orders
import fgc_total_all_orders
import fgc_total_new_orders
import fgc_total_new_registration
import fgc_total_revenue
import pandas as pd
import sqlalchemy
import pymssql 

def import_script():

    fgc_all_mobile_orders.read_query()

    fgc_all_non_mobile_orders.read_query()

    fgc_total_all_orders.read_query()

    fgc_total_new_orders.read_query()

    fgc_total_new_registration.read_query()
    
    fgc_total_revenue.read_query()

if __name__ == '__main__':
    import_script()



