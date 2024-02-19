import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, session
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
  
app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'

data = {'SELECT username, password FROM users'}

def get_register(register_id):
    conn = get_db_connection()
    register = conn.execute('SELECT * FROM register WHERE id = ?',
                        (register_id,)).fetchone()
    conn.close()
    if register is None:
        abort(404)
    return register

def get_residents_id(residents_id):
    conn = get_db_connection()
    residents = conn.execute('SELECT * FROM resident WHERE id = ?',
                        (residents_id,)).fetchone()
    conn.close()
    if residents is None:
        abort(404)
    return residents

def get_officials_id(officials_id):
    conn = get_db_connection()
    officials = conn.execute('SELECT * FROM officials WHERE id = ?',
                        (officials_id,)).fetchone()
    conn.close()
    if officials is None:
        abort(404)
    return officials


@app.route('/tpopulation')
def postPop():
    conn = get_db_connection()
    resident = conn.execute('SELECT * FROM resident ORDER BY name ASC').fetchall()
    conn.close()
    
    return render_template('tpopulation.html', resident=resident)

@app.route('/tsenior')
def postSen():
    conn = get_db_connection()
    resident = conn.execute('SELECT * FROM resident WHERE age >= 60 ORDER BY name ASC').fetchall()
    conn.close()
    
    return render_template('tsenior.html', resident=resident)
@app.route('/tadult')
def postAdu():
    conn = get_db_connection()
    resident = conn.execute('SELECT * FROM resident WHERE age >= 20 AND NOT age >=59 ORDER BY name ASC').fetchall()
    conn.close()
    
    return render_template('tadult.html', resident=resident)

@app.route('/tteen')
def postTee():
    conn = get_db_connection()
    resident = conn.execute('SELECT * FROM resident WHERE age >= 13 AND NOT age >=19 ORDER BY name ASC').fetchall()
    conn.close()
    
    return render_template('tteen.html', resident=resident)

@app.route('/tchild')
def postChi():
    conn = get_db_connection()
    resident = conn.execute('SELECT * FROM resident WHERE age <= 12 ORDER BY name ASC').fetchall()
    conn.close()
    
    return render_template('tchild.html', resident=resident)




@app.route('/officials')
def postOff():
    conn = get_db_connection()
    officials = conn.execute('SELECT * FROM officials ORDER BY name ASC').fetchall()
    conn.close()
    
    return render_template('officials.html', officials=officials)

@app.route('/editOff')
def posteditOff():
    conn = get_db_connection()
    officials = conn.execute('SELECT * FROM officials').fetchall()
    conn.close()
    
    return render_template('editOff.html', officials=officials)

@app.route('/resident')
def postRes():
    conn = get_db_connection()
    resident = conn.execute('SELECT * FROM resident ORDER BY name ASC').fetchall()
    conn.close()

    return render_template('resident.html', resident=resident)

@app.route('/brgyclearance')
def postClear():
    conn = get_db_connection()
    resident = conn.execute('SELECT * FROM resident ORDER BY name ASC').fetchall()
    conn.close()

    return render_template('brgyclearance.html', resident=resident)

@app.route('/register')
def indexreg():
    return render_template('register.html')
    
@app.route('/register', methods=('GET', 'POST'))
def register():
   
    conn = get_db_connection()
    r_fullname = request.form['r_fullname']
    r_username = request.form['r_username']
   
    r_password = request.form['r_password']
    r_confirmpass = request.form['r_confirmpass']
    error = None

    cur = conn.cursor()
    
    cur.execute("SELECT * FROM users WHERE username = ?", (r_username,))
    
    if request.method == 'POST':
        if cur.fetchone() is not None:
            error = flash('Username registered already. Try Again!')
        
        elif r_password != r_confirmpass:
            flash ('password not match. Try again.')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (fullname, username, password) VALUES (?, ?, ?)',
                         (r_fullname, r_username, r_password))
            conn.commit()
            flash("Register Successfuly!")
            conn.close()
            return redirect(url_for('login'))
        
        
    return render_template('register.html', error=error)

# LOGIN
@app.route('/')
def index():
    return render_template('login.html')
@app.route('/', methods=('GET', 'POST'))
def login():

    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']


        cur.execute("SELECT * FROM users WHERE username = '"+username+"' and password = '"+password+"' ")
        users = cur.fetchone()

        if users:
            session['username'] = users['username']
            session['password'] = users['password']
            session['fullname'] = users['fullname']
            flash("You've successfully logged in!")
            return redirect(url_for('dashboard1'))
        else:
            flash("No registered account")
            return redirect(url_for('login'))

    return render_template('login.html')


# LOGOUT
@app.route('/logout')
def logout():
    flash("You've successfully logged out!")
    return redirect('/')


# DASHBOARD
@app.route('/dashboard1')
def dashboard1():
    conn = get_db_connection()
    resident = conn.execute('SELECT * FROM resident').fetchall()
    total = conn.execute('SELECT COUNT(id) FROM resident').fetchone()[0]
    senior = conn.execute('SELECT COUNT(age) FROM resident WHERE age >= 60').fetchone()[0]
    adults = conn.execute('SELECT COUNT(age) FROM resident WHERE age >= 20 AND NOT age >= 59').fetchone()[0]
    teens = conn.execute('SELECT COUNT(age) FROM resident WHERE age >= 13 AND NOT age >= 19').fetchone()[0]
    children = conn.execute('SELECT COUNT(age) FROM resident WHERE age <= 12').fetchone()[0]

    conn.close()
    return render_template('dashboard1.html', total=total, senior=senior, adults=adults, teens=teens, children=children)

# TOTAL POPULATION
@app.route('/tpopulation', methods=('GET', 'POST'))
def tpopulation():
    conn = get_db_connection()
    conn.close()
    return render_template('tpopulation.html')

