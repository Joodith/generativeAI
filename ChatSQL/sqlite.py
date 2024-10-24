import sqlite3

connection=sqlite3.connect('student.db')
cursor=connection.cursor()
cursor.execute('CREATE TABLE student (name VARCHAR(20), class VARCHAR(20), section VARCHAR(5), marks INTEGER)')

#Insert 5 records in the above table
cursor.execute("INSERT INTO student VALUES ('John', 'Devops', 'A', 90)")
cursor.execute("INSERT INTO student VALUES ('Smith', 'Data Science', 'B', 80)")
cursor.execute("INSERT INTO student VALUES ('David', 'Cloud', 'C', 85)")
cursor.execute("INSERT INTO student VALUES ('Miller', 'Devops', 'B', 95)")
cursor.execute("INSERT INTO student VALUES ('Brown', 'Data Science', 'A', 75)")

connection.commit()

print("The inserted records are:")
select_query="SELECT * FROM student"
data=cursor.execute(select_query)

for row in data:
    print(row)  
    
connection.close()




