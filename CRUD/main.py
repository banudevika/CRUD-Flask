import MySQLdb
from flask import  *
from flask_mysqldb import MySQL
app = Flask(__name__)


app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "crud"

mysql = MySQL(app)





@app.route('/')
def Main():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    student = cur.fetchall()
    return render_template('main.html',studentdetails=student)





@app.route('/insert', methods=['POST','GET'])
def insert():
    if request.method == "POST":
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO students (id, name, email, phoneno) VALUES (%s, %s, %s, %s)", (id, name, email, phone))
            mysql.connection.commit()
            return redirect(url_for('Main'))
        except MySQLdb.IntegrityError as e:
            msg = str(e)
            if 'Duplicate entry' in msg:
                return  render_template('addstudent.html',dmsg=True)
            else:
                return  render_template('addstudent.html',error = True)
    return render_template('addstudent.html')



@app.route('/delete/<string:id>',methods=['GET'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM students WHERE id=%s',(id,))
    mysql.connection.commit()
    
    return redirect(url_for('Main'))




@app.route('/update/<string:id>', methods=['POST', 'GET'])
def update(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students WHERE id = %s", (id,))
    student = cur.fetchone()

    if request.method == 'POST':
        # Handle form submission

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur.execute('UPDATE students SET name = %s, email = %s, phoneno = %s WHERE id = %s', (name, email, phone, id))
        mysql.connection.commit()
        return redirect(url_for('Main'))
    else:
        return render_template('updatepage.html',data = student)


if __name__ == '__main__':
    app.run(debug=True)






# @app.route('/Addstudent')
# def Add():
#     return render_template('Addstudent.html')


