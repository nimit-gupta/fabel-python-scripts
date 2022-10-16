from flask import Flask, redirect, render_template

application = app = Flask(__name__, template_folder='template', static_folder = 'static')

@app.route('/')
def index():
   return render_template('index.html')