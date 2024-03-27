# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
import sys
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"


#=====defining functions===========
def reg_user():
    """
    The `reg_user()` function adds a new user to the user.txt file by 
    requesting input for a new username, password, and password
    confirmation, and then checking if the passwords match before
    adding the user to the file.
    """
    # - Request input of a new username
    new_username = input("New Username: ")

    # - Check if the username already exists; if so, return a relevant message.
    if new_username in username_password:
        print("Username already exists. Please try a different one.")
        return

    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "w", encoding="utf-8") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do not match")


def add_task():
    """
    The `add_task` function allows a user to add a new task to a file,
    prompting for the following task details:
        - A username of the person whom the task is assigned to,
        - A title of a task,
        - A description of the task and 
        - the due date of the task.    
    and storing them in a structured format.
    """
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")


    # Then get the current date.
    curr_date = date.today()
    # Add the data to the file task.txt and
    # Include 'No' to indicate if the task is complete.
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w", encoding="utf-8") as task_file:
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
    print("Task successfully added.")


def view_all():
    """
    Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes 
        spacing and labelling) 
    """
    print("=" * 80)
    print()
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)
    print("=" * 80)


def view_mine():
    """
    The `view_mine` function reads tasks from task.txt file and prints 
    them to the console in a specific format.
    """
    print("=" * 80)
    print()
    for i, t in enumerate(task_list):
        if t['username'] == curr_user:
            disp_str = f"Task Number: \t {i + 1}\n"
            disp_str += f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            disp_str += f"Completed: \n {t['completed']}\n"
            print(disp_str)
    print("=" * 80)

    modify_task()


def modify_task():
    """
    The function `modify_task` allows the user to mark a task as
    complete or edit the task in a task list stored in a text file.
    """
    with open("tasks.txt", "r+", encoding="utf-8") as task_file:
        task_menu = """Please enter the number of the task you wish to select:
                    Otherwise, please input -1 to return to the main menu.\n"""
        task_selection = int(input(task_menu))
        if task_selection == -1:
            return

        else:
            edit_task = input("""Please select one of the following options:
                1. Mark the selected task complete
                2. Edit the task
                """)
            if edit_task == "1":
                task_list[task_selection - 1]['completed'] = True

            elif edit_task == "2":
                title = input("Please enter the new task: ")
                task_list[task_selection - 1]['title'] = f"{title}"

    # Updates the text file with the edited tasks
    with open("tasks.txt", "w", encoding="utf-8") as task_file:
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


