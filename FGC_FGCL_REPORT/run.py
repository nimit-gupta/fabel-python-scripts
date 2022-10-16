#!usr/bin/env python310
#coding:utf-8

import fgc_fr
import fgc_all_account_geo
import fgc_all_geo
import fgc_all_time_uk
import fgc_fr_topline
import fgc_ie
import fgc_ie_topline
import fgc_main_summary
import fgc_uk
import fgc_uk_topline
import fgc_summary
import fgc_menu_date_time

def main():

    fgc_fr.read_query()
    fgc_all_account_geo.read_query()
    fgc_all_geo.read_query()
    fgc_all_time_uk.read_query()
    fgc_fr_topline.read_query()
    fgc_ie.read_query()
    fgc_ie_topline.read_query()
    fgc_main_summary.read_query()
    fgc_uk.read_query()
    fgc_uk_topline.read_query()
    fgc_summary.read_query()
    fgc_menu_date_time.read_query()

if __name__ == '__main__':
    main()


