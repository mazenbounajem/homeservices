from flask import Flask,render_template,request, session#session
#from flask_session import Session
import mysql.connector

import pyodbc

app = Flask(__name__)
app.config["SESSION_PERMANENT"]= False
app.config["SESSION_TYPE"]= "filesystem"
app.config['SECRET_KEY'] = 'super secret key'

def connection():
    s = 'DESKTOP-Q7U1STD' #Your server name 
    d = 'Services' 
    u = 'sa' #Your login
    p = 'nit2011' #Your login password
    cstr = 'DRIVER={ODBC Driver 11 for SQL Server};SERVER='+s+';DATABASE='+d+';UID='+u+';PWD='+ p
    conn = pyodbc.connect(cstr)
    return conn
@app.route("/",methods=["GET","POST"])
def index():
    conn=connection()
    cursor = conn.cursor()
    if request.method== 'GET':
        return render_template('index.html')
    if request.method== 'POST':
        name=request.form['name']
        email=request.form['tel']
        phone=request.form['email']
        profession=request.form['profession']
        print(name,email,phone,profession)
        cursor.execute("INSERT INTO dbo.Profession(Name,Phone,Email,Profession) VALUES (?, ?,?, ?)",  name,email,phone,profession)
        conn.commit()
        conn.close()
        return render_template('index.html')


    
def connect():
    # Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
    server = 'DESKTOP-Q7U1STD' 
    database = 'Services' 
    username = 'sa' 
    password = 'nit2011' 
    # ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
    cursor = connection.cursor()
    return cursor

@app.route("/")
def about():
    return render_template('about.html')

@app.route("/")
def services():
    return render_template('services.html')
@app.route("/")
def contacts():
    return render_template('index.html')

@app.route("/signup", methods=["GET","POST"])
def signup():
    
    checksignup=[]
    conn = connection()
    cursor = conn.cursor()
    if request.method == 'GET':  
        return render_template("signup.html",message='NULL')

    if request.method == 'POST':
        name = request.form["name"]
        lastName = request.form["lastName"]
        phoneNumber = request.form["phoneNumber"]
        email=request.form["email"]
        password =request.form["password"]
        Gender=request.form["Gender"]
        try:
            cursor.execute('SELECT Email from Users Where Email=?',email)
            result=cursor.fetchone()
            print(result[0])
            if result[0]==email:
                return render_template("signup.html",message="Email already in use")
        except TypeError as e:
            print(e)
      #  finally:    
            cursor.execute("INSERT INTO dbo.Users(Name,Email,Password,PhoneNumber,Latitude,Longitude,FamilyName,Gender) VALUES (?, ?,?, ?,?,?,?,?)",  name,email,password,phoneNumber,'NULL','NULL',lastName,Gender)
            cursor.execute('SELECT Email,password,name from Users Where Email=? And password=?',email,password)
            result=cursor.fetchone()
            print(result[0])
            if result[0]== email and result[1]== password:
                session['username'] = result[2]
                return render_template("index.html",message=session['username'],logout='logout')



@app.route("/login", methods=["GET","POST"])
def login():
     

     conn = connection()
     cursor = conn.cursor()
     if request.method == 'GET':  
         return render_template('login.html')
     if request.method== 'POST':
         email=request.form["email"]
         password=request.form["password"]
         print(email,password)
         try:
            cursor.execute('SELECT Email,password,name from Users Where Email=? And password=?',email,password)
            result=cursor.fetchone()
            print(result[0])
            if result[0]== email and result[1]== password:
                session['username'] = result[2]
                return render_template("index.html",message=session['username'],logout='logout')
         except TypeError as e:
            print(e)
            return render_template('login.html',message="invalid email or password")
#logout for the session
@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return render_template("index.html")         