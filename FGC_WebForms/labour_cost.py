from flask import Flask, render_template, request, session, render_template_string
import pymssql
import pandas as pd

app = Flask(__name__, template_folder = 'template', static_folder = 'static')

app.secret_key = "feelgoodcontact"

@app.route('/')

def index():

    return render_template_string('''
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
                                                        <form action = "/app_1/show" method = 'POST'>
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

        #return render_template('relogin.html')

        return render_template_string(
                                        '''
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

        #con_1 = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

        con_1 = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

        sql_1 = '''
                 SELECT 
                        DISTINCT CONVERT(DATE, LabourCostDate, 101) Date,
                        PickPack,
                        Stock,
                        HolidayPaid,
                        Management
                FROM 
                        Fg_Daily_Labour_Costs
                WHERE
                        LabourCostDate >= DATEADD(m, DATEDIFF(m, 0, GETDATE()), 0)  AND LabourCostDate <= DATEADD(m,DATEDIFF(m, -1, GETDATE()),-1)
                 
                ORDER BY
                        1 DESC
              '''

        df_1 = pd.read_sql_query(sql_1, con_1)

        #return render_template("show.html", data = df_1.to_dict(orient='records'))

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
                                                                    <th scope="col">Date</th>
                                                                    <th scope="col">PICK AND PACK</th>
                                                                    <th scope="col">STOCK</th>
                                                                    <th scope="col">HOLIDAY PAID</th>
                                                                    <th scope="col">MANAGEMENT</th>
                                                                </tr>
                                                            </thead>
                                                            <tbody style="overflow-y:scroll; height:100px;">
                                                            {% for row in data %}
                                                                <tr>
                                                                    <td>{{row['Date']}}</td>
                                                                    <td>{{row['PickPack']}}</td>
                                                                    <td>{{row['Stock']}}</td>
                                                                    <td>{{row['HolidayPaid']}}</td>
                                                                    <td>{{row['Management']}}</td>
                                                                </tr>
                                                            {% endfor %}
                                                            </tbody>
                                                        </table>
                                                        {% endblock %}
                                                    </div>
                                                    <div class = 'row' style = 'margin-left:40%; column-gap:1px'>
                                                            <div class = 'column'>
                                                                <a href = '/app_1/add_new_data' class = 'btn btn-dark'>Click to Add</a>
                                                            </div>
                                                            <div class = 'column'>
                                                                <a href = '/app_1/edit_exits_data' class = 'btn btn-dark'>Click to Edit</a>
                                                            </div>
                                                    </div> 
                                                    <!--<br></br>-->
                                                    <div style = 'margin-left:45%'>
                                                       <a href = '/app_1' style="text-decoration:none; color:black">Click to Back</a>
                                                    </div>                  
                                                </body>
                                            ''', data = df_1.to_dict(orient='records'))

@app.route('/add_new_data')

def add_new_data():

    return render_template_string(
                                  '''<!DOCTYPE html>
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
                                                <form action= '/app_1/save_costs' method="POST"> 
                                                <div class = 'row' style = 'margin-top:10%;margin-left:15%; column-gap:5px'>
                                                    <div class = 'column'>
                                                        <input class="form-control" type = 'date' id="date" name="date" value={{date}} min="2021-01-01"  max="2022-12-31">
                                                    </div>
                                                    <div class = 'column'>
                                                        <input class="form-control" type = 'number' step = 'any' id = 'pick&pack', name = 'pickandpack', placeholder = 'Pick & Pack' value = {{pickpack}}>
                                                    </div>
                                                    <div class = 'column'>
                                                        <input class="form-control" type = 'number' step = 'any' id = 'stock', name = 'stock', placeholder = 'Stock' value = {{stock}}>
                                                    </div>
                                                    <div class = 'column'>
                                                        <input class="form-control" type = 'number' step = 'any' id = 'holidaypaid', name = 'holidaypaid', placeholder = 'Holiday Paid' value = {{holidaypaid}}>
                                                    </div>
                                                    <div class = 'column'>
                                                        <input class="form-control" type = 'number' step = 'any' id = 'management', name = 'management', placeholder = 'Management' value = {{management}}>
                                                    </div>
                                                    <div class='column'>
                                                        <button onclick="myFunction()" class="btn btn-dark" style = 'height:39px; width:150px;font-family:monospace'>Save</button>
                                                    </div>
                                                </div>
                                            </div>
                                            <br></br>
                                            <div style = 'margin-left:45%'>
                                               <a href = '/app_1' style="text-decoration:none;color:black">Click to Back</a>
                                            </div>
                                            <script>
                                                function myFunction() {confirm("Are you confirm!");}
                                            </script>
                                        </body>
                                    </html>
                                 '''
                                 )

@app.route('/save_costs' ,methods = ['GET','POST'])

def save_costs():

    labourcostdate = request.form.get('date')

    pickpack = request.form.get('pickandpack')

    stock = request.form.get('stock')

    holidaypaid = request.form.get('holidaypaid')

    management = request.form.get('management')

    adminuserid = session.get('admin_user_id')

    #con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    cur = con.cursor()

    cur.execute('''INSERT INTO Fg_Daily_Labour_Costs(LabourCostDate, PickPack, Stock, HolidayPaid, Management, AdminUserid) VALUES (%s,%s,%s,%s,%s,%s)''', 
                        (labourcostdate, pickpack, stock, holidaypaid, management, adminuserid))

    con.commit()

    cur.close()

    #con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    sql = '''
                 SELECT 
                        DISTINCT CONVERT(DATE, LabourCostDate, 101) Date,
                        PickPack,
                        Stock,
                        HolidayPaid,
                        Management
                FROM 
                        Fg_Daily_Labour_Costs
                WHERE
                        LabourCostDate >= DATEADD(m, DATEDIFF(m, 0, GETDATE()), 0)  AND LabourCostDate <= DATEADD(m,DATEDIFF(m, -1, GETDATE()),-1)

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
                                                            <th scope="col">Date</th>
                                                            <th scope="col">PICK AND PACK</th>
                                                            <th scope="col">STOCK</th>
                                                            <th scope="col">HOLIDAY PAID</th>
                                                            <th scope="col">MANAGEMENT</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody style="overflow-y:scroll; height:100px;">
                                                    {% for row in data %}
                                                        <tr>
                                                            <td>{{row['Date']}}</td>
                                                            <td>{{row['PickPack']}}</td>
                                                            <td>{{row['Stock']}}</td>
                                                            <td>{{row['HolidayPaid']}}</td>
                                                            <td>{{row['Management']}}</td>
                                                        </tr>
                                                    {% endfor %}
                                                    </tbody>
                                                </table>
                                                {% endblock %}
                                            </div>
                                            <div class = 'row' style = 'margin-left:40%; column-gap:1px'>
                                                    <div class = 'column'>
                                                        <a href = '/app_1/add_new_data' class = 'btn btn-dark'>Click to Add</a>
                                                    </div>
                                                    <div class = 'column'>
                                                        <a href = '/app_1/edit_exits_data' class = 'btn btn-dark'>Click to Edit</a>
                                                    </div>
                                            </div> 
                                            <!--<br></br>-->
                                            <div style = 'margin-left:45%'>
                                               <a href = '/app_1' style="text-decoration:none;color:black">Click to Back</a>
                                            </div>                  
                                        </body>
                                    ''', data = df.to_dict(orient='records'))

@app.route('/edit_exits_data')

def edit_exits_data():

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
                                                            <form action = '/app_1/edit_costs' method="POST" name = 'form-one'> 
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
                                                            <form action= '/app_1/save_edits' method="POST" name = 'form-second'> 
                                                                <div class = 'row' style = 'margin-top:2%;margin-left:15%; column-gap:5px'>
                                                                    <div class = 'column'>
                                                                        <input class="form-control" type = 'date' id="date" name="date" value={{date}} min="2021-01-01"  max="2022-12-31">
                                                                    </div>
                                                                    <div class = 'column'>
                                                                        <input class="form-control" type = 'number' step = 'any' id = 'pick&pack', name = 'pickandpack', placeholder = 'Pick & Pack' value = {{pickpack}}>
                                                                    </div>
                                                                    <div class = 'column'>
                                                                        <input class="form-control" type = 'number' step = 'any' id = 'stock', name = 'stock', placeholder = 'Stock' value = {{stock}}>
                                                                    </div>
                                                                    <div class = 'column'>
                                                                        <input class="form-control" type = 'number' step = 'any' id = 'holidaypaid', name = 'holidaypaid', placeholder = 'Holiday Paid' value = {{holidaypaid}}>
                                                                    </div>
                                                                    <div class = 'column'>
                                                                        <input class="form-control" type = 'number' step = 'any' id = 'management', name = 'management', placeholder = 'Management' value = {{management}}>
                                                                    </div>
                                                                    <div class='column'>
                                                                        <button class="btn btn-dark" style = 'height:39px; width:150px;font-family:monospace' name = 'edit'>Edit</button>
                                                                    </div>
                                                                </div>
                                                            </form>
                                                        </div> 
                                                        <br></br>
                                                        <div style = 'margin-left:45%'>
                                                           <a href = '/app_1' style="text-decoration:none;color:black">Click to Back</a>
                                                        </div>  
                                                    </body>
                                                </html>
                                                    
                                                    ''')

