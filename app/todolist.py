import sqlite3
import os
from datetime import datetime
import tabulate


def connect(filename):
    is_existing = os.path.exists(filename)
    db = sqlite3.connect("todolist.db")
    cursor = db.cursor()
    if not is_existing:
        cursor.execute(
            "CREATE TABLE Task ("
            "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
            "Name TEXT NOT NULL,"
            "Details TEXT NOT NULL,"
            "Priority INTEGER NOT NULL,"
            "Status TEXT NOT NULL,"
            "Start DATETIME,"
            "Finish DATETIME,"
            "Duration DATETIME);"
        )
    return db


class Todo:
    def __init__(self):
        self.db = connect("todolist.db")
        self.cursor = self.db.cursor()

    def todo(self, task_name, task_details, task_priority):
        self.cursor.execute(
            "INSERT INTO Task(Name, Details, Status, Priority)VALUES(?,?,?,?)",
            (task_name, task_details, "Todo", task_priority),
        )
        self.db.commit()
        return f"'{task_name.title()}' has been created"

    def doing(self, task_id):
        self.cursor.execute(f"SELECT Status FROM Task WHERE ID = {task_id}")
        results = self.cursor.fetchone()
        if results:
            status = results[0]
            if status == "Todo":
                try:
                    self.cursor.execute(
                        "UPDATE Task SET Status ='Doing',Start='{0}' WHERE ID = {1}".format(
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), task_id
                        )
                    )
                    self.db.commit()
                    return f"Task {task_id} has been updated"
                except sqlite3.OperationalError:
                    print("Invalid task ID!")

            elif status == "Doing":
                return "You are already doing this task"

            elif status == "Done":
                try:
                    self.cursor.execute(
                        "UPDATE Task SET Status ='Doing',Start='{0}', Finish='NULL' WHERE ID = {1}".format(
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), task_id
                        )
                    )
                    self.db.commit()
                    return f"Task with ID {task_id} has been successfully updated!"
                except sqlite3.OperationalError as err:
                    return f"{err}"
            return "Invalid task status"
        return "Invalid task status"

    def done(self, task_id):
        self.cursor.execute(f"SELECT Status FROM Task WHERE ID = {task_id}")
        results = self.cursor.fetchone()
        if results:
            status = results[0]
            if status == "Doing":
                try:
                    self.cursor.execute(f"SELECT Start FROM Task WHERE ID={task_id}")
                    start_time = datetime.strptime(
                        self.cursor.fetchone()[0], "%Y-%m-%d %H:%M:%S"
                    )
                    finish_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    duration = (
                        datetime.strptime(finish_time, "%Y-%m-%d %H:%M:%S") - start_time
                    )
                    self.cursor.execute(
                        "UPDATE Task SET Status='Done', Finish='{0}', Duration='{1}'  WHERE ID = {2}".format(
                            finish_time, duration, task_id
                        )
                    )
                    self.db.commit()
                    return f"Task with ID {task_id} has successfully been completed!"
                except sqlite3.OperationalError:
                    return "unknown task ID"
            if status == "Done":
                return "Task has already been completed"
            return "The task specified is still on the todo list: try changing it's status first"
        return "Invalid task status"

    def list_all(self):
        self.cursor.execute("SELECT ID, Name, Details, Status, Priority FROM Task")
        results = self.cursor.fetchall()
        if results:
            headers = ["ID", "Name", "Details", "Status", "Priority"]
            return tabulate.tabulate(results, headers, tablefmt="fancy_grid")
        return "No tasks added yet! please add some tasks and try again"

    def list_todo(self):
        self.cursor.execute(
            "SELECT ID, Name, Details, Priority FROM Task WHERE Status='Todo'"
        )
        results = self.cursor.fetchall()
        if results:
            headers = ["ID", "Name", "Details", "Priority"]
            return tabulate.tabulate(results, headers, tablefmt="fancy_grid")
        return "No tasks pending"

    def list_doing(self):
        self.cursor.execute(
            "SELECT ID, Name, Details, Priority, Start FROM Task WHERE Status='Doing'"
        )
        results = self.cursor.fetchall()
        if results:
            headers = ["ID", "Name", "Details", "Priority", "Start Time"]
            return tabulate.tabulate(results, headers, tablefmt="fancy_grid")
        return "No tasks are being worked on currently"

    def list_done(self):
        self.cursor.execute(
            "SELECT ID, Name, Details, Priority, Start, Finish, Duration FROM Task WHERE Status='Done'"
        )
        results = self.cursor.fetchall()
        if results:
            headers = [
                "ID",
                "Name",
                "Details",
                "Priority",
                "Started on",
                "Finished on",
                "Duration",
            ]
            return tabulate.tabulate(results, headers, tablefmt="fancy_grid")
        return "No tasks are being worked on currently!"

    def list_priority(self, priority_level):
        self.cursor.execute(
            f"SELECT ID, Name, Details, Priority, Start FROM Task WHERE Priority = {priority_level}"
            )
        results = self.cursor.fetchall()
        if results:
            headers = [
                "ID",
                "Name",
                "Details",
                "Priority",
                "Started on",
                "Duration",
            ]
            return tabulate.tabulate(results, headers, tablefmt="fancy_grid")
        return "No tasks matching this priority level"

    def edit_task(self, task_id):
        self.cursor.execute(f"SELECT Name, Details FROM Task WHERE ID={task_id}")
        results = self.cursor.fetchone()
        if results:
            new_name = input("Enter task name: ")
            new_details = input("Task details: ")
            new_priority = input("Task priority: ")
            if new_details and new_name and new_priority:
                self.cursor.execute(
                    'UPDATE Task SET Name = \'{}\', Details = "{}", Priorty = "{}", WHERE ID = {}'.format(
                        new_name, new_details, new_priority, task_id
                    )
                )
                self.db.commit()
                return "Task has been edited successfully!!"
            return "A task name is required"
        return "Task not found!"

    def delete_task(self, task_id):
        self.cursor.execute(f"SELECT Name FROM Task WHERE ID = {task_id}")
        result = self.cursor.fetchone()
        if result:
            self.cursor.execute(f"DELETE FROM Task WHERE ID = {task_id}")
            self.db.commit()
            return f"Task to '{result[0]}' with ID '{task_id}' has been deleted"
        return "Task not found!"
