#!usr/bin/env python310
#coding:utf-8

from IPython.core.display import display
from datetime import datetime
import pygsheets

def read_query():

    now = datetime.now()

    dt_string = now.strftime("%A %d/%m/%Y")

    client = pygsheets.authorize(service_file= 'D:/Python_Deployments/FGC_FGCL_REPORT/Universal_Client_Secret.json')

    sh = client.open('FGC_FGCL_REPORT_2021_22')
    
    wks = sh.worksheet('title', 'Menu')

    wks.clear(start = 'L2', end = 'M4')

    wks.update_value('L2', 'Updated on - ' + dt_string)

if __name__ == '__main__':
    read_query()


