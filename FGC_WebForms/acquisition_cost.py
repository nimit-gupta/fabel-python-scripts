from flask import Flask, render_template, request, session, render_template_string, redirect, url_for
import pymssql
import pandas as pd

app = Flask(__name__, template_folder = 'template', static_folder = 'static')

app.secret_key = "feelgoodcontact"

@app.route('/')

def index():

    return render_template_string(
                                    ''' 
                                     <!DOCTYPE html>
                                        <html>
                                        <head>
                                        <!-- <link rel = 'stylesheets' href = "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous"> -->
                                        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
                                        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"></script>
                                        </head>
                                        <body>
                                        <nav class="navbar navbar-expand-lg navbar-light bg-light">
                                            <div class="container-fluid">
                                            <div class="collapse navbar-collapse" id="navbarNavDropdown">
                                                <ul class="navbar-nav">
                                                <a class="navbar-brand" href="#">
                                                    <img class="img-responsive" src="static/fgc-logo-1.png">
                                                </a>
                                                </ul>
                                            </div>
                                            </div>
                                        </nav>
                                        </div>
                                        <br></br>
                                        <br></br>
                                        <div>
                                            <section class="h-100">
                                            <div class="container h-100">
                                                <div class="row justify-content-sm-center h-100">
                                                <div class="col-xxl-4 col-xl-5 col-lg-5 col-md-7 col-sm-9">
                                                    <div class="card shadow-lg">
                                                    <div class="card-body p-5">
                                                        <h1 class="fs-4 card-title fw-bold mb-4">Login</h1>
                                                        <form action = "/app_2/show" method = 'POST'>
                                                        <div class="mb-3">
                                                            <label class="mb-2 text-muted" for="email">E-Mail Address</label>
                                                            <input id="email" type="email" class="form-control" name="email" value="" required autofocus>
                                                        </div>
                                                        <div class="mb-3">
                                                            <label class="mb-2 text-muted" for="password">Password</label>
                                                            <input id="password" type="password" class="form-control" name="password" required>
                                                        </div>
                                                        <div class="d-flex align-items-center">
                                                            <button type="submit" class="btn btn-dark">Submit</button>
                                                        </div>
                                                        </form>
                                                    </div>
                                                    </div>
                                                </div>
                                                </div>
                                            </div>
                                            </section> 
                                        </div>
                                        <!--<br></br>-->
                                        <div style = 'margin-left:47%; margin-top:10%'>
                                            <a href = '/' style="text-decoration:none; color:black">Click to Menu</a>
                                        </div>
                                        </body>
                                        </html>
                    ''')

@app.route('/show', methods = ['GET','POST'])

