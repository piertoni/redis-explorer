#!/usr/bin/env python3
import sys
import pathlib
import argparse

from tkinter import Tk, Text, StringVar
from tkinter import ttk

import redis


"""
Some tkinter recaps...

tree.insert('', 'end', name, text="f{name}"  # insert at the root
tree.insert('', 0, ...)  # insert at first child

id_ = tree.insert(...)  # getting id
tree.insert('parent', ...)  # insert after an existing parent
tree.insert(id, ...)  # insert after an existing id
"""

FONT = "Times New Roman"


def fill_tree(iterable, tree):
    tree.delete(*tree.get_children())
    ids = {}
    for key in sorted(iterable):
        values = (iterable[key].decode(),)
        text = key.decode()
        id_ = tree.insert("", "end", text=text, values=values)
        ids[key] = id_
    return ids


def main(args=None):

    conn_params = get_conn_params()

    master = Tk()
    master.title("Redis Explorer")
    master.geometry("700x900")

    ttk.Label(text="Filter", font=(FONT, 16)).pack()
    filter_text = StringVar()
    filter_ = ttk.Entry(master, textvariable=filter_text)
    filter_.pack()

    ttk.Label(text="Keys", font=(FONT, 16)).pack()
    tree = ttk.Treeview(master)
    tree["columns"] = "type"
    tree.heading("type", text="type")
    tree.heading("#0", text="key")
    tree.pack(fill="both", expand=1)

    ttk.Label(text="Content", font=(FONT, 16)).pack()
    tree_content = ttk.Treeview(master)
    tree_content["columns"] = ("value",)
    tree_content.pack(fill="both", expand=1)

    _cnx = redis.StrictRedis(**conn_params)
    info = {k: _cnx.type(k) for k in _cnx.keys()}

    def apply_filter(arg1, arg2, arg3):
        """will apply filter on the main tree"""
        # 'PY_VAR0', '', 'w'
        filter_ = filter_text.get()
        if filter_:
            _info = {k: v for k, v in info.items() if filter_ in k.decode()}
            fill_tree(_info, tree)

    fill_tree(info, tree)

    def selectItem(event):
        """On selecting an item will filter the content tree"""
        # <ButtonRelease event state=Mod2|Button1|0x2000 num=1 x=199 y=171>

        curItem = tree.focus()
        item_data = tree.item(curItem)

        # example of item_data
        # item_data = {'text': 'axis.dacm2', 'image': '', 'values': ['hash'], 'open': 0, 'tags': ''}
        key = item_data["text"].encode()

        tree_content.delete(*tree_content.get_children())

        type_ = item_data["values"][0]
        # set heading
        if type_ in ("hash", "zset"):
            tree_content.heading("#0", text="key")
            tree_content.heading("#1", text="value")
        else:
            tree_content.heading("#0", text="value")
            tree_content.heading("#1", text="")

        # read every item with proper method
        if type_ == "hash":
            data = _cnx.hgetall(key)
            for k, v in data.items():
                tree_content.insert("", "end", text=k.decode(), values=(v,))
        if type_ == "list":
            data = _cnx.lrange(key, 0, -1)
            for v in data:
                tree_content.insert("", "end", text=v.decode(), values=("",))
        if type_ == "set":
            data = _cnx.smembers(key)
            for v in data:
                tree_content.insert("", "end", text=v.decode(), values=("",))
        if type_ == "string":
            data = _cnx.getrange(key, 0, -1)
            tree_content.insert("", "end", text=data.decode(), values=("",))
        if type_ == "zset":
            data = _cnx.zrange(key, 0, -1, withscores=True)
            for k, v in data:
                tree_content.insert("", "end", text=k.decode(), values=(v,))

    # bindings
    tree.bind("<ButtonRelease-1>", selectItem)
    filter_text.trace("w", apply_filter)

    master.mainloop()


def get_conn_params():
    parser = argparse.ArgumentParser("Redis database explorer")
    parser.add_argument("--host", type=str, dest="host", default="0.0.0.0")
    parser.add_argument("--port", type=int, dest="port", default=6379)
    parser.add_argument("--db", type=int, dest="database", default=0)
    parser.add_argument("--pw", type=str, dest="password")

    args = parser.parse_args()

    conn_params = {"host": args.host, "port": args.port, "db": args.database}
    if args.password:
        conn_params["password"] = args.password

    return conn_params


if __name__ == "__main__":
    main()
