from dataclasses import dataclass
from datetime import datetime
from sqlite3 import connect
from typing import Tuple, Optional, List

from consts import DB_NAME
from models.to_do_list import ToDoList, select_to_do_list_by_id

EntryTuple = Tuple[int, str, str, int]


@dataclass()
class Entry:
    pk: int
    content: str
    timestamp: str
    todolist: int

    @staticmethod
    def __from_entry_tuple__(et: EntryTuple) -> 'Entry':
        return Entry(et[0], et[1], et[2], et[3])

    def __repr__(self):
        todlist: ToDoList = select_to_do_list_by_id(self.todolist)

        return f'<Entry {self.content}> of {todlist}'


def insert_entry(content: str, todolist: int):
    sql = 'INSERT INTO entries (content, timestamp, todolist) VALUES (?, ?, ?);'

    with connect(DB_NAME) as connection:
        connection.execute(sql, [content, datetime.now(), todolist])


def select_entry_by_id(pk: int) -> Optional[Entry]:
    sql = 'SELECT pk, content, timestamp, todolist FROM entries WHERE pk = ?;'

    with connect(DB_NAME) as connection:
        entry: EntryTuple = connection.execute(sql, [pk]).fetchone()

        if entry:
            return Entry.__from_entry_tuple__(entry)


def select_entries_by_to_do_list(todolist: int) -> List[Entry]:
    sql = 'SELECT pk, content, timestamp, todolist FROM entries WHERE todolist = ?;'

    with connect(DB_NAME) as connection:
        entries: List[EntryTuple] = connection.execute(sql, [todolist]).fetchall()

        return [Entry.__from_entry_tuple__(entry) for entry in entries]


def update_entry(pk: int, content: str, todolist: int):
    sql = 'UPDATE entries SET content = ?, timestamp = ?, todolist = ? WHERE pk = ?;'

    with connect(DB_NAME) as connection:
        connection.execute(sql, [content, datetime.now(), todolist, pk])


def delete_entry(pk: int):
    sql = 'DELETE FROM entries WHERE pk = ?;'

    with connect(DB_NAME) as connection:
        connection.execute(sql, [pk])
