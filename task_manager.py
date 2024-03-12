import os
from datetime import datetime, date
from prettytable import PrettyTable
# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password

def get_tasks():
    """
    Reads 'task_file' file.
    If the file doesn't exist, it creates a 'tasks.txt' file and writes 'INITIAL TASK' 
    returns the tasks
    """
    INITIAL_TASK = "admin;Add functionality to task manager;Add additional options and refactor the code.;2030-12-01;2022-11-22;Yes"
    try:
        with open("tasks.txt", 'r') as task_file:
            task_data = task_file.read().split("\n")
            task_data = [t for t in task_data if t != ""]
    except FileNotFoundError:
        with open("tasks.txt", "w") as default_file:
            default_file.write(INITIAL_TASK)
            task_data = INITIAL_TASK
    
    return task_data

def get_task_list():
    """
    the function reads all tasks from 'task.txt', stores a list variable and returns the list.
    """
    task_data = get_tasks()
    task_list = []
    for t_str in task_data:
        curr_t = {}
        # Split by semicolon and manually add each component
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False
        task_list.append(curr_t)   
    
    return task_list

def get_users_detail():
    '''
    This code reads usernames and password from the 'user.txt ' file to 
    allow a user to login. If the file doesn't exist, it creates a 'user.txt' file and writes 
    user: admin
    password: password
    '''
    while True:
        try:
            # Read in user_data
            with open("user.txt", 'r') as user_file:
                user_data = user_file.read().split("\n")
            break
        except FileNotFoundError:
            # If no user.txt file, write one with a default account
            with open("user.txt", "w") as default_file:
                default_file.write("admin;password")
            continue
    # Convert to a dictionary
    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password
 
    return username_password    

