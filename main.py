"""
Usage:
    todo <task_name>
    doing <task_id>
    done <task_id>
    edit <task_id>
    delete <task_id>
    list_todo
    list_doing
    list_done
    list_priority <priority_level>
    list_id
    quit

Options:
  -h --help     Show these commands.
"""

import os
import cmd
from docopt import DocoptExit, docopt
from app.todolist import Todo


def docopt_cmd(func):
    """
    source: https://github.com/docopt/docopt/blob/master/examples/interactive_example.py
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            print("Invalid Command!")
            print(e)
            return

        except SystemExit:
            # --help is printed by default
            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class Main(cmd.Cmd):
    os.system("clear")
    prompt = "Todo >>>"

    def __init__(self):
        super().__init__()
        self.todolist = Todo()

    @docopt_cmd
    def do_todo(self, args):
        """usage: todo <task_name>"""
        task_name = args["<task_name>"]
        details = input("Enter details: ")
        priority = input("Enter priority: ")
        print(self.todolist.todo(task_name, details, priority))

    @docopt_cmd
    def do_doing(self, args):
        """usage: doing <task_id> """
        task_id = args["<task_id>"]
        print(self.todolist.doing(task_id))

    @docopt_cmd
    def do_done(self, args):
        """usage: done <task_id>"""
        task_id = args["<task_id>"]
        print(self.todolist.done(task_id))

    @docopt_cmd
    def do_edit(self, args):
        """usage: edit <task_id>"""
        task_id = args["<task_id>"]
        print(self.todolist.edit_task(task_id))

    @docopt_cmd
    def do_delete(self, args):
        """usage: delete <task_id>"""
        task_id = args["<task_id>"]
        print(self.todolist.delete_task(task_id))

    @docopt_cmd
    def do_list_all(self, _):
        """usage: list_todo"""
        print(self.todolist.list_all())

    @docopt_cmd
    def do_list_priority(self, args):
        """usage: list_priority <priority_level>"""
        priority_level = args["<priority_level>"]
        print(self.todolist.list_priority(priority_level))

    @docopt_cmd
    def do_list_todo(self, _):
        """usage: list_todo"""
        print(self.todolist.list_todo())

    @docopt_cmd
    def do_list_doing(self, _):
        """usage: list_doing"""
        print(self.todolist.list_doing())

    @docopt_cmd
    def do_list_done(self, _):
        """usage: list_done"""
        print(self.todolist.list_done())

    def do_quit(self, _):
        """usage: exit"""
        print("Todo list closed.")
        exit()


if __name__ == "__main__":
    Main().cmdloop()
