
from flask import Flask, render_template, request, redirect, url_for,session
import psycopg2
from psycopg2.extras import RealDictCursor
import secrets
import random
import logging
from flask import flash
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

app.secret_key =secrets.token_hex(16)
def db_conn():
    conn = psycopg2.connect(database="cinema", host="localhost", user="postgres", password="root", port="5432")
    return conn

# Admin, Employee, and Customer Login
@app.route('/')
def renderLoginPage():
    return render_template('login.html')
@app.route('/login')
def login():
    return render_template('login.html')  # Make sure this template exists

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
            return redirect(url_for('customer_dashboard')) 

        else:
            return render_template('loginfail.html')

    except Exception as e:
        print(e)
        return render_template('loginfail.html')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_type = request.form['user_type']
        
        # Redirect to respective signup forms based on the user type
        if user_type == 'admin':
            return redirect(url_for('signup_admin'))
        elif user_type == 'employee':
            return redirect(url_for('signup_employee'))
        elif user_type == 'customer':
            return redirect(url_for('signup_customer'))
    return render_template('choose_signup.html')

# Admin Signup
@app.route('/signup/admin', methods=['GET', 'POST'])
def signup_admin():
    if request.method == 'POST':
        admin_id = request.form['admin_id']  # Get the admin ID from the form
        username = request.form['username']  # Get the username from the form
        pw = request.form['pw']   # Get the password from the form
        
        # Establish a connection to the database
        conn = db_conn()
        cur = conn.cursor()

        # Insert admin details into the database
        cur.execute('''INSERT INTO admin (admin_id, username, pw) 
                       VALUES (%s, %s, %s)''', 
                       (admin_id, username, pw))

        # Commit the transaction and close the connection
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('login'))  # Redirect to the login page after successful registration

    return render_template('signup_admin.html')


@app.route('/signup/employee', methods=['GET', 'POST'])
def signup_employee():
    if request.method == 'POST':
        # Fetch form data
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
        username = request.form['username']
        password = request.form['password']

        # Insert employee details into the database
        conn = db_conn()  # Establish a connection to the database
        cur = conn.cursor()
        
        cur.execute('''INSERT INTO employee 
                    (emp_id, salary, birth_date, age, first_name, middle_name, last_name, gender, email_id, phone_no, dep_id, username, password) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                    (emp_id, salary, birth_date, age, first_name, middle_name, last_name, gender, email_id, phone_no, dep_id, username, password))

        # Commit the transaction and close the connection
        conn.commit()
        cur.close()
        conn.close()

        # Redirect to the login page after successful signup
        return redirect(url_for('login')) 

    # Render the signup form for 'GET' requests
    return render_template('signup_employee.html')


# Customer Signup
@app.route('/signup/customer', methods=['GET', 'POST'])
def signup_customer():
    if request.method == 'POST':
        # Fetch form data
        customer_id = request.form['customer_id']
        cphone_no = request.form['cphone_no']
        cemail_id = request.form['cemail_id']
        cdob = request.form['cdob']
        cage = request.form['cage']
        cgender = request.form['cgender']
        cfirst_name = request.form['cfirst_name']
        cmiddle_name = request.form['cmiddle_name']
        clast_name = request.form['clast_name']
        caddress = request.form['caddress']
        username = request.form['username']
        password = request.form['password']

        # Insert customer details into the database
        conn = db_conn()  # Establish a connection to the database
        cur = conn.cursor()
        
        cur.execute('''INSERT INTO customer 
                    (customer_id, cphone_no, cemail_id, cdob, cage, cgender, cfirst_name, cmiddle_name, clast_name, caddress, username, password) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                    (customer_id, cphone_no, cemail_id, cdob, cage, cgender, cfirst_name, cmiddle_name, clast_name, caddress, username, password))

        # Commit the transaction and close the connection
        conn.commit()
        cur.close()
        conn.close()

        # Redirect to the login page after successful signup
        return redirect(url_for('login')) 

    # Render the signup form for 'GET' requests
    return render_template('signup_customer.html')

   
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
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="cinema",
        user="postgres",
        password="root"
    )
    return conn