def generate_reports():
    """
    The function `generate_reports` reads task information from a file,
    calculates various statistics such as total tasks, completed tasks,
    uncompleted tasks, and overdue tasks, and generates reports in text
    files for task overview and user overview.
    """

    # Create task_overview.txt if not already in existence
    if not os.path.exists("task_overview.txt"):
        with open("task_overview.txt", "w", encoding="utf-8") as task_overview_file:
            pass

    # Task Overview
    tasks_total = 0
    completed_tasks = 0
    uncompleted_tasks = 0
    overdue_tasks = 0
    uncompleted_percentage = 0
    overdue_percentage = 0

    with open("tasks.txt", "r+",encoding="utf-8") as task_file:
        lines = task_file.readlines()
        tasks_total = len(lines)

        data = []

        for line in lines:

            data = line.strip("\n").split(";")

            is_completed = data[5]

            if is_completed == "Yes":
                completed_tasks += 1

            else:
                uncompleted_tasks += 1

            current_date = datetime.now()
            deadline = datetime.strptime(data[3], "%Y-%m-%d")

            is_overdue = current_date > deadline

            if is_completed == "No" and is_overdue:
                overdue_tasks += 1

            # Percentage incomplete tasks calculation
            uncompleted_percentage = (uncompleted_tasks / tasks_total) * 100

            # Percentage of tasks that are overdue calculation
            overdue_percentage = (overdue_tasks / tasks_total) * 100

        # Write to task_overview.txt
        with open("task_overview.txt", "w", encoding="utf-8") as task_overview_file:
            task_overview_file.write("-" * 80)
            task_overview_file.write("\n")
            task_overview_file.write("Task Overview:\n")
            task_overview_file.write(f"The total number of tasks is:\t\t\t\t\t\t{tasks_total}\n")
            task_overview_file.write(f"The total number of completed tasks is:\t\t\t\t{completed_tasks}\n")
            task_overview_file.write(f"The total number of uncompleted tasks is:\t\t\t{uncompleted_tasks}\n")
            task_overview_file.write(f"The total number of tasks that are overdue is:\t\t{overdue_tasks}\n")
            task_overview_file.write(f"The percentage of tasks that are incomplete is:\t\t{uncompleted_percentage}%\n")
            task_overview_file.write(f"The percentage of tasks that are overdue is:\t\t{overdue_percentage}%\n")
            task_overview_file.write("-" * 80)

    # Create user_overview.txt if not already in existence
    if not os.path.exists("user_overview.txt"):
        with open("user_overview.txt", "w", encoding="utf-8") as default_file:
            pass

    # User Overview
    with open("tasks.txt", "r+",encoding="utf-8") as task_file:
        task_count = {}
        tasks_completed_count = {}
        tasks_uncompleted_count = {}
        tasks_overdue_count = {}
        tasks_not_overdue_count = {}
        percentage_user = 0
        completed_percentage_user = 0
        uncompleted_percentage_user = 0
        overdue_percentage_user = 0

        for line in task_file:
            task_info = line.strip().split(";")

            username = task_info[0]
            task_completion = task_info[5]
            current_date = datetime.now()
            task_due_date = datetime.strptime(task_info[3], "%Y-%m-%d")

            overdue = current_date > task_due_date

            if username not in task_count:
                task_count[username] = 1
                tasks_completed_count[username] = 0
                tasks_uncompleted_count[username] = 0
                tasks_overdue_count[username] = 0
                tasks_not_overdue_count[username] = 0
            else:
                task_count[username] += 1

            if task_completion == "Yes":
                tasks_completed_count[username] += 1
            else:
                tasks_uncompleted_count[username] +=1


            if task_completion == "No" and overdue:
                tasks_overdue_count[username] +=1

        # Write to user_overview.txt
        with open("user_overview.txt", "w", encoding="utf-8") as user_overview_file:
            num_users = len(username_password.keys())
            num_tasks = len(task_list)

            user_overview_file.write("-" * 80)
            user_overview_file.write("\n")
            user_overview_file.write(f"Number of users: \t\t {num_users}\n")
            user_overview_file.write(f"Number of tasks: \t\t {num_tasks}")
            user_overview_file.write("\n")

            for user in task_count:
                user_overview_file.write("-" * 80)
                user_overview_file.write("\n")
                user_overview_file.write(f"Username: {user}\n")
                user_overview_file.write(f"Total number of tasks assigned to user: {task_count[user]}\n")
                percentage_user = (task_count[user] / tasks_total) * 100
                user_overview_file.write(f"Percentage of the total number of tasks, assigned to this user: {percentage_user}\n")
                user_overview_file.write("\n")
                user_overview_file.write("Percentage of tasks assigned to user:\n")
                completed_percentage_user = (tasks_completed_count[user] / task_count[user]) * 100
                user_overview_file.write(f"Completed: {completed_percentage_user}%\n")
                uncompleted_percentage_user = (tasks_uncompleted_count[user] / task_count[user]) * 100
                user_overview_file.write(f"Uncompleted: {uncompleted_percentage_user}%\n")
                overdue_percentage_user = (tasks_overdue_count[user] / task_count[user]) * 100
                user_overview_file.write(f"\tOverdue: {overdue_percentage_user}%\n")
            user_overview_file.write("-" * 80)


# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w", encoding="utf-8") as default_file:
        pass

with open("tasks.txt", 'r', encoding="utf-8") as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


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


#====Login Section====
# This code reads usernames and password from the user.txt file to
# allow a user to login.

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w", encoding="utf-8") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r', encoding="utf-8") as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(',')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
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
    # Presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Please select one of the following options below:
r - Register a user
a - Add a task
va - View all tasks
vm - View my tasks
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()

    elif menu == 'gr' and curr_user == 'admin':
        # If the user is an admin they can generate reports on the
        # number of users and tasks in the system.
        generate_reports()

    elif menu == 'ds' and curr_user == 'admin':
        # If the user is an admin they can display statistics about
        # the number of users and tasks in the system.

        with open("task_overview.txt", "r", encoding="utf-8") as task_overview_file:
            task_stats = task_overview_file.read()
            print(task_stats)

        with open("user_overview.txt", "r", encoding="utf-8") as user_overview_file:
            user_stats = user_overview_file.read()
            print(user_stats)

    elif menu == 'e':
        sys.exit('Goodbye!!!')

    else:
        print("You have made a wrong choice, Please Try again")