@app.route('/edit_costs', methods = ['GET', 'POST'])

def edit_costs():

    labourcostdate = request.form.get('exitdate')

    #con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    sql = '''
             
                   SELECT 
                        DISTINCT CONVERT(DATE, LabourCostDate, 101) Date,
                        PickPack,
                        Stock,
                        HolidayPaid,
                        Management
                FROM 
                        Fg_Daily_Labour_Costs
                WHERE
                        LabourCostDate = '%(labourcostdate)s'

          '''%{'labourcostdate': labourcostdate}

    df = pd.read_sql_query(sql, con)

    date = df['Date'].squeeze()

    pickpack = df['PickPack'].squeeze()

    stock = df['Stock'].squeeze()

    holidaypaid = df['HolidayPaid'].squeeze()

    management = df['Management'].squeeze()

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
                                                <form action = '/app_1/edit_costs' method="POST" name = 'form-one'> 
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
                                                <form action = '/app_1/save_edits' method="POST" name = 'form-second'> 
                                                    <div class = 'row' style = 'margin-top:2%;margin-left:15%; column-gap:5px'>
                                                        <div class = 'column'>
                                                            <input class="form-control" type = 'date' id="date" name="date" value={{date}} min="2021-01-01"  max="2022-12-31">
                                                        </div>
                                                        <div class = 'column'>
                                                            <input class="form-control" type = 'number' step = 'any' id = 'pick&pack', name = 'pickandpack', placeholder = 'Pick & Pack' value = {{pickpack}}>
                                                        </div>
                                                        <div class = 'column'>
                                                            <input class="form-control" type = 'number' step = 'any' id = 'stock', name = 'stock', placeholder = 'Stock' value = {{stock}}>
                                                        </div>
                                                        <div class = 'column'>
                                                            <input class="form-control" type = 'number' step = 'any' id = 'holidaypaid', name = 'holidaypaid', placeholder = 'Holiday Paid' value = {{holidaypaid}}>
                                                        </div>
                                                        <div class = 'column'>
                                                            <input class="form-control" type = 'number' step = 'any' id = 'management', name = 'management', placeholder = 'Management' value = {{management}}>
                                                        </div>
                                                        <div class='column'>
                                                            <button class="btn btn-dark" style = 'height:39px; width:150px;font-family:monospace' name = 'edit'>Edit</button>
                                                        </div>
                                                    </div>
                                                </form>
                                            </div> 
                                            <br></br>
                                            <div style = 'margin-left:45%'>
                                               <a href = '/app_1' style="text-decoration:none;color:black">Click to Back</a>
                                            </div>  
                                        </body>
                                    </html>
    
                                  ''', date = date, pickpack = pickpack, stock = stock, holidaypaid = holidaypaid, management = management)

