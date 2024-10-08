
from flask import Flask, render_template, request, redirect, url_for,session
import psycopg2
import secrets

app = Flask(__name__)

app.secret_key =secrets.token_hex(16)
def db_conn():
    conn = psycopg2.connect(database="cinema", host="localhost", user="postgres", password="root", port="5432")
    return conn

# Admin, Employee, and Customer Login
@app.route('/')
def renderLoginPage():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def verifyAndRenderRespective():
    username = request.form['username']
    password = request.form['password']

    try:
        if username == 'employee' and password == 'employee': 
            return render_template('employee.html')

        elif username == 'manager' and password == 'manager':
            return render_template('index.html') 

        elif username == 'customer' and password == 'customer':  
            return render_template('customer.html')  

        else:
            return render_template('loginfail.html')

    except Exception as e:
        print(e)
        return render_template('loginfail.html')
    
def runQuery(query, params=None):
    conn = db_conn()  # Assuming you have a function to establish a DB connection
    cur = conn.cursor()
    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()


# ------------- ADMIN FUNCTIONALITIES -------------

@app.route('/admin')
def index():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM employee ORDER BY emp_id;')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', data=data)

# Create Employee
@app.route('/create', methods=['POST'])
def create():
    conn = db_conn()
    cur = conn.cursor()
    emp_id = request.form['emp_id']
    salary = request.form['salary']
    birth_date = request.form['birth_date']
    age = request.form['age']
    first_name = request.form['first_name']
    middle_name = request.form['middle_name']
    last_name = request.form['last_name']
    gender = request.form['gender']
    email_id = request.form['email_id']
    phone_no = request.form['phone_no']
    dep_id = request.form['dep_id']
    cur.execute('''INSERT INTO employee 
               (emp_id, salary, birth_date, age, first_name, middle_name, last_name, gender, email_id, phone_no, dep_id) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
               (emp_id, salary, birth_date, age, first_name, middle_name, last_name, gender, email_id, phone_no, dep_id))
    
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Update Employee
@app.route('/update', methods=['POST'])
def update():
    conn = db_conn()
    cur = conn.cursor()

    emp_id = request.form['emp_id']

    # List of columns and values to update
    columns = []
    values = []

    # Only update the fields that are provided (non-empty)
    if request.form['salary']:
        columns.append('salary = %s')
        values.append(request.form['salary'])

    if request.form['birth_date']:
        columns.append('birth_date = %s')
        values.append(request.form['birth_date'])

    if request.form['age']:
        columns.append('age = %s')
        values.append(request.form['age'])

    if request.form['first_name']:
        columns.append('first_name = %s')
        values.append(request.form['first_name'])

    if request.form['middle_name']:
        columns.append('middle_name = %s')
        values.append(request.form['middle_name'])

    if request.form['last_name']:
        columns.append('last_name = %s')
        values.append(request.form['last_name'])

    if request.form['gender']:
        columns.append('gender = %s')
        values.append(request.form['gender'])

    if request.form['email_id']:
        columns.append('email_id = %s')
        values.append(request.form['email_id'])

    if request.form['phone_no']:
        columns.append('phone_no = %s')
        values.append(request.form['phone_no'])

    if request.form['dep_id']:
        columns.append('dep_id = %s')
        values.append(request.form['dep_id'])

    # Make sure we are updating at least one field
    if columns:
        # Add the emp_id at the end of the values list (for the WHERE condition)
        values.append(emp_id)
        
        # Join the columns with commas to form the SET part of the query
        update_query = f"UPDATE employee SET {', '.join(columns)} WHERE emp_id = %s"
        
        # Execute the query
        cur.execute(update_query, values)
        conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for('index'))


# Delete Employee
@app.route('/delete', methods=['POST'])
def delete():
    conn = db_conn()
    cur = conn.cursor()
    emp_id = request.form['emp_id']
    cur.execute('''DELETE FROM employee WHERE emp_id = %s''', (emp_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Admin view Transactions
@app.route('/view_transactions')
def view_transactions():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM payment ORDER BY payment_id;')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('view_transactions.html', data=data)

# Admin view Tickets
@app.route('/view_tickets')
def view_tickets():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tickets ORDER BY ticket_id;')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('view_tickets.html', data=data)

@app.route('/admin/performance')
def monitor_performance():
    conn = db_conn()
    cur = conn.cursor()

    # Query for total sales
    cur.execute('SELECT COUNT(*), SUM(amount) FROM payment')
    total_tickets, total_revenue = cur.fetchone()

    # Query for most popular movies
    cur.execute('''SELECT m.movie_name, COUNT(t.ticket_id) AS tickets_sold 
                   FROM movies m
                   JOIN tickets t ON m.movie_name = t.movie_name
                   GROUP BY m.movie_name
                   ORDER BY tickets_sold DESC LIMIT 5;''')
    popular_movies = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('performance.html', 
                           total_tickets=total_tickets, 
                           total_revenue=total_revenue,
                           popular_movies=popular_movies,
                           )

# ------------- EMPLOYEE FUNCTIONALITIES -------------
@app.route('/employee_dashboard')
def employee_dashboard():
    return render_template('employee.html')

# Employee sell tickets (example form handling)
@app.route('/sell_ticket', methods=['POST'])
def sell_ticket():
    conn = db_conn()
    cur = conn.cursor()
    emp_id = request.form['emp_id']
    ticket_id = request.form['ticket_id']
    price = request.form['price']
    discount = request.form['discount']
    shows = request.form['shows']
    movie_name = request.form['movie_name']
    booking_date = request.form['booking_date']
    customer = request.form['booking_date']
    
    cur.execute('''INSERT INTO tickets (ticket_id, price, discount, shows,movie_name,booking_date,customer_id, movies_id) 
                   VALUES ( %s, %s, %s, %s)''', 
                (ticket_id, price, discount, shows,movie_name,booking_date,customer_id, movies_id ))
    conn.commit()
    conn.close()
    return redirect(url_for('employee_dashboard'))



@app.route('/employee/add-movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        # Collect the form data
        movies_id=request.form['movies_id']
        movie_name = request.form['movie_name']
        release_date = request.form['release_date']
        genre = request.form['genre']
        roles= request.form['roles']
    
        movie_lang = request.form['movie_lang']
        view_type = request.form['view_type']


        # Insert movie into the database
        conn = db_conn()
        cur = conn.cursor()
        cur.execute('''INSERT INTO movies (movies_id,movie_name,  release_date, genre, roles,movie_lang,view_type) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                    (movies_id, movie_name,  release_date, genre, roles,movie_lang,view_type))
        conn.commit()
        cur.close()
        conn.close()

        return "Movie added successfully!"

    return render_template('add_movie.html')


