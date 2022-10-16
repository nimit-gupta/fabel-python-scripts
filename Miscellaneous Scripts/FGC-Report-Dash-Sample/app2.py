#!/usr/bin/env python

import pymssql 
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc

import xlsxwriter

from dash_extensions import Download
from dash_extensions.snippets import send_bytes

import warnings
warnings.filterwarnings(action = 'ignore', category = DeprecationWarning)

import plotly.graph_objs as go
import base64
import config

app = dash.Dash(__name__, requests_pathname_prefix= '/app2/', external_stylesheets = [dbc.themes.BOOTSTRAP], title='FeelGoodContacts',server=True)

row = html.Div([
                   dbc.Row([
                             dbc.Col([
                                       html.H6('Year',style = {'font-weight':'bold','textAlign':'center','text-indent':'80%'}),
                                       dcc.Dropdown(
                                                    id = 'year',
                                                    options = [{'label': y, 'value': y} for y in ['2020','2021']],
                                                    style = {'width':'50%', 'margin-left':'50%'}
                                                    )
                                     ]),
                             dbc.Col([
                                       html.H6('Month',style = {'font-weight':'bold','textAlign':'center','text-indent':'-80%'}),
                                       dcc.Dropdown(
                                                    id = 'month',
                                                    options = [{'label' : x, 'value' : x} for x in [ '01','02','03',\
                                                                                                     '04','05','06',\
                                                                                                     '07','08','09',\
                                                                                                     '10','11','12']],
                                                    style = {'width':'50%'}
                                                   )
                                      ])
                              ]),
                    html.Br(),
                    dbc.Row([
                             dbc.Col([
                                      dcc.Loading(html.Button("Download", 
                                                              id = 'btn1', 
                                                              n_clicks = 0
                                                             )),
                                       Download(id="download")
                                     ], style = {'margin-left':'42%', 'display': 'inline-block', 'border-radius': '12px'}),
                             dbc.Col([
                                       dcc.Loading(html.A( 
                                                           html.Button("Refresh"), 
                                                           href="/",
                                                         )
                                                  )
                                     ], style = {'margin-left':'-40%', 'display': 'inline-block','border-radius': '12px'})
                            ])
            ])

image_filename = 'static/fgc-logo-1.png'

encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div([

                        html.Div([
                                        html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))
                                        ], style = {'margin-top':'3%','margin-left':'2%'}),
                   
                        html.Div([
                                    dbc.Container(children=[row])
                                    ], style = {'margin-top':'8%'})
                  
                     ])

@app.callback(Output('download','data'),[Input('btn1','n_clicks'),
                                         Input('year','value'), 
                                         Input('month','value')], 
                                         prevent_initial_call = True)

def download_xlsx_1(n_clicks, year, month):

    if n_clicks is not None and n_clicks > 0:

        con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

        #con = pymssql.connect(config.CONN_STR)

        sql = '''WITH CS_CTEUK AS 
                    (SELECT DISTINCT rr.OrderId,
                            isnull(EyeglassesParentOrderid, 0 ) as EyeglassesParentOrderid,
                            CONVERT(date,rr.CreatedOn,103) AS OrderDate, 
                            CONVERT(date,ry.CreatedOn,103) AS RefundDate,   

                            isnull(ry.Amount,0) as Refunded,  
                            CASE 
                                WHEN (ISNULL(rr.CreditCardId,0) = 18) then 'Marketing' 
                                WHEN (ISNULL(rr.CreditCardId,0) = 17) then 'SagePay'
                                WHEN (ISNULL(rr.CreditCardId,0) = 2) then 'PayPal'  
                                WHEN (ISNULL(rr.CreditCardId,0) = 21) then 'StoreCredit'   
                            end Payment_Method,  
                            iif(rr.currencyid = 1 , 'UK','IE') as Website, 
                            RefundReason, 
                            Status as OrderStatus

                        FROM [feelgood.live]..FG_Order rr  
                            INNER JOIN [feelgood.live]..FG_OrderchargesHistory ry on rr.orderid = ry.orderid and chargerefund = 0  
                            INNER JOIN [feelgood.live]..FG_RefundReason nn on ry.RefundReasonId = nn.RefundReasonId
                            INNER JOIN [feelgood.live]..FG_OrderStatus ss on rr.OrderStatusId = ss.OrderStatusId


                        WHERE
                            --month(RY.CreatedOn) = @month AND year(RY.createdon) = @year
                            CONVERT(VARCHAR(6),RY.CreatedOn , 112) = '%(year)s%(month)s'
                            --and rr.OrderStatusId not in (1, 44) 
                    )  

                    ,CS_CTEFR AS 
                    (SELECT DISTINCT rr.OrderId,
                            CONVERT(date,rr.CreatedOn,103) AS OrderDate,   
                            CONVERT(date,ry.CreatedOn,103) AS RefundDate,   
                            isnull(ry.Amount,0) as Refunded,  
                            CASE 
                                WHEN (ISNULL(rr.CreditCardId,0) = 18) then 'Marketing' 
                                WHEN (ISNULL(rr.CreditCardId,0) = 17) then 'SagePay'
                                WHEN (ISNULL(rr.CreditCardId,0) = 2) then 'PayPal'  
                            end Payment_Method,  
                            iif(rr.currencyid = 2 , 'FR','UK') as Website, 
                            RefundReason, 
                            Status as OrderStatus

                        FROM [feelgood.french]..FG_Order rr 
                            INNER JOIN [feelgood.french]..FG_OrderchargesHistory ry on rr.orderid = ry.orderid and chargerefund = 0  
                            INNER JOIN [feelgood.french]..FG_RefundReason nn on ry.RefundReasonId = nn.RefundReasonId
                            INNER JOIN [feelgood.french]..FG_OrderStatus ss on rr.OrderStatusId = ss.OrderStatusId and ss.CultureId = 1 

                        WHERE 
                            --month(RY.CreatedOn) = @month AND year(RY.createdon) = @year
                            CONVERT(VARCHAR(6),RY.CreatedOn , 112) = '%(year)s%(month)s'
                            --and rr.OrderStatusId not in (1, 44)
                    )  

                    SELECT DISTINCT
                        OrderId, EyeglassesParentOrderid,  OrderDate, RefundDate, Refunded, Payment_Method, Website, 
                            RefundReason, OrderStatus

                    FROM CS_CTEUK CC
                    --WHERE Refunded > 0 

                    UNION ALL

                    SELECT DISTINCT
                        OrderId, 0 as EyeglassesParentOrderid, OrderDate, RefundDate, Refunded, Payment_Method, Website, 
                            RefundReason, OrderStatus

                    FROM CS_CTEFR CC
                    --WHERE Refunded > 0 

                    ORDER BY RefundDate , Website desc
        '''%{'year':year, 'month':month}

        df = pd.read_sql_query(sql, con)

        def to_xlsx(bytes_io):

            xslx_writer = pd.ExcelWriter(bytes_io, engine="xlsxwriter")

            df.to_excel(xslx_writer, index=False, sheet_name="sheet1")

            xslx_writer.save()

        return send_bytes(to_xlsx, "refund.xlsx")



