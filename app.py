from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Iswarya@125",
    database="employee_db"
)

cursor = db.cursor(dictionary=False)

# LOGIN
@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        query = "SELECT * FROM admin WHERE username=%s AND password=%s"
        values = (username, password)

        cursor.execute(query, values)

        admin = cursor.fetchone()

        if admin:
            return redirect('/dashboard')

    return render_template('login.html')

# DASHBOARD
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# ADD EMPLOYEE
@app.route('/add', methods=['GET', 'POST'])
def add_employee():
     if request.method == 'POST':

        name = request.form['name']
        department = request.form['department']
        salary = request.form['salary']
        email = request.form['email']
        phone = request.form['phone']

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Iswarya@125",
            database="employee_db"
        )

        cursor = db.cursor()

        query = """
        INSERT INTO employees(name, department, salary, email, phone)
        VALUES(%s,%s,%s,%s,%s)
        """
        values = (name, department, salary, email, phone)

        cursor.execute(query, values)
        db.commit()

        return redirect('/dashboard')

     return render_template('add_employee.html')
     

# VIEW EMPLOYEES
@app.route('/employees')
def employees():

    db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Iswarya@125",
            database="employee_db"
    )

    cursor.execute('SELECT * FROM employees')
    data = cursor.fetchall()
    print("DATA FROM DB:",data)
    return render_template('view_employees.html', employees=data)

# DELETE EMPLOYEE
@app.route('/delete/<int:id>')
def delete_employee(id):

    query = "DELETE FROM employees WHERE id=%s"

    cursor.execute(query, (id,))
    db.commit()

    return redirect('/employees')

# EDIT EMPLOYEE
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):

    if request.method == 'POST':

        name = request.form['name']
        department = request.form['department']
        salary = request.form['salary']
        email = request.form['email']
        phone = request.form['phone']

        query = """
        UPDATE employees
        SET name=%s, department=%s, salary=%s,
        email=%s, phone=%s
        WHERE id=%s
        """

        values = (name, department, salary, email, phone, id)

        cursor.execute(query, values)
        db.commit()

        return redirect('/employees')

    query = "SELECT * FROM employees WHERE id=%s"

    cursor.execute(query, (id,))

    employee = cursor.fetchone()

    return render_template('edit_employee.html', employee=employee)

# SEARCH EMPLOYEE
@app.route('/search', methods=['GET', 'POST'])
def search_employee():

    data = []

    if request.method == 'POST':

        name = request.form['name']

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Iswarya@125",
            database="employee_db"
        )

        cursor = db.cursor()

        cursor.execute("SELECT * FROM employees WHERE name LIKE %s", ('%' + name + '%',))

        data = cursor.fetchall()

    return render_template("search_employee.html", employees=data)

if __name__ == "__main__":
    app.run(debug=True)