def show():

    email = request.form.get('email')

    password = request.form.get('password')

    #con_0 = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    con_0 = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    sql_0 = '''
            SELECT 
                    a.AdminUserId,
                    a.Email,
                    b.Password
                FROM 
                    FG_AdminUser a
                INNER JOIN 
                    fg_userpy b ON (a.AdminUserId = b.AdminUserId)
                WHERE 
                    a.Email = '%(email)s'
                    AND b.Password = '%(password)s'
                    AND a.Enable = 1
          '''%{'email': email,'password':password}

    df_0 = pd.read_sql_query(sql_0, con_0)

    adminuserid = df_0['AdminUserId'].squeeze()

    session['admin_user_id'] = str(adminuserid)

    if df_0.empty is True:

        return render_template_string('''
                                        <!DOCTYPE html>
                                            <html>
                                            <head>
                                            <!-- <link rel = 'stylesheets' href = "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous"> -->
                                            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
                                            </head>
                                            <body>
                                                <div>
                                                    <div class="alert alert-danger" role="alert">
                                                        <h4 class="alert-heading">Wrong Credentials!</h4>
                                                        <p>Please <a href = '/' style="text-decoration:none"> Click Here! </a>to login again, thank you.</p>    
                                                    </div>
                                                </div>
                                            </body>
                                            </html>
                                      ''')

    else:

        return redirect(url_for('select_country'))


@app.route('/select_country')

def select_country():

        return render_template_string('''
                                         <!DOCTYPE html>
                                            <html>
                                                <head>
                                                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
                                                </head>
                                                <body>
                                                    <div style = 'margin-left:2%;margin-top:2%'>
                                                        <img src="static/fgc-logo-1.png" alt="example" class="logo"/>
                                                    </div>
                                                    <div>
                                                        <form action = '/app_2/redirect_to_country_page' method = 'POST'>
                                                        <div class = 'row' style = 'margin-top:15%;margin-left:40%; column-gap:5px'>
                                                            <div class = 'column'>
                                                                <select id = 'select_country' name = 'select_country' class = 'form-control' style = 'width:100%'>
                                                                    <option value="">--Choose Country--</option>
                                                                    <option value="UK">UK</option>
                                                                    <option value="IE">IE</option>
                                                                    <option value="FR">FR</option>
                                                                </select>
                                                            </div>
                                                            <div class = 'column'>
                                                                <button onclick="myFunction()" class="btn btn-dark">Submit</button>
                                                            </div>
                                                        </div>
                                                        </form>
                                                    </div>
                                                    <br></br>
                                                    <div style = 'margin-left:45%'>
                                                       <a href = '/app_2' style="text-decoration:none;color:black">Click to Back</a>
                                                    </div>
                                                    <script>
                                                        function myFunction() {confirm("Are you confirm!");}
                                                    </script>
                                                </body>
                                            </html>
                                       ''')

@app.route('/redirect_to_country_page', methods = ['GET','POST'])

def redirect_to_country_page():

    select_country = request.form.get('select_country')

    if select_country == 'UK':

            #con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

            con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live') 
 

            sql = '''
                     SELECT 
                           DISTINCT CONVERT(DATE, AcquistionCostDate, 101) AcquistionCostDate,
                           Website,
                           Google ,
                           Bing,
                           Facebook
                     FROM
                          FG_Daily_Acquisition_Cost
                     WHERE 
                          AcquistionCostDate >= DATEADD(m, DATEDIFF(m, 0, GETDATE()), 0)  AND AcquistionCostDate <= DATEADD(m,DATEDIFF(m, -1, GETDATE()),-1)
                          AND Website = 'UK'
                     ORDER BY 
                          AcquistionCostDate DESC
                  '''

            df = pd.read_sql_query(sql, con)

            return render_template_string('''
                                                <!DOCTYPE html>
                                                <head>
                                                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
                                                </head>
                                                <body> 
                                                    <div style = 'margin-left:2%;margin-top:2%'>
                                                        <img src="static/fgc-logo-1.png" alt="example" class="logo"/>
                                                    </div>
                                                    <div class = 'container' style = 'text-align: center; margin-top:5%'>
                                                        {% block content %}
                                                        <table class="table table-sm">
                                                            <thead class="thead-dark">
                                                                <tr>
                                                                    <th scope="col">AcquistionCostDate</th>
                                                                    <th scope="col">Website</th>
                                                                    <th scope="col">Google</th>
                                                                    <th scope="col">Bing</th>
                                                                    <th scope="col">Facebook</th>
                                                                </tr>
                                                            </thead>
                                                            <tbody style="overflow-y:scroll; height:100px;">
                                                            {% for row in data %}
                                                                <tr>
                                                                    <td>{{row['AcquistionCostDate']}}</td>
                                                                    <td>{{row['Website']}}</td>
                                                                    <td>{{row['Google']}}</td>
                                                                    <td>{{row['Bing']}}</td>
                                                                    <td>{{row['Facebook']}}</td>
                                                                </tr>
                                                            {% endfor %}
                                                            </tbody>
                                                        </table>
                                                        {% endblock %}
                                                    </div>
                                                    
                                                        <div class = 'row' style = 'margin-left:44%; column-gap:1px'>
                                                            <div class = 'column'>
                                                                <a href = '/app_2/add_new_data_uk' class = 'btn btn-dark'>Click to Add</a>
                                                            </div>
                                                            <div class = 'column'>
                                                                <a href = '/app_2/edit_exits_data_uk' class = 'btn btn-dark'>Click to Edit</a>
                                                            </div>
                                                        </div>
                                                        <div class = 'row' style = 'margin-left:48%'>
                                                            <div class = 'column'>
                                                                <a href = '/app_2/select_country' style='color:black'>Click to Back</a>
                                                            </div>
                                                        </div>
                                                
                                                </body>
                                                
                        ''', data = df.to_dict(orient='records'))

    elif select_country == 'IE':

            #con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')
            
            con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

            sql = '''
                     SELECT 
                           DISTINCT CONVERT(DATE, AcquistionCostDate, 101) AcquistionCostDate,
                           Website,
                           Google ,
                           Bing,
                           Facebook
                     FROM
                         FG_Daily_Acquisition_Cost
                     WHERE 
                          AcquistionCostDate >= DATEADD(m, DATEDIFF(m, 0, GETDATE()), 0)  AND AcquistionCostDate <= DATEADD(m,DATEDIFF(m, -1, GETDATE()),-1)
                          AND Website = 'IE'
                     ORDER BY 
                          AcquistionCostDate DESC
                  '''

            df = pd.read_sql_query(sql, con)

            return render_template_string('''
                                             <!DOCTYPE html>
                                                <head>
                                                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
                                                </head>
                                                <body> 
                                                    <div style = 'margin-left:2%;margin-top:2%'>
                                                        <img src="static/fgc-logo-1.png" alt="example" class="logo"/>
                                                    </div>
                                                    <div class = 'container' style = 'text-align: center; margin-top:5%'>
                                                        {% block content %}
                                                        <table class="table table-sm">
                                                            <thead class="thead-dark">
                                                                <tr>
                                                                    <th scope="col">AcquistionCostDate</th>
                                                                    <th scope="col">Website</th>
                                                                    <th scope="col">Google</th>
                                                                    <th scope="col">Bing</th>
                                                                    <th scope="col">Facebook</th>
                                                                </tr>
                                                            </thead>
                                                            <tbody style="overflow-y:scroll; height:100px;">
                                                            {% for row in data %}
                                                                <tr>
                                                                    <td>{{row['AcquistionCostDate']}}</td>
                                                                    <td>{{row['Website']}}</td>
                                                                    <td>{{row['Google']}}</td>
                                                                    <td>{{row['Bing']}}</td>
                                                                    <td>{{row['Facebook']}}</td>
                                                                </tr>
                                                            {% endfor %}
                                                            </tbody>
                                                        </table>
                                                        {% endblock %}
                                                    </div>
                                                    
                                                        <div class = 'row' style = 'margin-left:44%; column-gap:1px'>
                                                            <div class = 'column'>
                                                                <a href = '/app_2/add_new_data_ie' class = 'btn btn-dark'>Click to Add</a>
                                                            </div>
                                                            <div class = 'column'>
                                                                <a href = '/app_2/edit_exits_data_ie' class = 'btn btn-dark'>Click to Edit</a>
                                                            </div>
                                                        </div>
                                                        <div class = 'row' style = 'margin-left:48%'>
                                                            <div class = 'column'>
                                                                <a href = '/app_2/select_country' style = 'color:black'>Click to Back</a>
                                                            </div>
                                                        </div>
                                                
                                                </body>
            
                                          ''', data = df.to_dict(orient='records'))

    elif select_country == 'FR':

            #con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live') 

            con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

            sql = '''
                     SELECT 
                           DISTINCT CONVERT(DATE, AcquistionCostDate, 101) AcquistionCostDate,
                           Website,
                           Google ,
                           Bing,
                           Facebook
                     FROM
                          FG_Daily_Acquisition_Cost
                     WHERE 
                          AcquistionCostDate >= DATEADD(m, DATEDIFF(m, 0, GETDATE()), 0)  AND AcquistionCostDate <= DATEADD(m,DATEDIFF(m, -1, GETDATE()),-1)
                          AND Website = 'FR'
                     ORDER BY 
                          AcquistionCostDate DESC
                  '''

            df = pd.read_sql_query(sql, con)

            return render_template_string('''
                                     <!DOCTYPE html>
                                                <head>
                                                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
                                                </head>
                                                <body> 
                                                    <div style = 'margin-left:2%;margin-top:2%'>
                                                        <img src="static/fgc-logo-1.png" alt="example" class="logo"/>
                                                    </div>
                                                    <div class = 'container' style = 'text-align: center; margin-top:5%'>
                                                        {% block content %}
                                                        <table class="table table-sm">
                                                            <thead class="thead-dark">
                                                                <tr>
                                                                    <th scope="col">AcquistionCostDate</th>
                                                                    <th scope="col">Website</th>
                                                                    <th scope="col">Google</th>
                                                                    <th scope="col">Bing</th>
                                                                    <th scope="col">Facebook</th>
                                                                </tr>
                                                            </thead>
                                                            <tbody style="overflow-y:scroll; height:100px;">
                                                            {% for row in data %}
                                                                <tr>
                                                                    <td>{{row['AcquistionCostDate']}}</td>
                                                                    <td>{{row['Website']}}</td>
                                                                    <td>{{row['Google']}}</td>
                                                                    <td>{{row['Bing']}}</td>
                                                                    <td>{{row['Facebook']}}</td>
                                                                </tr>
                                                            {% endfor %}
                                                            </tbody>
                                                        </table>
                                                        {% endblock %}
                                                    </div>
                                                    
                                                        <div class = 'row' style = 'margin-left:44%; column-gap:1px'>
                                                            <div class = 'column'>
                                                                <a href = '/app_2/add_new_data_fr' class = 'btn btn-dark'>Click to Add</a>
                                                            </div>
                                                            <div class = 'column'>
                                                                <a href = '/app_2/edit_exits_data_fr' class = 'btn btn-dark'>Click to Edit</a>
                                                            </div>
                                                        </div>
                                                        <div class = 'row' style = 'margin-left:48%'>
                                                            <div class = 'column'>
                                                                <a href = '/app_2/select_country' style = 'color:black'>Click to Back</a>
                                                            </div>
                                                        </div>
                                                
                                                </body>
            
                                   ''', data = df.to_dict(orient='records'))

    else:
            pass
             
@app.route('/add_new_data_uk')

def add_new_data_uk():

    return render_template_string('''
                                     <!DOCTYPE html>
                                        <html>
                                            <head>
                                                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
                                            </head>
                                            <body>
                                                <div>
                                                    <div style = 'margin-left:2%;margin-top:2%'>
                                                        <img src="static/fgc-logo-1.png" alt="example" class="logo"/>
                                                    </div>
                                                </div>
                                                <div>
                                                    <form action = '/app_2/save_costs_uk' method="POST"> 
                                                    <div class = 'row' style = 'margin-top:10%;margin-left:15%; column-gap:5px'>
                                                        <div class = 'column'>
                                                            <input class="form-control" type = 'date' id="date" name="date" min="2021-01-01"  max="2022-12-31">
                                                        </div>
                                                        <div class = 'column'>
                                                            <input class="form-control" type = 'text' id = 'website', name = 'website', placeholder = 'UK' value = 'UK'>
                                                        </div>
                                                        <div class = 'column'>
                                                            <input class="form-control" type = 'number' step = 'any' id = 'google', name = 'google', placeholder = 'Google'>
                                                        </div>
                                                        <div class = 'column'>
                                                            <input class="form-control" type = 'number' step = 'any' id = 'bing', name = 'bing', placeholder = 'Bing'>
                                                        </div>
                                                        <div class = 'column'>
                                                            <input class="form-control" type = 'number' step = 'any' id = 'facebook', name = 'facebook', placeholder = 'Facebook'>
                                                        </div>
                                                        <div class='column'>
                                                            <button onclick="myFunction()" class="btn btn-dark" style = 'height:39px; width:150px;font-family:monospace'>Save</button>
                                                        </div>
                                                    </div>
                                                </div>
                                                <br></br>
                                                   <div style = 'margin-left:45%'>
                                                     <a href = '/app_2' style="text-decoration:none;color:black">Click to Back</a>
                                                   </div>
                                                <script>
                                                    function myFunction() {confirm("Are you confirm!");}
                                                </script>
                                            </body>
                                        </html>
                                ''') 

@app.route('/save_costs_uk' ,methods = ['GET','POST'])

def save_costs_uk():

    acquistioncostdate = request.form.get('date')

    website = request.form.get('website')

    google = request.form.get('google')

    bing = request.form.get('bing')

    facebook = request.form.get('facebook')

    adminuserid = session.get('admin_user_id')

    #con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    cur = con.cursor()

    cur.execute('''INSERT INTO FG_Daily_Acquisition_Cost(AcquistionCostDate, Website, Google, Bing,Facebook, AdminUserId) VALUES (%s,%s,%s,%s,%s,%s)''', 
                        (acquistioncostdate,website,google,bing,facebook,adminuserid))

    con.commit()

    cur.close()

    #con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    sql = '''
                     SELECT 
                           DISTINCT CONVERT(DATE, AcquistionCostDate, 101) AcquistionCostDate,
                           Website,
                           Google ,
                           Bing,
                           Facebook
                     FROM
                          FG_Daily_Acquisition_Cost
                     WHERE 
                         AcquistionCostDate >= DATEADD(m, DATEDIFF(m, 0, GETDATE()), 0)  AND AcquistionCostDate <= DATEADD(m,DATEDIFF(m, -1, GETDATE()),-1)
                         AND Website = 'UK'
                ORDER BY
                        1 DESC
                 
              '''

    df = pd.read_sql_query(sql, con)

    return render_template_string('''
                                     <!DOCTYPE html>
                                    <head>
                                        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
                                    </head>
                                    <body> 
                                        <div style = 'margin-left:2%;margin-top:2%'>
                                            <img src="static/fgc-logo-1.png" alt="example" class="logo"/>
                                        </div>
                                        <div class = 'container' style = 'text-align: center; margin-top:5%'>
                                            {% block content %}
                                            <table class="table table-sm">
                                                <thead class="thead-dark">
                                                    <tr>
                                                        <th scope="col">AcquistionCostDate</th>
                                                        <th scope="col">Website</th>
                                                        <th scope="col">Google</th>
                                                        <th scope="col">Bing</th>
                                                        <th scope="col">Facebook</th>
                                                    </tr>
                                                </thead>
                                                <tbody style="overflow-y:scroll; height:100px;">
                                                {% for row in data %}
                                                    <tr>
                                                        <td>{{row['AcquistionCostDate']}}</td>
                                                        <td>{{row['Website']}}</td>
                                                        <td>{{row['Google']}}</td>
                                                        <td>{{row['Bing']}}</td>
                                                        <td>{{row['Facebook']}}</td>
                                                    </tr>
                                                {% endfor %}
                                                </tbody>
                                            </table>
                                            {% endblock %}
                                        </div>
                                        
                                            <div class = 'row' style = 'margin-left:44%; column-gap:1px'>
                                                <div class = 'column'>
                                                    <a href = '/app_2/add_new_data_uk' class = 'btn btn-dark'>Click to Add</a>
                                                </div>
                                                <div class = 'column'>
                                                    <a href = '/app_2/edit_exits_data_uk' class = 'btn btn-dark'>Click to Edit</a>
                                                </div>
                                            </div>
                                            <div class = 'row' style = 'margin-left:48%'>
                                                <div class = 'column'>
                                                    <a href = '/app_2/select_country' style = 'color:black'>Click to Back</a>
                                                </div>
                                            </div>
                                    
                                    </body>
    
                                  ''', data = df.to_dict(orient='records'))

@app.route('/edit_exits_data_uk')

def edit_exits_data_uk():

    return render_template_string('''
                                     <!DOCTYPE html>
                                        <html>
                                            <head>
                                                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
                                            </head>
                                            <body>
                                                <div>
                                                    <div style = 'margin-left:2%;margin-top:2%'>
                                                        <img src="static/fgc-logo-1.png" alt="example" class="logo"/>
                                                    </div>
                                                </div>
                                                <div>
                                                    <form action='/app_2/edit_costs_uk' method="POST" name = 'form-one'> 
                                                        <div class = 'row' style = 'margin-top:10%;margin-left:40%; column-gap:5px'>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'date' id="date" name="exitdate" value={{date}} min="2021-01-01"  max="2022-12-31">
                                                            </div>
                                                            <div class='column'>
                                                                <button class="btn btn-dark" style = 'height:39px; width:150px;font-family:monospace' name = 'submit'>Submit</button>
                                                        </div>
                                                        </div>
                                                    </form>
                                                </div>
                                            
                                            
                                                <br></br>
                                        
                                                <div>
                                                    <form action = '/app_2/save_edits_uk' method="POST" name = 'form-second'> 
                                                        <div class = 'row' style = 'margin-top:2%;margin-left:15%; column-gap:5px'>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'date' id="date" name="date" value={{date}} min="2021-01-01"  max="2022-12-31">
                                                            </div>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'text' id = 'website', name = 'website', placeholder = 'Website' value = {{website}}>
                                                            </div>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'number' step = 'any' id = 'google', name = 'google', placeholder = 'Google' value = {{google}}>
                                                            </div>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'number' step = 'any' id = 'bing', name = 'bing', placeholder = 'Bing' value = {{bing}}>
                                                            </div>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'number' step = 'any' id = 'facebook', name = 'facebook', placeholder = 'Facebook' value = {{facebook}}>
                                                            </div>
                                                            <div class='column'>
                                                                <button class="btn btn-dark" style = 'height:39px; width:150px;font-family:monospace' name = 'edit'>Edit</button>
                                                            </div>
                                                        </div>
                                                    </form>
                                                </div>  
                                                <br></br>
                                                  <div style = 'margin-left:45%'>
                                                     <a href = '/app_2' style="text-decoration:none;color:black">Click to Back</a>
                                                  </div>  
                                            </body>
                                        </html>
                                                                            
                                                                        ''')

@app.route('/edit_costs_uk', methods = ['GET', 'POST'])

def edit_costs_uk():

    acquistioncostdate = request.form.get('exitdate')

    #con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    sql = '''
             
                   SELECT 
                        DISTINCT CONVERT(DATE, AcquistionCostDate, 101) Date,
                        Website,
                        Google,
                        Bing,
                        Facebook
                FROM 
                        FG_Daily_Acquisition_Cost
                WHERE
                        AcquistionCostDate = '%(acquistioncostdate)s'
                        AND Website = 'UK'

          '''%{'acquistioncostdate': acquistioncostdate}

    df = pd.read_sql_query(sql, con)

    date = df['Date'].squeeze()

    website = df['Website'].squeeze()

    google = df['Google'].squeeze()

    bing = df['Bing'].squeeze()

    facebook = df['Facebook'].squeeze()

    return render_template_string('''
                                     <!DOCTYPE html>
                                        <html>
                                            <head>
                                                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
                                            </head>
                                            <body>
                                                <div>
                                                    <div style = 'margin-left:2%;margin-top:2%'>
                                                        <img src="static/fgc-logo-1.png" alt="example" class="logo"/>
                                                    </div>
                                                </div>
                                                <div>
                                                    <form action='/app_2/edit_costs_uk' method="POST" name = 'form-one'> 
                                                        <div class = 'row' style = 'margin-top:10%;margin-left:40%; column-gap:5px'>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'date' id="date" name="exitdate" value={{date}} min="2021-01-01"  max="2022-12-31">
                                                            </div>
                                                            <div class='column'>
                                                                <button class="btn btn-dark" style = 'height:39px; width:150px;font-family:monospace' name = 'submit'>Submit</button>
                                                        </div>
                                                        </div>
                                                    </form>
                                                </div>
                                            
                                            
                                                <br></br>
                                        
                                                <div>
                                                    <form action='/app_2/save_edits_uk' method="POST" name = 'form-second'> 
                                                        <div class = 'row' style = 'margin-top:2%;margin-left:15%; column-gap:5px'>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'date' id="date" name="date" value={{date}} min="2021-01-01"  max="2022-12-31">
                                                            </div>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'text' id = 'website', name = 'website', placeholder = 'Website' value = {{website}}>
                                                            </div>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'number' step = 'any' id = 'google', name = 'google', placeholder = 'Google' value = {{google}}>
                                                            </div>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'number' step = 'any' id = 'bing', name = 'bing', placeholder = 'Bing' value = {{bing}}>
                                                            </div>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'number' step = 'any' id = 'facebook', name = 'facebook', placeholder = 'Facebook' value = {{facebook}}>
                                                            </div>
                                                            <div class='column'>
                                                                <button class="btn btn-dark" style = 'height:39px; width:150px;font-family:monospace' name = 'edit'>Edit</button>
                                                            </div>
                                                        </div>
                                                    </form>
                                                </div> 
                                                <br></br>
                                                    <div style = 'margin-left:45%'>
                                                       <a href = '/app_2' style="text-decoration:none;color:black">Click to Back</a>
                                                    </div>   
                                            </body>
                                        </html>
                                                                        ''', date = date, website = website, google = google, bing = bing, facebook = facebook)

@app.route('/save_edits_uk', methods = ['GET','POST'])

def save_edits_uk():

    acquistioncostdate = request.form.get('date')
    
    website = request.form.get('website')

    google = request.form.get('google')

    bing = request.form.get('bing')

    facebook = request.form.get('facebook')

    adminuserid = session.get('admin_user_id')

    #con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    cur = con.cursor()

    cur.execute(" UPDATE FG_Daily_Acquisition_Cost SET Google = '%s', Bing = '%s', Facebook = '%s', AdminUserid = '%s' WHERE AcquistionCostDate = '%s' AND Website = '%s'"%(google, bing, facebook, adminuserid, acquistioncostdate, website)) 
                        
    con.commit()

    cur.close()

    #session.clear()

    #con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    sql = '''
                 SELECT 
                           DISTINCT CONVERT(DATE, AcquistionCostDate, 101) AcquistionCostDate,
                           Website,
                           Google ,
                           Bing,
                           Facebook
                     FROM
                          FG_Daily_Acquisition_Cost
                     WHERE 
                         AcquistionCostDate >= DATEADD(m, DATEDIFF(m, 0, GETDATE()), 0)  AND AcquistionCostDate <= DATEADD(m,DATEDIFF(m, -1, GETDATE()),-1)
                         AND Website = 'UK'
                ORDER BY
                        1 DESC
              '''

    df = pd.read_sql_query(sql, con)

    return render_template_string('''
                                <!DOCTYPE html>
                                <head>
                                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
                                </head>
                                <body> 
                                    <div style = 'margin-left:2%;margin-top:2%'>
                                        <img src="static/fgc-logo-1.png" alt="example" class="logo"/>
                                    </div>
                                    <div class = 'container' style = 'text-align: center; margin-top:5%'>
                                        {% block content %}
                                        <table class="table table-sm">
                                            <thead class="thead-dark">
                                                <tr>
                                                    <th scope="col">AcquistionCostDate</th>
                                                    <th scope="col">Website</th>
                                                    <th scope="col">Google</th>
                                                    <th scope="col">Bing</th>
                                                    <th scope="col">Facebook</th>
                                                </tr>
                                            </thead>
                                            <tbody style="overflow-y:scroll; height:100px;">
                                            {% for row in data %}
                                                <tr>
                                                    <td>{{row['AcquistionCostDate']}}</td>
                                                    <td>{{row['Website']}}</td>
                                                    <td>{{row['Google']}}</td>
                                                    <td>{{row['Bing']}}</td>
                                                    <td>{{row['Facebook']}}</td>
                                                </tr>
                                            {% endfor %}
                                            </tbody>
                                        </table>
                                        {% endblock %}
                                    </div>
                                    
                                        <div class = 'row' style = 'margin-left:44%; column-gap:1px'>
                                            <div class = 'column'>
                                                <a href = '/app_2/add_new_data_uk' class = 'btn btn-dark'>Click to Add</a>
                                            </div>
                                            <div class = 'column'>
                                                <a href = '/app_2/edit_exits_data_uk' class = 'btn btn-dark'>Click to Edit</a>
                                            </div>
                                        </div>
                                        <div class = 'row' style = 'margin-left:48%'>
                                            <div class = 'column'>
                                                <a href = '/app_2/select_country' style = 'color:black'>Back to Menu</a>
                                            </div>
                                        </div>
                                
                                </body>''', data = df.to_dict(orient='records'))


###################### IE #######################################################

@app.route('/add_new_data_ie')

def add_new_data_ie():

    return render_template_string('''
                                     <!DOCTYPE html>
                                        <html>
                                            <head>
                                                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
                                            </head>
                                            <body>
                                                <div>
                                                    <div style = 'margin-left:2%;margin-top:2%'>
                                                        <img src="static/fgc-logo-1.png" alt="example" class="logo"/>
                                                    </div>
                                                </div>
                                                <div>
                                                    <form action = '/app_2/save_costs_ie' method="POST"> 
                                                    <div class = 'row' style = 'margin-top:10%;margin-left:15%; column-gap:5px'>
                                                        <div class = 'column'>
                                                            <input class="form-control" type = 'date' id="date" name="date" min="2021-01-01"  max="2022-12-31">
                                                        </div>
                                                        <div class = 'column'>
                                                            <input class="form-control" type = 'text' id = 'website', name = 'website', placeholder = 'IE' value = 'IE'>
                                                        </div>
                                                        <div class = 'column'>
                                                            <input class="form-control" type = 'number' step = 'any' id = 'google', name = 'google', placeholder = 'Google'>
                                                        </div>
                                                        <div class = 'column'>
                                                            <input class="form-control" type = 'number' step = 'any' id = 'bing', name = 'bing', placeholder = 'Bing'>
                                                        </div>
                                                        <div class = 'column'>
                                                            <input class="form-control" type = 'number' step = 'any' id = 'facebook', name = 'facebook', placeholder = 'Facebook'>
                                                        </div>
                                                        <div class='column'>
                                                            <button onclick="myFunction()" class="btn btn-dark" style = 'height:39px; width:150px;font-family:monospace'>Save</button>
                                                        </div>
                                                    </div>
                                                </div>
                                               <br></br>
                                                   <div style = 'margin-left:45%'>
                                                      <a href = '/app_2' style="text-decoration:none;color:black">Click to Back</a>
                                                </div>
                                                <script>
                                                    function myFunction() {confirm("Are you confirm!");}
                                                </script>
                                            </body>
                                        </html>
                                ''') 

@app.route('/save_costs_ie' ,methods = ['GET','POST'])

def save_costs_ie():

    acquistioncostdate = request.form.get('date')

    website = request.form.get('website')

    google = request.form.get('google')

    bing = request.form.get('bing')

    facebook = request.form.get('facebook')

    adminuserid = session.get('admin_user_id')

    #con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    cur = con.cursor()

    cur.execute('''INSERT INTO FG_Daily_Acquisition_Cost(AcquistionCostDate, Website, Google, Bing,Facebook, AdminUserId) VALUES (%s,%s,%s,%s,%s,%s)''', 
                        (acquistioncostdate,website,google,bing,facebook,adminuserid))

    con.commit()

    cur.close()

    #con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    sql = '''
                     SELECT 
                           DISTINCT CONVERT(DATE, AcquistionCostDate, 101) AcquistionCostDate,
                           Website,
                           Google ,
                           Bing,
                           Facebook
                     FROM
                          FG_Daily_Acquisition_Cost
                     WHERE 
                         AcquistionCostDate >= DATEADD(m, DATEDIFF(m, 0, GETDATE()), 0)  AND AcquistionCostDate <= DATEADD(m,DATEDIFF(m, -1, GETDATE()),-1)
                         AND Website = 'IE'
                ORDER BY
                        1 DESC
                 
              '''

    df = pd.read_sql_query(sql, con)

    return render_template_string('''
                                     <!DOCTYPE html>
                                    <head>
                                        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
                                    </head>
                                    <body> 
                                        <div style = 'margin-left:2%;margin-top:2%'>
                                            <img src="static/fgc-logo-1.png" alt="example" class="logo"/>
                                        </div>
                                        <div class = 'container' style = 'text-align: center; margin-top:5%'>
                                            {% block content %}
                                            <table class="table table-sm">
                                                <thead class="thead-dark">
                                                    <tr>
                                                        <th scope="col">AcquistionCostDate</th>
                                                        <th scope="col">Website</th>
                                                        <th scope="col">Google</th>
                                                        <th scope="col">Bing</th>
                                                        <th scope="col">Facebook</th>
                                                    </tr>
                                                </thead>
                                                <tbody style="overflow-y:scroll; height:100px;">
                                                {% for row in data %}
                                                    <tr>
                                                        <td>{{row['AcquistionCostDate']}}</td>
                                                        <td>{{row['Website']}}</td>
                                                        <td>{{row['Google']}}</td>
                                                        <td>{{row['Bing']}}</td>
                                                        <td>{{row['Facebook']}}</td>
                                                    </tr>
                                                {% endfor %}
                                                </tbody>
                                            </table>
                                            {% endblock %}
                                        </div>
                                        
                                            <div class = 'row' style = 'margin-left:44%; column-gap:1px'>
                                                <div class = 'column'>
                                                    <a href = '/app_2/add_new_data_ie' class = 'btn btn-dark'>Click to Add</a>
                                                </div>
                                                <div class = 'column'>
                                                    <a href = '/app_2/edit_exits_data_ie' class = 'btn btn-dark'>Click to Edit</a>
                                                </div>
                                            </div>
                                            <div class = 'row' style = 'margin-left:48%'>
                                                <div class = 'column'>
                                                    <a href = '/app_2/select_country' style='color:black'>Back to Menu</a>
                                                </div>
                                            </div>
                                    
                                    </body>
    
                                  ''', data = df.to_dict(orient='records'))

@app.route('/edit_exits_data_ie')

def edit_exits_data_ie():

    return render_template_string('''
                                     <!DOCTYPE html>
                                        <html>
                                            <head>
                                                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
                                            </head>
                                            <body>
                                                <div>
                                                    <div style = 'margin-left:2%;margin-top:2%'>
                                                        <img src="static/fgc-logo-1.png" alt="example" class="logo"/>
                                                    </div>
                                                </div>
                                                <div>
                                                    <form action='/app_2/edit_costs_ie' method="POST" name = 'form-one'> 
                                                        <div class = 'row' style = 'margin-top:10%;margin-left:40%; column-gap:5px'>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'date' id="date" name="exitdate" value={{date}} min="2021-01-01"  max="2022-12-31">
                                                            </div>
                                                            <div class='column'>
                                                                <button class="btn btn-dark" style = 'height:39px; width:150px;font-family:monospace' name = 'submit'>Submit</button>
                                                        </div>
                                                        </div>
                                                    </form>
                                                </div>
                                            
                                            
                                                <br></br>
                                        
                                                <div>
                                                    <form action = '/app_2/save_edits_ie' method="POST" name = 'form-second'> 
                                                        <div class = 'row' style = 'margin-top:2%;margin-left:15%; column-gap:5px'>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'date' id="date" name="date" value={{date}} min="2021-01-01"  max="2022-12-31">
                                                            </div>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'text' id = 'website', name = 'website', placeholder = 'Website' value = {{website}}>
                                                            </div>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'number' step = 'any' id = 'google', name = 'google', placeholder = 'Google' value = {{google}}>
                                                            </div>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'number' step = 'any' id = 'bing', name = 'bing', placeholder = 'Bing' value = {{bing}}>
                                                            </div>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'number' step = 'any' id = 'facebook', name = 'facebook', placeholder = 'Facebook' value = {{facebook}}>
                                                            </div>
                                                            <div class='column'>
                                                                <button class="btn btn-dark" style = 'height:39px; width:150px;font-family:monospace' name = 'edit'>Edit</button>
                                                            </div>
                                                        </div>
                                                    </form>
                                                </div>
                                                <br></br>
                                                   <div style = 'margin-left:45%'>
                                                      <a href = '/app_2' style="text-decoration:none;color:black">Click to Back</a>
                                                   </div>    
                                            </body>
                                        </html>
                                                                            
                                                                        ''')

@app.route('/edit_costs_ie', methods = ['GET', 'POST'])

def edit_costs_ie():

    acquistioncostdate = request.form.get('exitdate')

    #con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    sql = '''
             
                   SELECT 
                        DISTINCT CONVERT(DATE, AcquistionCostDate, 101) Date,
                        Website,
                        Google,
                        Bing,
                        Facebook
                FROM 
                        FG_Daily_Acquisition_Cost
                WHERE
                        AcquistionCostDate = '%(acquistioncostdate)s'
                        AND Website = 'IE'

          '''%{'acquistioncostdate': acquistioncostdate}

    df = pd.read_sql_query(sql, con)

    date = df['Date'].squeeze()

    website = df['Website'].squeeze()

    google = df['Google'].squeeze()

    bing = df['Bing'].squeeze()

    facebook = df['Facebook'].squeeze()

    return render_template_string('''
                                     <!DOCTYPE html>
                                        <html>
                                            <head>
                                                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
                                            </head>
                                            <body>
                                                <div>
                                                    <div style = 'margin-left:2%;margin-top:2%'>
                                                        <img src="static/fgc-logo-1.png" alt="example" class="logo"/>
                                                    </div>
                                                </div>
                                                <div>
                                                    <form action='/app_2/edit_costs_ie' method="POST" name = 'form-one'> 
                                                        <div class = 'row' style = 'margin-top:10%;margin-left:40%; column-gap:5px'>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'date' id="date" name="exitdate" value={{date}} min="2021-01-01"  max="2022-12-31">
                                                            </div>
                                                            <div class='column'>
                                                                <button class="btn btn-dark" style = 'height:39px; width:150px;font-family:monospace' name = 'submit'>Submit</button>
                                                        </div>
                                                        </div>
                                                    </form>
                                                </div>
                                            
                                            
                                                <br></br>
                                        
                                                <div>
                                                    <form action='/app_2/save_edits_ie' method="POST" name = 'form-second'> 
                                                        <div class = 'row' style = 'margin-top:2%;margin-left:15%; column-gap:5px'>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'date' id="date" name="date" value={{date}} min="2021-01-01"  max="2022-12-31">
                                                            </div>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'text' id = 'website', name = 'website', placeholder = 'Website' value = {{website}}>
                                                            </div>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'number' step = 'any' id = 'google', name = 'google', placeholder = 'Google' value = {{google}}>
                                                            </div>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'number' step = 'any' id = 'bing', name = 'bing', placeholder = 'Bing' value = {{bing}}>
                                                            </div>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'number' step = 'any' id = 'facebook', name = 'facebook', placeholder = 'Facebook' value = {{facebook}}>
                                                            </div>
                                                            <div class='column'>
                                                                <button class="btn btn-dark" style = 'height:39px; width:150px;font-family:monospace' name = 'edit'>Edit</button>
                                                            </div>
                                                        </div>
                                                    </form>
                                                </div> 
                                                <br></br>
                                                   <div style = 'margin-left:45%'>
                                                     <a href = '/app_2' style="text-decoration:none;color:black">Click to Back</a>
                                                   </div>   
                                            </body>
                                        </html>
                                                                        ''', date = date, website = website, google = google, bing = bing, facebook = facebook)

@app.route('/save_edits_ie', methods = ['GET','POST'])

def save_edits_ie():

    acquistioncostdate = request.form.get('date')
    
    website = request.form.get('website')

    google = request.form.get('google')

    bing = request.form.get('bing')

    facebook = request.form.get('facebook')

    adminuserid = session.get('admin_user_id')

    #con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    cur = con.cursor()

    cur.execute(" UPDATE FG_Daily_Acquisition_Cost SET Google = '%s', Bing = '%s', Facebook = '%s', AdminUserid = '%s' WHERE AcquistionCostDate = '%s' AND Website = '%s' "%(google, bing, facebook, adminuserid, acquistioncostdate, website)) 
                        
    con.commit()

    cur.close()

    #session.clear()

    #con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    sql = '''
                 SELECT 
                           DISTINCT CONVERT(DATE, AcquistionCostDate, 101) AcquistionCostDate,
                           Website,
                           Google ,
                           Bing,
                           Facebook
                     FROM
                          FG_Daily_Acquisition_Cost
                     WHERE 
                         AcquistionCostDate >= DATEADD(m, DATEDIFF(m, 0, GETDATE()), 0)  AND AcquistionCostDate <= DATEADD(m,DATEDIFF(m, -1, GETDATE()),-1)
                         AND Website = 'IE'
                ORDER BY
                        1 DESC
              '''

    df = pd.read_sql_query(sql, con)

    return render_template_string('''
                                <!DOCTYPE html>
                                <head>
                                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
                                </head>
                                <body> 
                                    <div style = 'margin-left:2%;margin-top:2%'>
                                        <img src="static/fgc-logo-1.png" alt="example" class="logo"/>
                                    </div>
                                    <div class = 'container' style = 'text-align: center; margin-top:5%'>
                                        {% block content %}
                                        <table class="table table-sm">
                                            <thead class="thead-dark">
                                                <tr>
                                                    <th scope="col">AcquistionCostDate</th>
                                                    <th scope="col">Website</th>
                                                    <th scope="col">Google</th>
                                                    <th scope="col">Bing</th>
                                                    <th scope="col">Facebook</th>
                                                </tr>
                                            </thead>
                                            <tbody style="overflow-y:scroll; height:100px;">
                                            {% for row in data %}
                                                <tr>
                                                    <td>{{row['AcquistionCostDate']}}</td>
                                                    <td>{{row['Website']}}</td>
                                                    <td>{{row['Google']}}</td>
                                                    <td>{{row['Bing']}}</td>
                                                    <td>{{row['Facebook']}}</td>
                                                </tr>
                                            {% endfor %}
                                            </tbody>
                                        </table>
                                        {% endblock %}
                                    </div>
                                    
                                        <div class = 'row' style = 'margin-left:44%; column-gap:1px'>
                                            <div class = 'column'>
                                                <a href = '/app_2/add_new_data_ie' class = 'btn btn-dark'>Click to Add</a>
                                            </div>
                                            <div class = 'column'>
                                                <a href = '/app_2/edit_exits_data_ie' class = 'btn btn-dark'>Click to Edit</a>
                                            </div>
                                        </div>
                                        <div class = 'row' style = 'margin-left:48%'>
                                            <div class = 'column'>
                                                <a href = '/app_2/select_country' style = 'color:black'>Back to Menu</a>
                                            </div>
                                        </div>
                                
                                </body>''', data = df.to_dict(orient='records'))

##############################FR##############################################

@app.route('/add_new_data_fr')

def add_new_data_fr():

    return render_template_string('''
                                     <!DOCTYPE html>
                                        <html>
                                            <head>
                                                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
                                            </head>
                                            <body>
                                                <div>
                                                    <div style = 'margin-left:2%;margin-top:2%'>
                                                        <img src="static/fgc-logo-1.png" alt="example" class="logo"/>
                                                    </div>
                                                </div>
                                                <div>
                                                    <form action = '/app_2/save_costs_fr' method="POST"> 
                                                    <div class = 'row' style = 'margin-top:10%;margin-left:15%; column-gap:5px'>
                                                        <div class = 'column'>
                                                            <input class="form-control" type = 'date' id="date" name="date" min="2021-01-01"  max="2022-12-31">
                                                        </div>
                                                        <div class = 'column'>
                                                            <input class="form-control" type = 'text' id = 'website', name = 'website', placeholder = 'FR' value = 'FR'>
                                                        </div>
                                                        <div class = 'column'>
                                                            <input class="form-control" type = 'number' step = 'any' id = 'google', name = 'google', placeholder = 'Google'>
                                                        </div>
                                                        <div class = 'column'>
                                                            <input class="form-control" type = 'number' step = 'any' id = 'bing', name = 'bing', placeholder = 'Bing'>
                                                        </div>
                                                        <div class = 'column'>
                                                            <input class="form-control" type = 'number' step = 'any' id = 'facebook', name = 'facebook', placeholder = 'Facebook'>
                                                        </div>
                                                        <div class='column'>
                                                            <button onclick="myFunction()" class="btn btn-dark" style = 'height:39px; width:150px;font-family:monospace'>Save</button>
                                                        </div>
                                                    </div>
                                                </div>
                                                <br></br>
                                                   <div style = 'margin-left:45%'>
                                                     <a href = '/app_2' style="text-decoration:none;color:black">Click to Back</a>
                                                   </div>
                                                <script>
                                                    function myFunction() {confirm("Are you confirm!");}
                                                </script>
                                            </body>
                                        </html>
                                ''') 

@app.route('/save_costs_fr' ,methods = ['GET','POST'])

def save_costs_fr():

    acquistioncostdate = request.form.get('date')

    website = request.form.get('website')

    google = request.form.get('google')

    bing = request.form.get('bing')

    facebook = request.form.get('facebook')

    adminuserid = session.get('admin_user_id')

    #con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    cur = con.cursor()

    cur.execute('''INSERT INTO FG_Daily_Acquisition_Cost(AcquistionCostDate, Website, Google, Bing,Facebook, AdminUserId) VALUES (%s,%s,%s,%s,%s,%s)''', 
                        (acquistioncostdate,website,google,bing,facebook,adminuserid))

    con.commit()

    cur.close()

    #con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    sql = '''
                     SELECT 
                           DISTINCT CONVERT(DATE, AcquistionCostDate, 101) AcquistionCostDate,
                           Website,
                           Google ,
                           Bing,
                           Facebook
                     FROM
                          FG_Daily_Acquisition_Cost
                     WHERE 
                         AcquistionCostDate >= DATEADD(m, DATEDIFF(m, 0, GETDATE()), 0)  AND AcquistionCostDate <= DATEADD(m,DATEDIFF(m, -1, GETDATE()),-1)
                         AND Website = 'FR'
                ORDER BY
                        1 DESC
                 
              '''

    df = pd.read_sql_query(sql, con)

    return render_template_string('''
                                     <!DOCTYPE html>
                                    <head>
                                        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
                                    </head>
                                    <body> 
                                        <div style = 'margin-left:2%;margin-top:2%'>
                                            <img src="static/fgc-logo-1.png" alt="example" class="logo"/>
                                        </div>
                                        <div class = 'container' style = 'text-align: center; margin-top:5%'>
                                            {% block content %}
                                            <table class="table table-sm">
                                                <thead class="thead-dark">
                                                    <tr>
                                                        <th scope="col">AcquistionCostDate</th>
                                                        <th scope="col">Website</th>
                                                        <th scope="col">Google</th>
                                                        <th scope="col">Bing</th>
                                                        <th scope="col">Facebook</th>
                                                    </tr>
                                                </thead>
                                                <tbody style="overflow-y:scroll; height:100px;">
                                                {% for row in data %}
                                                    <tr>
                                                        <td>{{row['AcquistionCostDate']}}</td>
                                                        <td>{{row['Website']}}</td>
                                                        <td>{{row['Google']}}</td>
                                                        <td>{{row['Bing']}}</td>
                                                        <td>{{row['Facebook']}}</td>
                                                    </tr>
                                                {% endfor %}
                                                </tbody>
                                            </table>
                                            {% endblock %}
                                        </div>
                                        
                                            <div class = 'row' style = 'margin-left:44%; column-gap:1px'>
                                                <div class = 'column'>
                                                    <a href = '/app_2/add_new_data_fr' class = 'btn btn-dark'>Click to Add</a>
                                                </div>
                                                <div class = 'column'>
                                                    <a href = '/app_2/edit_exits_data_fr' class = 'btn btn-dark'>Click to Edit</a>
                                                </div>
                                            </div>
                                            <div class = 'row' style = 'margin-left:48%'>
                                                <div class = 'column'>
                                                    <a href = '/app_2/select_country' style = 'color:black'>Back to Menu</a>
                                                </div>
                                            </div>
                                    
                                    </body>
    
                                  ''', data = df.to_dict(orient='records'))

@app.route('/edit_exits_data_fr')

def edit_exits_data_fr():

    return render_template_string('''
                                     <!DOCTYPE html>
                                        <html>
                                            <head>
                                                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
                                            </head>
                                            <body>
                                                <div>
                                                    <div style = 'margin-left:2%;margin-top:2%'>
                                                        <img src="static/fgc-logo-1.png" alt="example" class="logo"/>
                                                    </div>
                                                </div>
                                                <div>
                                                    <form action='/app_2/edit_costs_fr' method="POST" name = 'form-one'> 
                                                        <div class = 'row' style = 'margin-top:10%;margin-left:40%; column-gap:5px'>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'date' id="date" name="exitdate" value={{date}} min="2021-01-01"  max="2022-12-31">
                                                            </div>
                                                            <div class='column'>
                                                                <button class="btn btn-dark" style = 'height:39px; width:150px;font-family:monospace' name = 'submit'>Submit</button>
                                                        </div>
                                                        </div>
                                                    </form>
                                                </div>
                                            
                                            
                                                <br></br>
                                        
                                                <div>
                                                    <form action = '/app_2/save_edits_fr' method="POST" name = 'form-second'> 
                                                        <div class = 'row' style = 'margin-top:2%;margin-left:15%; column-gap:5px'>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'date' id="date" name="date" value={{date}} min="2021-01-01"  max="2022-12-31">
                                                            </div>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'text' id = 'website', name = 'website', placeholder = 'Website' value = {{website}}>
                                                            </div>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'number' step = 'any' id = 'google', name = 'google', placeholder = 'Google' value = {{google}}>
                                                            </div>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'number' step = 'any' id = 'bing', name = 'bing', placeholder = 'Bing' value = {{bing}}>
                                                            </div>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'number' step = 'any' id = 'facebook', name = 'facebook', placeholder = 'Facebook' value = {{facebook}}>
                                                            </div>
                                                            <div class='column'>
                                                                <button class="btn btn-dark" style = 'height:39px; width:150px;font-family:monospace' name = 'edit'>Edit</button>
                                                            </div>
                                                        </div>
                                                    </form>
                                                </div> 
                                                <br></br>
                                                   <div style = 'margin-left:45%'>
                                                     <a href = '/app_2' style="text-decoration:none;color:black">Click to Back</a>
                                                   </div>   
                                            </body>
                                        </html>
                                                                            
                                                                        ''')

@app.route('/edit_costs_fr', methods = ['GET', 'POST'])

def edit_costs_fr():

    acquistioncostdate = request.form.get('exitdate')

    #con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    sql = '''
             
                   SELECT 
                        DISTINCT CONVERT(DATE, AcquistionCostDate, 101) Date,
                        Website,
                        Google,
                        Bing,
                        Facebook
                FROM 
                        FG_Daily_Acquisition_Cost
                WHERE
                        AcquistionCostDate = '%(acquistioncostdate)s'
                        AND Website = 'FR'

          '''%{'acquistioncostdate': acquistioncostdate}

    df = pd.read_sql_query(sql, con)

    date = df['Date'].squeeze()

    website = df['Website'].squeeze()

    google = df['Google'].squeeze()

    bing = df['Bing'].squeeze()

    facebook = df['Facebook'].squeeze()

    return render_template_string('''
                                     <!DOCTYPE html>
                                        <html>
                                            <head>
                                                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
                                            </head>
                                            <body>
                                                <div>
                                                    <div style = 'margin-left:2%;margin-top:2%'>
                                                        <img src="static/fgc-logo-1.png" alt="example" class="logo"/>
                                                    </div>
                                                </div>
                                                <div>
                                                    <form action='/app_2/edit_costs_fr' method="POST" name = 'form-one'> 
                                                        <div class = 'row' style = 'margin-top:10%;margin-left:40%; column-gap:5px'>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'date' id="date" name="exitdate" value={{date}} min="2021-01-01"  max="2022-12-31">
                                                            </div>
                                                            <div class='column'>
                                                                <button class="btn btn-dark" style = 'height:39px; width:150px;font-family:monospace' name = 'submit'>Submit</button>
                                                        </div>
                                                        </div>
                                                    </form>
                                                </div>
                                            
                                            
                                                <br></br>
                                        
                                                <div>
                                                    <form action='/app_2/save_edits_fr' method="POST" name = 'form-second'> 
                                                        <div class = 'row' style = 'margin-top:2%;margin-left:15%; column-gap:5px'>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'date' id="date" name="date" value={{date}} min="2021-01-01"  max="2022-12-31">
                                                            </div>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'text' id = 'website', name = 'website', placeholder = 'Website' value = {{website}}>
                                                            </div>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'number' step = 'any' id = 'google', name = 'google', placeholder = 'Google' value = {{google}}>
                                                            </div>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'number' step = 'any' id = 'bing', name = 'bing', placeholder = 'Bing' value = {{bing}}>
                                                            </div>
                                                            <div class = 'column'>
                                                                <input class="form-control" type = 'number' step = 'any' id = 'facebook', name = 'facebook', placeholder = 'Facebook' value = {{facebook}}>
                                                            </div>
                                                            <div class='column'>
                                                                <button class="btn btn-dark" style = 'height:39px; width:150px;font-family:monospace' name = 'edit'>Edit</button>
                                                            </div>
                                                        </div>
                                                    </form>
                                                </div> 
                                                <br></br>
                                                   <div style = 'margin-left:45%'>
                                                     <a href = '/app_2' style="text-decoration:none;color:black">Click to Back</a>
                                                   </div>   
                                            </body>
                                        </html>
                                                                        ''', date = date, website = website, google = google, bing = bing, facebook = facebook)

@app.route('/save_edits_fr', methods = ['GET','POST'])

def save_edits_fr():

    acquistioncostdate = request.form.get('date')
    
    website = request.form.get('website')

    google = request.form.get('google')

    bing = request.form.get('bing')

    facebook = request.form.get('facebook')

    adminuserid = session.get('admin_user_id')

    #con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    cur = con.cursor()

    cur.execute(" UPDATE FG_Daily_Acquisition_Cost SET Google = '%s', Bing = '%s', Facebook = '%s', AdminUserid = '%s' WHERE AcquistionCostDate = '%s' AND Website = '%s'"%(google, bing, facebook, adminuserid, acquistioncostdate, website)) 
                        
    con.commit()

    cur.close()

    #session.clear()

    #con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    sql = '''
                 SELECT 
                           DISTINCT CONVERT(DATE, AcquistionCostDate, 101) AcquistionCostDate,
                           Website,
                           Google ,
                           Bing,
                           Facebook
                     FROM
                          FG_Daily_Acquisition_Cost
                     WHERE 
                         AcquistionCostDate >= DATEADD(m, DATEDIFF(m, 0, GETDATE()), 0)  AND AcquistionCostDate <= DATEADD(m,DATEDIFF(m, -1, GETDATE()),-1)
                         AND Website = 'FR'
                ORDER BY
                        1 DESC
              '''

    df = pd.read_sql_query(sql, con)

    return render_template_string('''
                                <!DOCTYPE html>
                                <head>
                                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
                                </head>
                                <body> 
                                    <div style = 'margin-left:2%;margin-top:2%'>
                                        <img src="static/fgc-logo-1.png" alt="example" class="logo"/>
                                    </div>
                                    <div class = 'container' style = 'text-align: center; margin-top:5%'>
                                        {% block content %}
                                        <table class="table table-sm">
                                            <thead class="thead-dark">
                                                <tr>
                                                    <th scope="col">AcquistionCostDate</th>
                                                    <th scope="col">Website</th>
                                                    <th scope="col">Google</th>
                                                    <th scope="col">Bing</th>
                                                    <th scope="col">Facebook</th>
                                                </tr>
                                            </thead>
                                            <tbody style="overflow-y:scroll; height:100px;">
                                            {% for row in data %}
                                                <tr>
                                                    <td>{{row['AcquistionCostDate']}}</td>
                                                    <td>{{row['Website']}}</td>
                                                    <td>{{row['Google']}}</td>
                                                    <td>{{row['Bing']}}</td>
                                                    <td>{{row['Facebook']}}</td>
                                                </tr>
                                            {% endfor %}
                                            </tbody>
                                        </table>
                                        {% endblock %}
                                    </div>
                                    
                                        <div class = 'row' style = 'margin-left:44%; column-gap:1px'>
                                            <div class = 'column'>
                                                <a href = '/app_2/add_new_data_fr' class = 'btn btn-dark'>Click to Add</a>
                                            </div>
                                            <div class = 'column'>
                                                <a href = '/app_2/edit_exits_data_fr' class = 'btn btn-dark'>Click to Edit</a>
                                            </div>
                                        </div>
                                        <div class = 'row' style = 'margin-left:48%'>
                                            <div class = 'column'>
                                                <a href = '/app_2/select_country' style = 'color:black'>Back to Menu</a>
                                            </div>
                                        </div>
                                
                                </body>''', data = df.to_dict(orient='records'))