@app.route('/save_edits', methods = ['GET','POST'])

def save_edits():

    labourcostdate = request.form.get('date')
    
    pickpack = request.form.get('pickandpack')

    stock = request.form.get('stock')

    holidaypaid = request.form.get('holidaypaid')

    management = request.form.get('management')

    adminuserid = session.get('admin_user_id')

    #con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    cur = con.cursor()

    cur.execute(" UPDATE Fg_Daily_Labour_Costs SET pickpack = '%s', stock = '%s', holidaypaid = '%s', management = '%s', AdminUserid = '%s' WHERE labourcostdate = '%s' "%(pickpack, stock, holidaypaid, management, adminuserid, labourcostdate)) 
                        
    con.commit()

    cur.close()

    #con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    con = pymssql.connect(host = r'217.174.248.81', port = 49559, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    sql = '''
                 SELECT 
                        DISTINCT CONVERT(DATE, LabourCostDate, 101) Date,
                        PickPack,
                        Stock,
                        HolidayPaid,
                        Management
                FROM 
                        Fg_Daily_Labour_Costs
                WHERE
                        LabourCostDate >= DATEADD(m, DATEDIFF(m, 0, GETDATE()), 0)  AND LabourCostDate <= DATEADD(m,DATEDIFF(m, -1, GETDATE()),-1)
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
                                                            <th scope="col">Date</th>
                                                            <th scope="col">PICK AND PACK</th>
                                                            <th scope="col">STOCK</th>
                                                            <th scope="col">HOLIDAY PAID</th>
                                                            <th scope="col">MANAGEMENT</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody style="overflow-y:scroll; height:100px;">
                                                    {% for row in data %}
                                                        <tr>
                                                            <td>{{row['Date']}}</td>
                                                            <td>{{row['PickPack']}}</td>
                                                            <td>{{row['Stock']}}</td>
                                                            <td>{{row['HolidayPaid']}}</td>
                                                            <td>{{row['Management']}}</td>
                                                        </tr>
                                                    {% endfor %}
                                                    </tbody>
                                                </table>
                                                {% endblock %}
                                            </div>
                                              <div class = 'row' style = 'margin-left:40%; column-gap:1px'>
                                                    <div class = 'column'>
                                                        <a href = "{{url_for('add_new_data')}}" class = 'btn btn-dark'>Click to Add</a>
                                                    </div>
                                                    <div class = 'column'>
                                                        <a href = "{{url_for('edit_exits_data')}}" class = 'btn btn-dark'>Click to Edit</a>
                                                    </div>
                                            </div>
                                            <!--<br></br>-->
                                            <div style = 'margin-left:45%'>
                                                <a href = '/app_1' style="text-decoration:none;color:black">Click to Back</a>
                                            </div>
                                        
                                        </body>
                                                                        ''', data = df.to_dict(orient='records'))





