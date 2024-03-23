from flask import Flask, render_template, request, redirect, url_for, flash

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from important import path, login, secret
from sqlalchemy import create_engine

from flask import Flask
from flask_bcrypt import Bcrypt
import pandas as pd
import time
from password import db_connection, cursor, insert_data, insert_data2
from important import path, secret, login







import mysql.connector
app = Flask(__name__, static_url_path='/static')
bcrypt = Bcrypt(app)



print('User added successfully.')
app.config['SQLALCHEMY_DATABASE_URI'] = path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secret 
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = login
db1 = 'mysql://abdullah:abdullah3539##@localhost/year2023'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), unique= True, nullable=False)
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        try:
            return bcrypt.check_password_hash(self.password, password)
        except ValueError:
            return False

def create_app():
    return app







# Callback to reload user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Function to insert a user into the database
def insert_user(username, password):
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()





@app.route('/register3539', methods=['GET', 'POST'])

def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if the passwords match
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))

        # Check if the username is already taken
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username is already taken', 'danger')
            return redirect(url_for('register'))

        # Create a new user and add to the database
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login1'))

    return render_template('register.html') 

     

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login1():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('get_values'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/login2', methods=['GET', 'POST'])

def login2():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login2.html')









  

@app.route('/insert_data2', methods=['POST'])
def insert_data_route1():
    procedurename = request.form['procedurename']
    

    # Create a table if it doesn't exist
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS proceduretable (
            procedurename VARCHAR(500)
        );
    """)
    time.sleep(2)

    insert_data2(procedurename)

    return redirect('/admin')

@app.route('/admin' , methods=['GET','POST'])
def get():
    query = "SELECT * FROM proceduretable"
    cursor.execute(query)
    rows = cursor.fetchall()
    return render_template('admin.html', rows=rows)
    

@app.route('/data', methods=['GET', 'POST'])
def index():
    month_name = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
  
    day_name = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    
    
    query = "SELECT * FROM proceduretable"
    cursor.execute(query)
    rows = cursor.fetchall()
    columnname = [desc[0] for desc in cursor.description]
    procedure_name = [dict(zip(columnname, row))['procedurename'] for row in rows]


    return render_template('index.html', month_name=month_name, day_name=day_name, procedure_name=procedure_name)

@app.route('/insert_data', methods=['POST'])
def insert_data_route():
    month = request.form['month']
    name = request.form['name']
    procedure_type = request.form['procedure_type']
    amount = request.form['amount']
    day = request.form['day']

    # Create a table if it doesn't exist
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {month} (
            no INT auto_increment primary key,
            name VARCHAR(500),
            procedure_type VARCHAR(500),
            amount INT,
            day VARCHAR(500)
        )
    """)
    time.sleep(1)

    insert_data(month, name, procedure_type, amount, day)

    return redirect('/data')
@app.route('/get_special', methods=['GET', 'POST'])
def get_special():
    
    month_name = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    if request.method == 'POST':
        month = request.form["month"]
        database = request.form['database']
        query = "SELECT {}, day FROM {}".format(database, month)
        query2 = "SELECT AVG(amount) FROM {}".format(month)
        cursor.execute(query)
        
        rows = cursor.fetchall()
        cursor.execute(query2)
        row = cursor.fetchall()
        r1 = str(row)
        r1 = r1[11:20]
        engine = create_engine(db1)
        query3 = 'SELECT * FROM March'
        data = pd.read_sql_query(query3, engine)
        analysis = data.describe()
        

        return render_template('display.html', rows=rows, r1=r1, database=database, analysis=analysis)
    return render_template('getvalue.html', month_name=month_name)


@app.route('/get_values', methods=['GET', 'POST'])
def get_values():
    
    month_name = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    

    try:    
        if request.method == 'POST':
            month = request.form['month']
            
            query = f"SELECT * FROM {month}"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            return render_template('display_values.html', rows=rows)
        
    except mysql.connector.errors.ProgrammingError as e:
        if "Table 'year2023.December' doesn't exist" in str(e):
            return redirect(url_for('get_values'))
           
    return render_template('get_values.html', month_name=month_name)                   


        
@app.route('/go', methods=['POST'])
def go_to_database():
    return redirect('/login')

@app.route('/go_back', methods=['POST'])
def go_back():
    return redirect('/data')


@app.route('/go_special', methods=['POST'])
def go_special():
    return redirect('/get_special')
# The route for main page and its contents.
@app.route('/')
def main():
    return render_template('main.html')







@app.route('/exit', methods=['POST'])
def exit_route():
    cursor.close()
    db_connection.close()
    return(None)

with app.app_context():
    db.create_all()

from scrypt2 import app  

if __name__ == '__main__':
    
    app.run(debug=True,host="0.0.0.0", port=5000)

    