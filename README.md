# Overview
This is a Todo list app that is run via the command line. Tasks can be added, edited, removed along with a status of todo/doing/done. It is possible ot list all tasks, as well as listing by priority or status with using the commands listed below.

![IMG](https://github.com/john-lock/todo-cmd/blob/dev/todo_listall.png)


# Instructions
Run the applicaiton with `python main.py`

Application commands:
Create new task (details and then priority will be prompted):
`>>> todo <task_name>`

Mark task as in progress:
`>>> doing <task_id>`

Mark task as done:
`>>> done <task_id>`

Edit task:
`>>> edit <task_id>`

Delete task:
`>>> delete <task_id>`

List todo tasks:
`>>> list_todo`

List in progress tasks:
`>>> list_doing`

List completed tasks:
`>>> list_done`

List tasks which have a certain priority level:
`>>> list_priority <priority_level>`

Quit application:
`>>> quit`

Help flag to show commands:
`>>> --help`


# Installation
Clone this repo with `git clone `
Setup the virtual environment with: `virtualvenv venv` and then `source venv/bin/activate` to activate
Install the dependencies with `pip install -r requirements.txt`
Finally run the application with: `python main.py`. The DB will be created if not found already from a previous session. 


# Tests
Tests are run with `pytest` and found in `test_todo.py`

# Further development
- Add support for multi word task names without editing them in.
- Next step targeted is to better integrate the priority of tasks with High/Medium/Low options. 
- Add command to clear all done tasks (delete or archieve them)
