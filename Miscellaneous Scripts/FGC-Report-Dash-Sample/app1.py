#!/usr/bin/env python

import pymssql 
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc

import warnings
warnings.filterwarnings(action = 'ignore', category = DeprecationWarning)

import plotly.graph_objs as go
import base64
import config

app = dash.Dash(name = 'app1', requests_pathname_prefix = '/app1/', external_stylesheets = [dbc.themes.BOOTSTRAP], title='FeelGoodContacts',server = True)

con_X = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

#con_X = pymssql.connect(config.CONN_STR)

sql_X = '''SELECT
                DISTINCT g.ProductType
           FROM 
                FG_PRODUCT c
           LEFT JOIN 
                FG_ProductDescription d ON (c.ProductId = d.ProductId)
           LEFT JOIN 
                FG_ProductBrandJoin e ON (d.ProductId = e.ProductID)
           LEFT JOIN 
                FG_BRAND f ON (e.BrandID = f.BrandID)
           LEFT JOIN 
                FG_ProductTypes g ON (c.ProductTypeId = g.ProductTypeId)
                
        '''

df_X = pd.read_sql_query(sql_X, con_X)

row = html.Div([
                html.Div([
                            dbc.Row([
                                    dbc.Col([
                                              dcc.Dropdown(id = 'producttypes',
                                                           options = [{'label': k, 'value' : k} for k in df_X['ProductType']],
                                                           placeholder = 'Products'
                                                          )
                                            ]),
                                    dbc.Col([
                                                dcc.Dropdown(id = 'Brands', 
                                                             placeholder = 'Brands',
                                                             style = {'width':'100%','margin-left':'0%'})
                                            ]),
                                    dbc.Col([
                                                dcc.Dropdown(id = 'Products', placeholder = 'Products', style = {'width':'100%'})
                                            ]),
                                   ], style = {'column-gap':'2px'}),
                            html.Br(),
                            dbc.Row([
                                    dbc.Col([
                                                dcc.Dropdown(id = 'Month', 
                                                             options = [{'label':'JAN', 'value':'01'},
                                                                        {'label':'FEB', 'value':'02'},
                                                                        {'label':'MAR', 'value':'03'},
                                                                        {'label':'APR', 'value':'04'},
                                                                        {'label':'MAY', 'value':'05'},
                                                                        {'label':'JUN', 'value':'06'},
                                                                        {'label':'JUL', 'value':'07'},
                                                                        {'label':'AUG', 'value':'08'},
                                                                        {'label':'SEP', 'value':'09'},
                                                                        {'label':'OCT', 'value':'10'},
                                                                        {'label':'NOV', 'value':'11'},
                                                                        {'label':'DEC', 'value':'12'},
                                                                        
                                                                        ],
                                                             placeholder = 'Month')
                                            ]),
                                    dbc.Col([
                                                dcc.Dropdown(id = 'Year', 
                                                             options = [{'label':'2021', 'value':'2021'},
                                                                        {'label':'2022', 'value':'2022'}],
                                                             placeholder = 'Year',
                                                             #style = {'left-margin':'-70%'}
                                                             )
                                            ]),
                                    dbc.Col([
                                             html.Button(
                                                        'Submit',
                                                        id = 'submit_button',
                                                        type = 'submit',
                                                        style = {'height':'35px','display':'inline-block',\
                                                                                        'background-color': '#ffffff',\
                                                                                        'font-weight':'bold', 'border-radius':'4px'
                                                                                        ,'margin-left':'-10px'}
                                                )
                                            ]),
                                    dbc.Col([
                                             html.A(
                                                     html.Button('Refresh', style = {'height':'35px','display':'inline-block',\
                                                                                        'background-color': '#ffffff',\
                                                                                        'font-weight':'bold', 'border-radius':'4px',
                                                                                        'margin-left':'-160px'}),
                                                     href = '/app1',
                                                   )
                                            ])
                                   ], style = {'margin-left':'20%'})
                        ])
                      ])

image_filename = 'static/fgc-logo-1.png'

encoded_image = base64.b64encode(open(image_filename, 'rb').read())
               
app.layout = html.Div([ 
                        html.Div([
                                  html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))
                                 ], style = {'margin-top':'3%','margin-left':'2%'}),
                        html.Div(
                                 [
                                  "Business Dashboard"
                                 ], 
                                 style = {'text-align':'center',
                                          'color':'black',
                                          'font-weight':'bold',
                                          'font-size':'150%',
                                          'font-family':'monospace'
                                         }
                                 ),
                        html.Br(),
                        html.Div([
                                  html.Div([
                                             dbc.Container(children = [row])
                                           ]),
                                        
                                  html.Div([dcc.Loading(
                                                        dcc.Graph(id = 'graph-1'))
                                                        ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                        'margin-top': '10px','border-style': 'groove'}
                                                ),
                                  html.Div([dcc.Loading(
                                                        dcc.Graph(id = 'graph-2'))
                                                        ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                'margin-top': '10px','border-style': 'groove'}
                                                ),
                                        
                                  html.Div([dcc.Loading(
                                                        dcc.Graph(id = 'graph-3'))
                                                        ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                'margin-top': '-5px','border-style': 'groove'}
                                                ),
                                  html.Div([dcc.Loading(
                                                        dcc.Graph(id = 'graph-4'))
                                                        ],style = {'width':'50%','display':'inline-block','padding':'0 20',\
                                                                'margin-top': '-5px','border-style': 'groove'}
                                                )
                                        ]),
                                                 
                        html.Div([
                                  html.A("Back to Menu",
                                          href = '/')
                                  ], style = {'text-align':'center'})
                      ])