# ------------- CUSTOMER FUNCTIONALITIES -------------
@app.route('/customer_dashboard')
def customer_dashboard():
    return render_template('customer.html')

# Customer book ticket
# Customer selects movie, language, view type, and show time
@app.route('/select_movie', methods=['GET', 'POST'])
def select_movie():
    conn = db_conn()
    cur = conn.cursor()

    if request.method == 'POST':
        customer_id = request.form['customer_id']
        movie_id = request.form['movie_id']
        movie_lang = request.form['movie_lang']
        view_type = request.form['view_type']
        show_time = request.form['show_time']
        
        # Save the selections to session for use in the next step
        session['customer_id'] = customer_id
        session['movie_id'] = movie_id
        session['movie_lang'] = movie_lang
        session['view_type'] = view_type
        session['show_time'] = show_time

        return redirect(url_for('select_seats'))
    
    cur.execute('SELECT * FROM movies')  # Get list of movies
    movies = cur.fetchall()

    cur.close()
    conn.close()
    
    return render_template('select_movie.html', movies=movies)
# Customer selects seats
@app.route('/select_seats', methods=['GET', 'POST'])
def select_seats():
    conn = db_conn()
    cur = conn.cursor()

    if request.method == 'POST':
        seat_id = request.form['seat_id']
        no_of_seats = request.form['no_of_seats']

        # Save seat selection to session for later use
        session['seat_id'] = seat_id
        session['no_of_seats'] = no_of_seats

        return redirect(url_for('make_payment'))
    
    # Get available seats for the selected show
    cur.execute('SELECT * FROM seats WHERE available = TRUE')
    available_seats = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('select_seats.html', seats=available_seats)
# Customer makes payment and books ticket
@app.route('/make_payment', methods=['GET', 'POST'])
def make_payment():
    conn = db_conn()
    cur = conn.cursor()

    if request.method == 'POST':
        payment_amount = request.form['payment_amount']
        payment_method = request.form['payment_method']

        # Retrieve the data from session
        customer_id = session.get('customer_id')
        movies_id = session.get('movies_id')
        movie_lang = session.get('movie_lang')
        view_type = session.get('view_type')
        show_time = session.get('show_time')
        seat_id = session.get('seat_id')
        no_of_seats = session.get('no_of_seats')

        # Generate ticket ID
        cur.execute('''INSERT INTO bookingInfo (customer_id, movies_id, movie_lang, view_type, show_time, seat_id, no_of_seats) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING ticket_id''',
                    (customer_id, movies_id, movie_lang, view_type, show_time, seat_id, no_of_seats))
        ticket_id = cur.fetchone()[0]

        # Update seat availability
        cur.execute('UPDATE seats SET available = FALSE WHERE seat_id = %s', (seat_id,))

        # Insert payment details into the payment table
        cur.execute('''INSERT INTO paymentInfo (customer_id, ticket_id, amount, payment_method, payment_date) 
                       VALUES (%s, %s, %s, %s, NOW())''', (customer_id, ticket_id, payment_amount, payment_method))

        conn.commit()
        cur.close()
        conn.close()

        # Redirect to customer dashboard or display the ticket confirmation
        return redirect(url_for('customer_dashboard'))

    return render_template('make_payment.html')



if __name__ == '__main__':
    app.run(debug=True, port=5001)