# TOTAL SENIOR
@app.route('/tsenior', methods=('GET', 'POST'))
def tsenior():
    conn = get_db_connection()
    conn.close()
    return render_template('tsenior.html')

# TOTAL ADULTS
@app.route('/tadult', methods=('GET', 'POST'))
def tadult():
    conn = get_db_connection()
    conn.close()
    return render_template('tadult.html')

# TOTAL TEENAGERS
@app.route('/tteen', methods=('GET', 'POST'))
def tteen():
    conn = get_db_connection()
    conn.close()
    return render_template('tteen.html')

# TOTAL CHILDREN
@app.route('/tchild', methods=('GET', 'POST'))
def tchild():
    conn = get_db_connection()
    conn.close()
    return render_template('tchild.html')


# OFFICIALS
@app.route('/officials', methods=('GET', 'POST'))
def officials():
    if request.method == 'POST':
        name = request.form['name']
        chair = request.form['chair']
        position = request.form['position']
        contact = request.form['contact']

        if not name:
            flash('name is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO officials (name,chair,position,contact) VALUES (?, ?, ?, ?)',
                         (name,chair, position, contact))
            conn.commit()
            flash("Official successfully added", "success")
            conn.close()
            return redirect(url_for('officials' ))    
    return render_template('officials.html', officials=officials)

# EDIT OFFICIALS
@app.route('/<int:id>/editOff', methods=('GET', 'POST'))
def editOff(id):
    post = get_officials_id(id)
    
    if request.method == 'POST':
        name = request.form['name']
        chair = request.form['chair']
        position = request.form['position']
        contact = request.form['contact']

        if not name:
            flash('name is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE officials SET name = ?, chair = ?, position = ?, contact = ? WHERE id = ?',
                         (name, chair, position, contact, id))
            conn.commit()
            conn.close()
            flash("Official successfully edited", "success")
            return redirect(url_for('officials'))    
    return render_template('editOff.html', post=post)

# DELETE OFFICIALS
@app.route('/<int:id>/deleteOff', methods=('GET', 'POST'))
def deleteOff(id):
    officials = get_officials_id(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM officials WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(officials['name']))
    return redirect(url_for('officials'))


# RESIDENTS
@app.route('/resident', methods=('GET', 'POST'))
def resident():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        citizenship = request.form['citizenship']
        bplace = request.form['bplace']
        bdate = request.form['bdate']
        age = request.form['age']
        cstatus = request.form['cstatus']      
        gender = request.form['gender']
        purok = request.form['purok']
        contact = request.form['contact']
        occupation = request.form['occupation']
        address = request.form['address']
        if not name:
            flash('name is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO resident (name,email,citizenship,bplace,bdate,age,cstatus,gender,purok,contact,occupation,address) VALUES (?, ?, ?, ?,?, ?, ?, ?,?, ?, ?, ?)',
                         (name,email,citizenship,bplace,bdate,age,cstatus,gender,purok,contact,occupation,address))
            conn.commit()
            flash("Resident successfully added!", "success")
            conn.close()
            return redirect(url_for('resident'))    
    return render_template('resident.html', resident=resident)

# EDIT RESIDENTS
@app.route('/<int:id>/editRes', methods=('GET', 'POST'))
def editRes(id):
    post = get_residents_id(id)
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        citizenship = request.form['citizenship']
        bplace = request.form['bplace']
        bdate = request.form['bdate']
        age = request.form['age']
        cstatus = request.form['cstatus']
        gender = request.form['gender']
        purok = request.form['purok']
        contact = request.form['contact']
        occupation = request.form['occupation']
        address = request.form['address']
        

        if not name:
            flash('name is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE resident SET name = ?, email = ?, citizenship = ?, bplace = ?, bdate = ?, age = ?, cstatus = ?, gender = ?, purok = ?, contact = ?, occupation = ?, address = ?'
                        ' WHERE id = ?',
                         (name,email,citizenship, bplace, bdate, age, cstatus, gender, purok, contact, occupation, address, id))
            conn.commit()
            flash("Resident successfully edited", "success")
            conn.close()
            return redirect(url_for('resident'))    
    return render_template('editRes.html', post=post)

# DELETE RESIDENTS
@app.route('/<int:id>/deleteRes', methods=('GET', 'POST'))
def deleteRes(id):
    resident = get_residents_id(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM resident WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(resident['name']))
    return redirect(url_for('resident'))

# VIEW RESIDENTS
@app.route('/<int:id>/view_res', methods=('GET', 'POST'))
def view_res(id):
    post = get_residents_id(id)
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        citizenship = request.form['citizenship']
        bplace = request.form['bplace']
        bdate = request.form['bdate']
        age = request.form['age']
        contact = request.form['contact']
        occupation = request.form['occupation']
        address = request.form['address']
        

        if not name:
            flash('name is required!')
        else:
            conn = get_db_connection()
            return redirect(url_for('resident'))    
    return render_template('view_res.html', post=post)

# BRGY CLEARANCE
@app.route('/brgyclearance', methods=('GET', 'POST'))
def brgyclearance():
    
    
    return render_template('brgyclearance.html')

# GENERATE CERTIFICATE
@app.route('/generate', methods=('GET', 'POST'))
def generate():
    conn = get_db_connection()
    resident = conn.execute('SELECT * FROM resident').fetchall()
    name = conn.execute('SELECT name FROM resident ').fetchone()[0]
    captain = conn.execute('SELECT name FROM officials ').fetchone()[0]
    
    
    return render_template('generate.html',name=name, captain=captain)
# ABOUT
@app.route('/about')
def about():
    return render_template('about.html')
