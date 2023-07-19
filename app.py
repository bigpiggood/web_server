from flask import Flask , render_template , request, redirect, session
from data import Articles
from mysql import Mysql
import config
# print(Articles())
import pymysql



app = Flask(__name__)

mysql = Mysql(password=config.PASSWORD)
app.secret_key = 'eungok'





@app.route('/', methods=['GET', 'POST'])
def index():
    # if request.method == 'GET':
    #     os_info = dict(request.headers)
    #     # req_data = request.get_json()
    #     print(os_info)
    #     name = request.args.get("name")
    #     print(name)
    #     hello = request.args.get("hello")
    #     print(hello)
    #     return render_template('index.html', header=f'{name}님 {hello}!!')

    # elif request.method == 'POST':
    #     data = request.form.get("name")
    #     data_2 = request.form["hello"]
    #     print(data_2)
        return render_template('index.html')

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == "GET":
        return render_template('hello.html')

    elif request.method == 'POST':
        name = request.form['name']
        hello = request.form['hello']
        print(hello)
        return render_template('index.html', name=name, hello=hello)


@app.route('/list', methods=['GET', 'POST'])
def list():
    data = Articles()
    return render_template('list.html', data=data) 


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
       username = request.form['username']
       email = request.form['email']  
       phone = request.form['phone']  
       password = request.form['password']  
       print(username, email, phone, password)    
    #  print(result)

       db = pymysql.connect(host=mysql.host, user=mysql.user, db=mysql.db, password=mysql.password, charset=mysql.charset)
       curs = db.cursor()

       sql = f'SELECT * FROM user WHERE email = %s'
       curs.execute(sql, email)

       rows = curs.fetchall()  
       print(rows) 
       if rows:
           return render_template('register.html', data=1)
       else:
          result = mysql.insert_user(username, email, phone, password) 
          print(result)
          return redirect('/login')

    elif request.method == 'GET':
        return render_template('register.html',data=0)

@app.route('/login',  methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
        email = request.form.get('email')  
        password = request.form.get('password') 

        db = pymysql.connect(host=mysql.host, user=mysql.user, db=mysql.db, password=mysql.password, charset=mysql.charset)
        curs = db.cursor()
        
        sql = f'SELECT * FROM user WHERE email = %s'
        curs.execute(sql, email)

        rows = curs.fetchall()  
        print(rows) 
        
        if rows:
            result = mysql.verify_password(password, rows[0][4])
            if result:
                session['is_loged_in'] = True
                session['username'] = rows[0][1]
                return redirect('/')
            else:
                return redirect('/login')
        else:
            return render_template('login.html')      

if __name__=='__main__':
    app.run(debug=True)