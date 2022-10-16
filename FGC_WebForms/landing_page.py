from flask import Flask, render_template, redirect, session
from flask.templating import render_template_string

app = Flask(__name__, template_folder = 'template')

@app.route('/')

def index_page():

    return render_template_string('''
                                     <!DOCTYPE html>
                                        <html>
                                        <head>
                                        <!-- <link rel = 'stylesheets' href = "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous"> -->
                                        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
                                        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"></script>
                                        </head>
                                        <body>
                                        <div>
                                            <nav class="navbar navbar-expand-lg navbar-light bg-light">
                                               <div class="container-fluid">
                                                   <div class="collapse navbar-collapse" id="navbarNavDropdown">
                                                     <ul class="navbar-nav">
                                                       <a class="navbar-brand" href="#">
                                                          <img class="img-responsive" src="static/fgc-logo-1.png">
                                                       </a>
                                                       <div class="collapse navbar-collapse" id="navbarNavDropdown">
                                                            <ul class="navbar-nav"> 
                                                               <li class="nav-item">
                                                                 <a class="nav-link" href="/app_1">Labour Cost Form</a>
                                                               </li>
                                                               <li class="nav-item">
                                                                 <a class="nav-link" href="/app_2">Acquisition Cost Form</a>
                                                               </li>
                                                       </div>
                                                    </div>
                                                </div>
                                             </nav>
                                          </div>
                                          <div>
                                             <p style="text-align:center;margin-top:18%;opacity:0.5"><img src = 'static/fgc-logo-1.png' ></p>
                                          </div>
    
                                   ''')

