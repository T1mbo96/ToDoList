from typing import List, Optional

from flask import Flask, render_template, Response, request, redirect, url_for

from config import Config
from models.entry import Entry, select_entries_by_to_do_list, insert_entry, delete_entry
from models.to_do_list import ToDoList, select_all_to_do_lists, delete_to_do_list, insert_to_do_list, \
    select_to_do_list_by_name, select_to_do_list_by_id

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=['GET'])
def index() -> Response:
    todolists: List[ToDoList] = select_all_to_do_lists()

    return render_template('index.html', todolists=todolists)


@app.route('/create/list', methods=['POST'])
def create_to_do_list() -> Response:
    name: Optional[str] = request.form.get('name', type=str)

    insert_to_do_list(name)

    return redirect(url_for('index'))


@app.route('/remove/list', methods=['POST'])
def remove_to_do_list() -> Response:
    pk: Optional[int] = request.form.get('pk', type=int)

    delete_to_do_list(pk)

    return redirect(url_for('index'))


@app.route('/list/<name>', methods=['GET'])
def list_entries(name: str) -> Response:
    todolist: Optional[ToDoList] = select_to_do_list_by_name(name)
    entries: List[Entry] = select_entries_by_to_do_list(todolist.pk)

    return render_template('list.html', todolist=todolist, entries=entries)


@app.route('/create/entry', methods=['POST'])
def create_entry() -> Response:
    content: Optional[str] = request.form.get('content', type=str)
    todolist: Optional[ToDoList] = select_to_do_list_by_id(request.form.get('todolist', type=int))

    insert_entry(content, todolist.pk)

    return redirect(url_for('list_entries', name=todolist.name))


@app.route('/remove/entry', methods=['POST'])
def remove_entry() -> Response:
    pk: Optional[int] = request.form.get('pk', type=int)
    todolist: Optional[ToDoList] = select_to_do_list_by_id(request.form.get('todolist', type=int))

    delete_entry(pk)

    return redirect(url_for('list_entries', name=todolist.name))


if __name__ == '__main__':
    app.run()