@app.callback(Output('Brands','options'),[Input('producttypes','value')])
def brands_dropdown(producttypes):

    con_Y = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    #con_Y = pymssql.connect(config.CONN_STR)

    sql_Y = '''
                        SELECT
                        DISTINCT f.BrandName
                        FROM 
                        FG_PRODUCT c
                        LEFT JOIN 
                        FG_ProductDescription d ON (c.ProductId = d.ProductId)
                        LEFT JOIN 
                        FG_ProductBrandJoin e ON (d.ProductId = e.ProductID)
                        LEFT JOIN 
                        FG_BRAND f ON (e.BrandID = f.BrandID)
                        LEFT JOIN 
                        FG_ProductTypes g ON (c.ProductTypeId = g.ProductTypeId)
                        WHERE 
                        g.ProductType = '%(producttypes)s'
                        AND f.BrandName IS NOT NULL
          '''%{'producttypes': producttypes}

    df_Y = pd.read_sql_query(sql_Y, con_Y)

    return [{'label': k, 'value' : k} for k in df_Y['BrandName']] 

@app.callback(Output('Products','options'),[Input('Brands','value')])
def brands_dropdown(brands):

    con_Z = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    #con_Z = pymssql.connect(config.CONN_STR)

    sql_Z = '''
                SELECT
                        DISTINCT d.Name
                FROM 
                        FG_PRODUCT c 
                LEFT JOIN 
                        FG_ProductDescription d ON (c.ProductId = d.ProductId)
                LEFT JOIN 
                        FG_ProductBrandJoin e ON (d.ProductId = e.ProductID)
                LEFT JOIN 
                        FG_BRAND f ON (e.BrandID = f.BrandID)
                LEFT JOIN 
                        FG_ProductTypes g ON (c.ProductTypeId = g.ProductTypeId)
                WHERE 
                        f.BrandName = '%(brands)s'
                
         '''%{'brands': brands}

    df_Z = pd.read_sql_query(sql_Z, con_Z)

    return [{'label': k, 'value' : k} for k in df_Z['Name']] 


@app.callback(Output('graph-1','figure'),[Input('submit_button','n_clicks')],[State('producttypes','value'),
                                                                              State('Brands','value'),
                                                                              State('Products','value'),
                                                                              State('Month','value'), 
                                                                              State('Year','value')])

def update_graph_1(n_clicks, producttypes, brands, products, month, year):

    if n_clicks is not None and n_clicks > 0:

        con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

        #con = pymssql.connect(config.CONN_STR)

        sql = '''   SELECT
                         ORDER_DATE ORDER_DATE,
                         SUM(ORDER_AMOUNT) ORDER_AMOUNT
                    FROM
                        (
                            SELECT
                                CAST(a.CreatedOn AS VARCHAR(11)) AS ORDER_DATE,
                                ROUND(SUM(a.GrandTotalAmount),2) AS ORDER_AMOUNT
                            FROM 
                                FG_ORDER a 
                            LEFT JOIN 
                                FG_OrderItems b ON (a.OrderId = b.OrderId)
                            LEFT JOIN 
                                FG_PRODUCT c ON (b.ProductId = c.ProductId)
                            LEFT JOIN 
                                FG_ProductDescription d ON (c.ProductId = d.ProductId)
                            LEFT JOIN 
                                FG_ProductBrandJoin e ON (d.ProductId = e.ProductID)
                            LEFT JOIN 
                                FG_BRAND f ON (e.BrandID = f.BrandID)
                            LEFT JOIN 
                                FG_ProductTypes g ON (c.ProductTypeId = g.ProductTypeId)
                            WHERE 
                                CONVERT(VARCHAR(6),a.CreatedOn , 112) = '%(year)s%(month)s'
                                AND f.BrandName = '%(brands)s'
                                AND d.Name = '%(products)s'
                                AND g.ProductType = '%(producttypes)s'
                                AND a.PaymentTransactionStatus = 1
                                AND a.parentOrderid is null 
                                AND a.orderstatusid not in (1, 44)
                                AND a.currencyid IN (1,2)
                            GROUP BY 
                                a.CreatedOn
                       ) A
                    GROUP BY 
                         ORDER_DATE
                        
            '''%{'producttypes': producttypes, 'brands':brands, 'products':products, 'year':year, 'month':month}

        df = pd.read_sql_query(sql, con)

        y1 = df['ORDER_AMOUNT']
        
        x1 = df['ORDER_DATE']

        annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5)) for xi, yi in zip(x1, y1)]  
        return {
                    'data': [ 
                                go.Scatter (
                                        x = df['ORDER_DATE'],
                                        y = df['ORDER_AMOUNT'],
                                        name = 'Order Amount',
                                        mode = 'lines+markers',
                                        marker_color='rgb(102, 153, 255)'
                                        )
                               
                            ],

                    'layout':  
                            go.Layout (
                                        xaxis = {
                                                'title' : '<b>Dates</b>',
                                                'showgrid':False,
                                                'zeroline':False,
                                                'tickangle': 45
                                                },

                                        yaxis = {
                                                'title' : '<b>Order Amount (in GBP)</b>',
                                                'showgrid': False,
                                                'zeroline':False,
                                                },

                                        legend=dict(
                                                    orientation="h",
                                                    yanchor="bottom",
                                                    y=1.02,
                                                    xanchor="right",
                                                    x=1
                                                ),
                                        annotations = annot_1,

                                        title = '<b>Date Wise Order Amount</b>', 

                                        paper_bgcolor = '#e6e6e6',

                                        showlegend = True,

                                        hovermode = "x unified"
                                      )
                                    
                    }
    else:
        return {}