# ------------- ADMIN FUNCTIONALITIES -------------

@app.route('/admin')
def index():
    conn = None
    cur = None
    try:
        logging.debug("Attempting to connect to the database")
        conn = db_conn()
        if not conn:
            logging.error("Failed to establish database connection")
            return render_template('index.html', data=[], error="Database connection failed")
        
        logging.debug("Creating cursor")
        cur = conn.cursor()
        logging.debug("Executing SQL query")
        cur.execute('SELECT * FROM employee;')
        logging.debug("Fetching data")
        data = cur.fetchall()
        logging.debug(f"Fetched {len(data)} rows")
        
        if not data:
            logging.warning("No data retrieved from the database")
        return render_template('index.html', data=data)
    except Exception as e:
        print(f"An error occurred: {e}")
        return render_template('index.html', data=[], error="Failed to fetch employee data")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.route('/view_payment')
def view_payment():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''SELECT * FROM payment''')
    payment = cur.fetchall()
    
    # Calculate total revenue
    total_revenue = sum(row[3] for row in payment)  # Assuming the amount is in the fourth column (index 3)

    cur.close()
    conn.close()
    
    # Pass total_revenue to the template
    return render_template('view_payment.html', payment=payment, total_revenue=total_revenue)

@app.route('/employee_list')
def view_employee():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM employee')
    employee = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Debugging: print the fetched data
    print("Fetched Employee Data:", employee)  # Add this line
    
    return render_template('employee_list.html', employee=employee)



@app.route('/back_to_dashboard')
def back_to_dashboard():
    return redirect(url_for('index'))  
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
def update_employee():
    conn = db_conn()
    cur = conn.cursor()
    emp_id = request.form['emp_id']
    update_field = request.form['update_field']
    new_value = request.form['new_value']
    
    # Create SQL query to update the specific field
    query = f"UPDATE employee SET {update_field} = %s WHERE emp_id = %s"
    cur.execute(query, (new_value, emp_id))
    conn.commit()

    return redirect(url_for('index'))  # Adjust this to your page route



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
    customer_id = request.form['customer_id']
    movies_id = request.form['movies_id']

    
    cur.execute('''INSERT INTO tickets (ticket_id, price, discount, shows,movie_name,booking_date,customer_id, movies_id) 
                   VALUES ( %s, %s, %s, %s ,%s, %s, %s, %s)''', 
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
        poster_url = request.form['poster_url']

        # Insert movie into the database
        conn = db_conn()
        cur = conn.cursor()
        cur.execute('''INSERT INTO movies (movies_id,movie_name,  release_date, genre, roles,movie_lang,view_type,poster_url) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s,%s)''',
                    (movies_id, movie_name,  release_date, genre, roles,movie_lang,view_type,poster_url))
        conn.commit()
        cur.close()
        conn.close()

        return "Movie added successfully!"

    return render_template('add_movie.html')


# ------------- CUSTOMER FUNCTIONALITIES -------------


# Route for the customer home page with options: Book Movie and View Transactions


@app.route('/customer_dashboard')
def customer_dashboard():
    return render_template('customer.html')


# Route for the customer home page with options: Book Movie and View Transactions




# Route for movie booking (show collection of movie posters)
@app.route('/book_movie')
def book_movie():
    conn = db_conn()
    cur = conn.cursor()
    # Fetch available movies from database
    cur.execute("SELECT movies_id, movie_name, poster_url FROM movies")  # Assuming 'movies' table has this data
    rows = cur.fetchall()
    movies = [{'movies_id': row[0], 'movie_name': row[1], 'poster_url': row[2]} for row in rows]
    cur.close()
    conn.close()
    print(movies)  # Print the list of movies to verify URLs
    return render_template('select_movie.html', movies=movies)  # Display the movie posters

# Route for selecting movie details (e.g., language, showtime, etc.)
@app.route('/movie_details', methods=['GET', 'POST'])

def movie_details():
    if request.method == 'POST':
        # Retrieve or generate customer_id
        cust_id = session.get('cust_id')

        if not cust_id:  # If no customer_id is stored in the session
            cust_id = random.randint(1000, 9999)  # Generate a random customer_id
            session['customer_id'] = cust_id

            # Insert new customer into the `customer` table
            conn = db_conn()
            cur = conn.cursor()

            try:
                cur.execute('''INSERT INTO customer (cust_id) VALUES (%s)''', (cust_id,))
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(f"Error inserting customer: {e}")
            finally:
                cur.close()
                conn.close()

        # Retrieve booking details from form
        movies_id = request.form.get('movies_id')  # Use `get()` to avoid KeyErrors
        movie_lang = request.form.get('movie_lang')
        show_time = request.form.get('show_time')
        view_type = request.form.get('view_type')
       
        # Insert booking info into the `bookingInfo` table
        conn = db_conn()
        cur = conn.cursor()

        try:
            cur.execute('''INSERT INTO bookingInfo (cust_id, movies_id, movie_lang, show_time, view_type) 
                           VALUES (%s, %s,%s, %s, %s)''', 
                        (cust_id,movies_id, movie_lang, show_time, view_type))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error inserting booking info: {e}")
        finally:
            cur.close()
            conn.close()
        
        
    return render_template('movie_details.html')


# Route for selecting seats (similar to BookMyShow UI)
@app.route('/select_seats', methods=['GET', 'POST'])
def select_seats():
    if request.method == 'POST':
        seats = request.form.getlist('seats')  # List of selected seat IDs
        num_seats = len(seats)
        customer_id = session['customer_id']

        conn = db_conn()
        cur = conn.cursor()
        # Insert seat booking into seatBooking table
        for seat_id in seats:
            cur.execute('''INSERT INTO seatBooking (customer_id, movies_id, seat_id, num_seats) 
                           VALUES (%s, %s, %s, %s)''', 
                           (customer_id, 1, seat_id, num_seats))  # Use a default movie_id (e.g., 1)
        conn.commit()
        cur.close()
        conn.close()

        return redirect('/make_payment')  # Redirect to payment without passing movie_id

    return render_template('select_seats.html')  # Seat selection graphic (similar to BookMyShow)

# Route for payment (UI where user selects payment mode and enters amount)
@app.route('/make_payment', methods=['GET', 'POST'])
def make_payment():
    if request.method == 'POST':
        payment_mode = request.form['payment_mode']
        amount = request.form['amount']
        customer_id = session['customer_id']

        conn = db_conn()
        cur = conn.cursor()
        # Insert payment info into payment table
        cur.execute('''INSERT INTO payment (customer_id, movies_id, num_seats, payment_mode, amount) 
                       VALUES (%s, %s, %s, %s, %s)''', 
                       (customer_id, 1, 1, payment_mode, amount))  # Use a default movie_id and num_seats
        conn.commit()
        cur.close()
        conn.close()

        flash("Transaction Complete!")
        return redirect('/book_movie')  # Redirect back to movie selection page

    return render_template('make_payment.html')  # Payment form (mode of payment, amount)

# Route to view the most recent transaction (bill format)
@app.route('/view_transaction')
def view_transaction():
    customer_id = session['customer_id']

    conn = db_conn()
    cur = conn.cursor()
    # Fetch the most recent transaction
    cur.execute('''SELECT * FROM payment WHERE customer_id = %s ORDER BY transaction_time DESC LIMIT 1''', 
                (customer_id,))
    transaction = cur.fetchone()
    cur.close()
    conn.close()

    return render_template('view_transaction.html', transaction=transaction)  # Display the transaction in bill format

if __name__ == '__main__':
    app.run(debug=True)
