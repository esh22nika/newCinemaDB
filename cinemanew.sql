CREATE TABLE customer (
    customer_id SERIAL PRIMARY KEY,
    cphone_no CHAR(10),
    cemail_id VARCHAR(25),
    cdob DATE,
    cage INTEGER,
    cgender CHAR(1),
    cfirst_name VARCHAR(25),
    cmiddle_name VARCHAR(25),
    clast_name VARCHAR(25),
    caddress VARCHAR(100),
    username VARCHAR(255),
    password VARCHAR(255)
);

CREATE TABLE employee (
    emp_id SERIAL PRIMARY KEY,
    salary INTEGER,
    birth_date DATE,
    age INTEGER,
    first_name VARCHAR(25),
    middle_name VARCHAR(25),
    last_name VARCHAR(25),
    gender CHAR(1),
    email_id VARCHAR(25),
    phone_no CHAR(10),
    dep_id INTEGER,
    username VARCHAR(255),
    password VARCHAR(255),
    FOREIGN KEY (dep_id) REFERENCES department(dep_id)
);

CREATE TABLE department (
    dep_id SERIAL PRIMARY KEY,
    dep_name VARCHAR(50)
);

CREATE TABLE movies (
    movies_id SERIAL PRIMARY KEY,
    movie_name VARCHAR(100),
    release_date DATE,
    genre CHAR(10),
    roles CHAR(100),
    movie_lang VARCHAR(25),
    view_type VARCHAR(100),
    poster_url TEXT
);

CREATE TABLE tickets (
    ticket_id SERIAL PRIMARY KEY,
    price INTEGER,
    discount INTEGER,
    shows INTEGER,
    movie_name VARCHAR(25),
    booking_date DATE,
    customer_id INTEGER,
    movies_id INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (movies_id) REFERENCES movies(movies_id)
);

CREATE TABLE payment (
    payment_id SERIAL PRIMARY KEY,
    payment_mode VARCHAR(10),
    payment_date DATE,
    amount INTEGER,
    customer_id INTEGER,
    ticket_id INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
);

CREATE TABLE seats (
    seat_id VARCHAR(10) PRIMARY KEY,
    ticket_id INTEGER,
    no_of_seats INTEGER,
    available BOOLEAN,
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
);

CREATE TABLE bookinginfo (
    ticket_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    movies_id INTEGER,
    movie_lang VARCHAR(50),
    view_type VARCHAR(50),
    show_time VARCHAR(20),
    seat_id VARCHAR(10),
    no_of_seats INTEGER,
    booking_date TIMESTAMP WITHOUT TIME ZONE,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (movies_id) REFERENCES movies(movies_id),
    FOREIGN KEY (seat_id) REFERENCES seats(seat_id)
);

CREATE TABLE paymentinfo (
    payment_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    ticket_id INTEGER,
    amount NUMERIC(10,2),
    payment_method VARCHAR(50),
    payment_date TIMESTAMP WITHOUT TIME ZONE,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
);

CREATE TABLE admin (
    admin_id SERIAL PRIMARY KEY,
    pw VARCHAR(25),
    username VARCHAR(255)
);

CREATE TABLE emp1 (
    e_id SERIAL PRIMARY KEY,
    e_uname VARCHAR(100),
    manager_id INTEGER,
    FOREIGN KEY (manager_id) REFERENCES emp1(e_id)
);
