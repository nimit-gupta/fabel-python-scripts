from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware 
#from werkzeug.serving import run_simple 
from landing_page import app as app_0
from labour_cost import app as app_1
from acquisition_cost import app as app_2

app = Flask(__name__)

app.wsgi_app = DispatcherMiddleware(app_0, {
                                                 '/app_1': app_1,
                                                 '/app_2': app_2
                                                
                                          })

