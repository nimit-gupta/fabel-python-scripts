#!/usr/bin/env python
# Copyright 2020 Google LLC


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

import pandas as pd
import sqlalchemy

from IPython.core.display import display


# [START get_keyword_stats]
def main(client, customer_id):
    ga_service = client.get_service("GoogleAdsService")

    query = """
               SELECT
                    segments.date,
                    metrics.clicks,
                    metrics.impressions,
                    metrics.ctr,
                    metrics.average_cpc,
                    metrics.conversions,
                    metrics.cost_micros,
                    metrics.cost_per_conversion,
                    metrics.conversions_from_interactions_rate, 
                    metrics.conversions_value        
              FROM 
                    customer
              WHERE 
                    segments.date DURING YESTERDAY
                    
            """

    search_request = client.get_type("SearchGoogleAdsStreamRequest")
    search_request.customer_id = customer_id
    search_request.query = query
    stream = ga_service.search_stream(search_request)

    empty_list_date = []
    empty_list_clicks = []
    empty_list_impressions = []
    empty_list_ctr = []
    empty_list_average_cpc = []
    empty_list_conversions = []
    empty_list_cost_micros = []
    empty_list_cost_per_conversion = []
    empty_list_conversions_from_interactions_rate = []
    empty_conversions_value = []
    
    for batch in stream:
        for row in batch.results:

            segments = row.segments 
            metrics = row.metrics

            empty_list_date.append(segments.date)
            empty_list_clicks.append(metrics.clicks)
            empty_list_impressions.append(metrics.impressions)
            empty_list_ctr.append(metrics.ctr)
            empty_list_average_cpc.append(metrics.average_cpc)
            empty_list_conversions.append(metrics.conversions)
            empty_list_cost_micros.append(metrics.cost_micros)
            empty_list_cost_per_conversion.append(metrics.cost_per_conversion)
            empty_list_conversions_from_interactions_rate.append(metrics.conversions_from_interactions_rate),
            empty_conversions_value.append(metrics.conversions_value)
    
    df = pd.DataFrame({
                       'Date'           : empty_list_date,
                       'Impressions'    : empty_list_impressions,
                       'Clicls'         : empty_list_clicks,
                       'CTR'            : empty_list_ctr,
                       'Average_Cpc'    : empty_list_average_cpc,
                       'Costs'          : empty_list_cost_micros,
                       'Conversions'    : empty_list_conversions,
                       'Cost_Per_Conversion' : empty_list_cost_per_conversion,
                       'Conversion_Rate' : empty_list_conversions_from_interactions_rate,
                       'Revenue' : empty_conversions_value
                       
                      })

   

    df['CTR'] = df['CTR'].mul(100).round(2)

    df['Average_Cpc'] = df['Average_Cpc'].div(1000000).round(2)

    df['Costs'] = df['Costs'].div(1000000).round(2)

    df['Cost_Per_Conversion'] = df['Cost_Per_Conversion'].div(1000000).round(2)

    df['Conversion_Rate'] = df['Conversion_Rate'].mul(100).round(2)

    df['Revenue'] = df['Revenue'].round(2)    
    
    display(df)
    
    engine = sqlalchemy.create_engine(f"mssql+pymssql://DevUser3:flgT!9585@217.174.248.77:3689/feelgood.reports")

    con = engine.connect() 

    table_name = 'fgc_fr_gads'

    df.to_sql(table_name, con, if_exists = 'append', method = 'multi', chunksize = 10000, index = False)

