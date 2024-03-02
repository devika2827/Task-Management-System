import mysql.connector as c

con = c.connect(host = 'localhost', user = 'root', password = 'root1234')
cur = con.cursor()

cur.execute('USE Task;')
cur.execute('CREATE TABLE User(User_ID int, Username varchar(255), Password varchar(200));')


def user():
    choice = 'L'

    while choice in ('L','S','E'):
        print('''1. Login (L)
2. Sign Up (S)
3. Exit (E) ''')
        choice = input('Enter your choice : ')

        if choice == 'L':
            login()
        
        elif choice == 'S':
            sign_up()
        
        elif choice == 'E':
            print('---------------------------------------------------------------------------------------------------')
            cur.close()
            break
        
        else : 
            print(' Choose from the given options ! ')

def login():
    uname = input('Enter the Username : ')
    password = input('Enter the Password : ')
    
    cur.execute(f"SELECT * FROM User WHERE username = '{uname}' AND password = '{password}';")
    a = cur.fetchone()
    if a:
        print(a)
        print("Login successful!")
        global user_id
        user_id = a[0]
        menu()
    
    else:
        print("Invalid username or password.")


def sign_up():
    uname = input('Enter Username : ') 
    
    cur.execute(f"SELECT * FROM User WHERE username = '{uname}';")
    
    if cur.fetchone():
        print("Username already exists. Please choose another.")
        return
    
    password = input('Enter the Password : ')
    
    cur.execute("SELECT LAST_INSERT_ID();")
    
    global user_id
    user_id = cur.fetchone()[0]

    print(f"Signup successful! User ID: '{user_id}'")
    global t_name
    t_name = f"tasks_{user_id}"
    cur.execute(f"INSERT INTO User (user_id, username, password) VALUES ({user_id},'{uname}','{password}')")
    cur.execute(f"CREATE TABLE {t_name} (Task_ID int, Task varchar(200), Category varchar(200), Due_Date DATE, Status char(200), Priority varchar(200) ); ")
    
    con.commit()
    
    

def menu():
    
    print('---------------------------------Welcome to Task Management System-----------------------------------')
    print()
    while True:
        print('What would you like to do?')
        print('''1. Add Task
2. Modify Task
3. Change status
4. See pending tasks
5. View all tasks
6. See important tasks
7. Delete task
8. Exit''')
      
        ch = int(input('Enter choice : '))
        print()
        
        if ch == 1:
            add()
            print()
        
        elif ch == 2:
            modify()
            print()
        
        elif ch == 3:
            change()
            print()
        
        elif ch == 4:
            pending()
            print()
        
        elif ch == 5:
            display()
            print()
        
        elif ch == 6:
            imp()
            print()
        
        elif ch == 7:
            delete()
            print()
        
        else:
            break

def add():
    id = input('Enter Task ID : ')
    task = input('Enter Task : ')
    cat = input('Enter Category : ')
    due = input('Enter Due Date : ')
    status = input('Enter Status (Pending/Complete): ')
    pri = input('Enter Priority : ')

    cur.execute(f"INSERT INTO {t_name} VALUES('{id}','{task}','{cat}','{due}','{status}','{pri}')")
    con.commit()
    print('Task added!')

def modify():
    
    id = input('Enter the Task ID : ')
    column = input('Enter Column to be changed : ')
    val = input('Enter the new value : ')

    cur.execute(f"UPDATE {t_name} SET {column} = '{val}' WHERE task_id = '{id}' ;")
    con.commit()
    print('Modified!')


def change():

    id = input('Enter the Task ID : ')
    val = input('Enter ( Pending / Complete ) : ')

    cur.execute(f"UPDATE {t_name} SET status = '{val}' WHERE task_id = '{id}';")
    con.commit()
    print('Status changed!')

def pending():

    cur.execute(f"SELECT task,due_date,priority FROM {t_name} WHERE status = 'Pending';")
    pending_tasks = cur.fetchall()

    if not pending_tasks:
        print('There are no pending tasks!')
    else:
        for task_info in pending_tasks:
            print(list(task_info))

def display():

    cur.execute(f"SELECT * FROM {t_name} ORDER BY Due_Date;")
    tasks = cur.fetchall()

    if not tasks:
        print('There are no tasks!')
    else:
        for task_info in tasks:
            print(list(task_info))
        

def imp():

    cur.execute(f"SELECT task,due_date,status FROM {t_name} WHERE priority = 'Important';")
    imp_tasks = cur.fetchall()

    if not imp_tasks:
        print('There are no important tasks!')
    else:
        for task_info in imp_tasks:
            print(list(task_info))
        
def delete():

    a = input('Enter the task to be deleted : ')
    cur.execute(f"DELETE FROM {t_name} WHERE Task = '{a}';")
    con.commit()
    print('Task deleted! ')

user()