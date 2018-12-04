import os
import unittest
import sqlite3
from app import todolist


class test_TodoDB(unittest.TestCase):
    """
    Test Todo Database
    """

    def setUp(self):
        self.conn = sqlite3.connect("testtodo.db")
        cursor = self.conn.cursor()
        cursor.execute("")

        # create table
        cursor.execute(
            "CREATE TABLE Task ("
            "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
            "Name TEXT NOT NULL,"
            "Details TEXT NOT NULL,"
            "Priority INTEGER NOT NULL,"
            "Status TEXT NOT NULL);"
        )

        # insert data
        tasks = [('1', 'refactor','Refactor sub-functions for DRY','1','Todo'),
                ('2', 'test','Expand to cover new feature integrations','2','Doing')]

        cursor.executemany("INSERT INTO Task VALUES (?,?,?,?,?)",
                           tasks)

        self.conn.commit()

    def tearDown(self):
        os.remove('testtodo.db')

    def test_todo(self):
        actual = todolist.Todo.list_all()
        expected = 'done'
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()


"""
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
"""
