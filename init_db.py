import psyopg2
conn=psycopg2.connect(database="cinema",host="localhost",user="postgres",password="root",port="5432")
cur=conn.cursor()
cur.execute('''INSERT INTO employee (emp_ID, salary, birth_date, age, first_name, middle_name, last_name, gender, email_ID, phone_no) 
VALUES 
(6984, 60000, '1996-05-15', 34, 'Ella', 'Kumar', 'Reddy', 'M', 'ella.kumar@gmail.com', '9123406780');''')
conn.commit()
curr.close()
conn.close()