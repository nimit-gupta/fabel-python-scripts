from werkzeug.middleware.dispatcher import DispatcherMiddleware
from app1 import app as app1
from app2 import app as app2
from application import application as application

app_run = DispatcherMiddleware(application, {
                                                '/app1': app1.server,
                                                '/app2': app2.server
                                              }
                              )   