@app.callback(Output('graph-2','figure'),[Input('submit_button','n_clicks')],[State('producttypes','value'),
                                                                              State('Brands','value'),
                                                                              State('Products','value'),
                                                                              State('Month','value'), 
                                                                              State('Year','value')])

def update_graph_2(n_clicks, producttypes, brands, products, month, year):

    if n_clicks is not None and n_clicks > 0:

        con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

        #con = pymssql.connect(config.CONN_STR)

        sql = '''   SELECT
                         ORDER_DATE ORDER_DATE,
                         SUM(ORDER_AMOUNT) ORDER_AMOUNT
                    FROM
                        (
                            SELECT
                                DATENAME(MONTH,a.CreatedOn) AS ORDER_DATE,
                                ROUND(SUM(a.GrandTotalAmount),2) AS ORDER_AMOUNT
                            FROM 
                                FG_ORDER a 
                            LEFT JOIN 
                                FG_OrderItems b ON (a.OrderId = b.OrderId)
                            LEFT JOIN 
                                FG_PRODUCT c ON (b.ProductId = c.ProductId)
                            LEFT JOIN 
                                FG_ProductDescription d ON (c.ProductId = d.ProductId)
                            LEFT JOIN 
                                FG_ProductBrandJoin e ON (d.ProductId = e.ProductID)
                            LEFT JOIN 
                                FG_BRAND f ON (e.BrandID = f.BrandID)
                            LEFT JOIN 
                                FG_ProductTypes g ON (c.ProductTypeId = g.ProductTypeId)
                            WHERE 
                                CONVERT(VARCHAR(6),a.CreatedOn , 112) BETWEEN CONVERT(VARCHAR(6),DATEADD(Year,-1*DATEDIFF(Year,GETDATE(),0),0), 112) AND '%(year)s%(month)s'
                                AND f.BrandName = '%(brands)s'
                                AND d.Name = '%(products)s'
                                AND g.ProductType = '%(producttypes)s'
                                AND a.PaymentTransactionStatus = 1
                                AND a.parentOrderid is null 
                                AND a.orderstatusid not in (1, 44)
                                AND a.currencyid IN (1,2)
                            GROUP BY 
                                a.CreatedOn        
                       ) A
                    GROUP BY 
                         ORDER_DATE
                    ORDER BY
                         DATEPART(mm, CAST(ORDER_DATE + '1900' AS DATETIME)) asc
                        
            '''%{'producttypes': producttypes, 'brands':brands, 'products':products, 'year':year, 'month':month}

        df = pd.read_sql_query(sql, con)

        y1 = df['ORDER_AMOUNT']
        
        x1 = df['ORDER_DATE']

        annot_1 = [dict(x=xi,y=yi,text= str(yi),xanchor='center',yanchor='bottom',showarrow=False,\
                   font=dict(size = 9.5)) for xi, yi in zip(x1, y1)]  
        return {
                    'data': [ 
                                go.Scatter (
                                        x = df['ORDER_DATE'],
                                        y = df['ORDER_AMOUNT'],
                                        name = 'Order Amount',
                                        mode = 'lines+markers',
                                        marker_color='rgb(102, 153, 255)'
                                        )
                               
                            ],

                    'layout':  
                            go.Layout (
                                        xaxis = {
                                                'title' : '<b>Dates</b>',
                                                'showgrid':False,
                                                'zeroline':False,
                                                'tickangle': 45
                                                },

                                        yaxis = {
                                                'title' : '<b>Order Amount (in GBP)</b>',
                                                'showgrid': False,
                                                'zeroline':False,
                                                },

                                        legend=dict(
                                                    orientation="h",
                                                    yanchor="bottom",
                                                    y=1.02,
                                                    xanchor="right",
                                                    x=1
                                                ),
                                        annotations = annot_1,

                                        title = '<b>Month Wise Order Amount</b>', 

                                        paper_bgcolor = '#e6e6e6',

                                        showlegend = True,

                                        hovermode = "x unified"
                                      )
                                    
                    }
    else:
        return {}