def reg_user():
    """
    checking user in the 'user.txt' file, if the user does not exist in the file,
    creates a new user. 
    """
    new_user_data = []
    new_user_in_list = True
    user_list = []
    # getting user names in the "user.txt" file
    with open("user.txt", 'r') as user_file:
        user_details = user_file.read().split("\n")
        for index in user_details:
            user_list.append(index.split(";")[0])  
    # - Request input of a new username
    new_username = input("New Username: ").lower()
    new_user_in_list =True
    # Checking if the user is in the list or not
    while new_user_in_list:
        if new_username in user_list:
            print(f"The user({new_username}) is already in the list, Please enter a new username!")
            new_username = input("New Username: ").lower()
        else:
            new_user_in_list = False
        
    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password
        with open("user.txt", "w") as out_file:  
            for k in username_password:
                new_user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(new_user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")

def add_task():
    """
    Allow a user to add a new task to task.txt file
    Prompt a user for the following: 
    - A username of the person whom the task is assigned to,
    - A title of a task,
    - A description of the task and 
    - the due date of the task.
    """
    # The loop checks the username that has been entered in the 'user.txt' file.
    # If not the code prints out the user names in the file and keeps asking for a valid user name.
    while True:
        username_password  = get_users_detail()
        task_username = input("Name of person assigned to task: ").lower()
        if task_username not in username_password.keys():
            user_table = PrettyTable(["User List"])
            print("User does not exist. Please enter a valid username from below list")
            for user in username_password.keys():
                user_table.add_row([user])
            print(user_table)
            continue
        else:
            break   
    # asks title of the task        
    task_title = input("Title of Task: ").upper()
    # asks description of the task
    task_description = input("Description of Task: ").upper()
    
    # asks due date, if the date's format is not as (YYYY-MM-DD) then keeps asking the date.
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()
    """
    Add the data to the file task.txt and
    Include 'No' to indicate if the task is complete.
    """
    # converts the task's details to a dictionary.
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    #adds the task to the task list and writes the list to 
    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("*" * 50 + "Task successfully added." + "*" * 50)

def view_task():
    """
    Reads the task from task.txt file and prints to the console in a table
    """

    task_list = get_task_list()
    task_no = 1
    task_table = PrettyTable(["No", "Username", "Title", "Description", "Assigned Date", "Due Date", "Status"])
    task_table.align["Title"] = "l"
    task_table.align["Description"] = "l"   
    # adds task to the table.
    for t in task_list:
        task_table.add_row([task_no, t['username'], t['title'], t['description'],
                            t['assigned_date'].strftime(DATETIME_STRING_FORMAT), 
                            t['due_date'].strftime(DATETIME_STRING_FORMAT),
                            "Completed" if t['completed'] else "In progress"
                            ])
        task_no += 1
    print(task_table)

def view_mine(user):
    """
    Reads the  user's task from 'task.txt' file and prints a table in the console
    if the user wants to modify one of his task then sends index number of the task to
    modify_task function. If the task's status is completed so 
    returns the main menu with a console message
    """
    task_list = get_task_list()
    user_task_list = []
    task_index = 0
    # reads the login user's tasks to a list variable
    for t in task_list:
        if t['username'] == user:
            user_task_list.append({"Task" : t['title'],
                                   "Assigned to" : t['username'],
                                   "Date Assigned" : t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                   "Due Date": t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                   "Task Description" : t['description'],
                                   "Completion Status" : "Yes" if t['completed'] else "No",
                                   "Task Index" : task_index,
                                   })
        task_index += 1
    
    task_no = 1
    task_table = PrettyTable(["No", "Title", "Description", "Assigned Date", "Due Date", "Completed"])
    task_table.align["Title"] = "l"
    task_table.align["Description"] = "l"
    # creates a table for user can see in the console
    for task in user_task_list:
        task_table.add_row([task_no, task['Task'], task['Task Description'], 
                            task['Date Assigned'],task['Due Date'], 
                            task['Completion Status']])
        task_no += 1
    print(task_table)
    # The loop gives options to the user can modify his task or return the main menu
    while True:
        user_task_selection = input("If you would like to modify a task please enter the task number\nOR press '-1'for the main menu\n")
        while not user_task_selection.isnumeric():
            if user_task_selection == "-1":
                print("Returning main menu ....\n")
                break
            else:
                print("You haven't entered a valid task number try again!")
                user_task_selection = input("Please enter the task number\nOR press '-1'for the main menu\n")    
        if user_task_selection == "-1":
                break
        user_task_selection = int(user_task_selection)
        if user_task_selection > (task_no - 1) or user_task_selection == 0:
            print("The number that you have entered is not an option")
            continue
        else:
            if user_task_list[user_task_selection-1]["Completion Status"] == "Yes":
                print("The selected task is completed, so You can't modify it,\nreturning the main menu...")
                break
            else:
                modify_task(user_task_list[user_task_selection-1]["Task Index"])
            break
           
def modify_task (task_index):
    """
    gives options to the user to modify selected tasks.
    """
    task_list = get_task_list() 
    menu_text =f'''Select one of the following Options below:
1 - Complete the task
2 - Change the task
3 - Assign the task to another user
'''
    menu = input(menu_text)
    # The loop checks the entered number is a valid number.
    while True:
        while not menu.isnumeric():
            print("You haven't entered a valid number. Please try again!")
            menu = input(menu_text)
        menu = int(menu)
        if 1<= menu <=3:
            break
        else:
            print ("You haven't entered a valid number. Please try again!")
            continue
    if menu == 1: # change the task's status to completed.
        task_list [task_index]["completed"] = True
    elif menu == 2: # change task, task description and due date
        task_title = input("Title of Task: ").upper()
        task_description = input("Description of Task: ").upper()
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break
            except ValueError:
                print("Invalid datetime format. Please use the format specified")
        
        task_list [task_index]['title'] = task_title
        task_list [task_index]['description'] = task_description
        task_list [task_index]['due_date'] = due_date_time
    else: # assigned the task another user, checks the new user in the 'user.txt' file.
        new_user = input("Please enter a new user for the task: ").lower()
        users = get_users_detail()
        while True: # checks the entered user in the 'user.txt' file if not prints all usernames
            if new_user in users.keys():
                task_list [task_index]['username'] = new_user
                break
            else:
                print("The user is not exist, please try again!")
                user_table = PrettyTable(["User List"])
                for user in users.keys():
                    user_table.add_row([user])
                print(user_table)
                new_user = input("Please enter an user from the above list: ").lower()
    with open("tasks.txt", "w") as task_file: # writes the updated task to the 'task.txt' file
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("*" * 50 + "Task successfully updated." + "*" * 50)
                
def display_statistic():
    '''
    If the user is an admin they can display statistics about number of users
     and tasks.
    '''
    username_password  = get_users_detail()
    task_list = get_task_list()
    num_users = len(username_password.keys())
    num_tasks = len(task_list)

    print("-----------------------------------")
    print(f"Number of users: \t\t {num_users}")
    print(f"Number of tasks: \t\t {num_tasks}")
    print("-----------------------------------")    

def generate_reports():
    """
    The function creates 2 reports one for task overview 
    and the other for user overview
    """
    task_list = get_task_list()
    users = get_users_detail()
    
    today_date = datetime.today()
    total_task = len(task_list)
    completed_task = 0
    overdue_task = 0
    users_in_task_list = []
    
    overview_table = PrettyTable(["Total Task", "Completed Task", "Uncompleted Task",
                                  "Uncompleted(%)", "Overdue Task", "Overdue(%)"])
    user_table = PrettyTable(["User", "Total Task Qty", "Task Ratio(%)", "Completion Ratio(%)",
                              "Uncompletion Ratio(%)", "Overdue Ratio(%)"])
    
    for user in users.keys():
        """
        The loop searches each user in the 'user.txt' file and 
        compares fi the user has any task assigned. 
        if the user has one or more tasks then, stores the user's task details.
        """
        user_task = 0
        user_completed_task = 0
        user_overdue_task = 0
        for task in task_list:
            if user == task ["username"]:
                user_task += 1
                if not user in users_in_task_list:
                    users_in_task_list.append(user) 
                if task ["completed"]:
                    user_completed_task += 1
                    completed_task += 1
                else:
                    if today_date > task ["due_date"] and task ["completed"] == False:
                        user_overdue_task += 1
                        overdue_task += 1

            # An error handling if the user is in the 'user.txt' file but no task has been assigned.           
            try: 
                user_progress = round(100 * user_completed_task / user_task, 1)
            except ZeroDivisionError:
                user_progress = 0
            # An error handling if the user has completed all tasks.
            try:
                overdue_progress = round(100 * overdue_task / (total_task-completed_task))
            except ZeroDivisionError:
                overdue_progress = 0
            
                      
        #adding user's details to the 'user overview table'
        user_table.add_row([user, user_task, 
                            round(100 * user_task / total_task, 1),
                            user_progress, 100-user_progress, 
                            overdue_progress])
    #adding task summary to the 'task overview table'   
    overview_table.add_row([total_task, completed_task, total_task-completed_task,
                            round(100 * (total_task-completed_task) / total_task, 1 ),
                            overdue_task, round(100 * overdue_task / (total_task-completed_task), 1)])           
       
  
    #coverting table to string and store in a "task_overview.txt" file
    overview_string = overview_table.get_string()    
    with open("task_overview.txt", "w") as overview_file:
        overview_file.write(overview_string)
      
    #coverting table to string and store in a "user_overview.txt" file
    user_string = user_table.get_string()
    user_string += f"\nTotal Tasks:\t{total_task}\nTotal Task Users:\t{len(users_in_task_list)}"
    with open("user_overview.txt", "w") as user_file:
        user_file.write(user_string)
    
    print ("*" * 50 + "\nTask & Overview reports have been generated\n" + "*" * 50)           
            
        
        
#=====importing libraries===========

DATETIME_STRING_FORMAT = "%Y-%m-%d"


# get tasks and task lists from the functions.
task_data = get_tasks()
task_list = get_task_list()
#====Login Section====

# get users and their passwords from the function.
username_password  = get_users_detail()

logged_in = False
while not logged_in:
    """
    checks username and password if it doesn't match then sends warning messages
    
    """
    print("LOGIN")
    curr_user = input("Username: ").lower()
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

while True:
    # if the current user is 'admin' then shows gr - Generate reports & ds- Display statistic options
    if curr_user == "admin": 
        admin_menu_option = "gr - Generate reports\nds - Display statistics\ne - Exit"
    else:
    # presenting the menu to the users
        admin_menu_option = "e - Exit"
    print()
    menu = input(f'''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
{admin_menu_option}
: ''').lower()

    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_task()
    elif menu == 'vm':
        view_mine(user = curr_user)
    elif menu == 'ds' and curr_user == 'admin': 
        display_statistic()
    elif menu == 'gr' and curr_user == 'admin': 
        generate_reports()
    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    else:
        print("You have made a wrong choice, Please Try again")