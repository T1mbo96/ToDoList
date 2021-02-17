from dataclasses import dataclass
from datetime import datetime
from sqlite3 import connect
from typing import Tuple, Optional, List

from consts import DB_NAME

ToDoListTuple = Tuple[int, str, str]


@dataclass()
class ToDoList:
    pk: int
    name: str
    timestamp: str

    @staticmethod
    def __from_to_do_list_tuple__(tdlt: ToDoListTuple) -> 'ToDoList':
        return ToDoList(tdlt[0], tdlt[1], tdlt[2])

    def __repr__(self):
        return f'<ToDoList "{self.name}">'


def insert_to_do_list(name: str):
    sql = 'INSERT INTO todolists (name, timestamp) VALUES(?, ?);'

    with connect(DB_NAME) as connection:
        connection.execute(sql, [name, datetime.now()])


def select_to_do_list_by_id(pk: int) -> Optional[ToDoList]:
    sql = 'SELECT pk, name, timestamp FROM todolists WHERE pk = ?;'

    with connect(DB_NAME) as connection:
        todolist: ToDoListTuple = connection.execute(sql, [pk]).fetchone()

        if todolist:
            return ToDoList.__from_to_do_list_tuple__(todolist)


def select_to_do_list_by_name(name: str) -> Optional[ToDoList]:
    sql = 'SELECT pk, name, timestamp FROM todolists WHERE name = ?;'

    with connect(DB_NAME) as connection:
        todolist: ToDoListTuple = connection.execute(sql, [name]).fetchone()

        return ToDoList.__from_to_do_list_tuple__(todolist)


def select_all_to_do_lists() -> List[ToDoList]:
    sql = 'SELECT pk, name, timestamp FROM todolists;'

    with connect(DB_NAME) as connection:
        todolists: List[ToDoListTuple] = connection.execute(sql).fetchall()

        return [ToDoList.__from_to_do_list_tuple__(todolist) for todolist in todolists]


def update_to_do_list(pk: int, name: str):
    sql = 'UPDATE todolists SET name = ?, timestamp = ? WHERE pk = ?;'

    with connect(DB_NAME) as connection:
        connection.execute(sql, [name, datetime.now(), pk])


def delete_to_do_list(pk: int):
    sql = 'DELETE FROM todolists WHERE pk = ?;'

    with connect(DB_NAME) as connection:
        connection.execute(sql, [pk])
