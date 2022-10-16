from flask import Flask, render_template, request, session
import pymssql
import pandas as pd

app = Flask(__name__, template_folder = 'template', static_folder = 'static')

app.secret_key = "feelgoodcontact"

@app.route('/')

def index():

    return render_template('login.html')

@app.route('/show', methods = ['GET','POST'])

def show():

    username = request.form.get('username')

    password = request.form.get('password')

    con_0 = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

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
                    a.Email = '%(username)s'
                    AND b.Password = '%(password)s'
                    AND a.Enable = 1
          '''%{'username': username,'password':password}

    df_0 = pd.read_sql_query(sql_0, con_0)

    adminuserid = df_0['AdminUserId'].squeeze()

    session['admin_user_id'] = str(adminuserid)

    if df_0.empty is True:

        return render_template('relogin.html')

    else:

        con_1 = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

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

        return render_template("show.html", data = df_1.to_dict(orient='records'))
             
@app.route('/add_new_data')

def add_new_data():

    return render_template('add_costs.html')

@app.route('/save_costs' ,methods = ['GET','POST'])

def save_costs():

    labourcostdate = request.form.get('date')

    pickpack = request.form.get('pickandpack')

    stock = request.form.get('stock')

    holidaypaid = request.form.get('holidaypaid')

    management = request.form.get('management')

    adminuserid = session.get('admin_user_id')

    con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    cur = con.cursor()

    cur.execute('''INSERT INTO Fg_Daily_Labour_Costs(LabourCostDate, PickPack, Stock, HolidayPaid, Management, AdminUserid) VALUES (%s,%s,%s,%s,%s,%s)''', 
                        (labourcostdate, pickpack, stock, holidaypaid, management, adminuserid))

    con.commit()

    cur.close()

    con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

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

    return render_template("show.html", data = df.to_dict(orient='records'))

@app.route('/edit_exits_data')

def edit_exits_data():

    return render_template('edit_costs.html')

@app.route('/edit_costs', methods = ['GET', 'POST'])

def edit_costs():

    labourcostdate = request.form.get('exitdate')

    con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

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

    return render_template('edit_costs.html', date = date, pickpack = pickpack, stock = stock, holidaypaid = holidaypaid, management = management)

@app.route('/save_edits', methods = ['GET','POST'])

def save_edits():

    labourcostdate = request.form.get('date')
    
    pickpack = request.form.get('pickandpack')

    stock = request.form.get('stock')

    holidaypaid = request.form.get('holidaypaid')

    management = request.form.get('management')

    adminuserid = session.get('admin_user_id')

    con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

    cur = con.cursor()

    cur.execute(" UPDATE Fg_Daily_Labour_Costs SET pickpack = '%s', stock = '%s', holidaypaid = '%s', management = '%s', AdminUserid = '%s' WHERE labourcostdate = '%s' "%(pickpack, stock, holidaypaid, management, adminuserid, labourcostdate)) 
                        
    con.commit()

    cur.close()

    con = pymssql.connect(host = r'217.174.248.77', port = 3689, user = r'DevUser3', password = r'flgT!9585', database = r'feelgood.live')

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

    return render_template("show.html", data = df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug = True)