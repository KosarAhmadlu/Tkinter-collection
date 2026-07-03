from tkinter import *
import sqlite3

# Database operations
def connect():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, isbn INTEGER)")
    conn.commit()
    conn.close()

def insert(title, author, year, isbn):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO book VALUES (NULL, ?, ?, ?, ?)", (title, author, year, isbn))
    conn.commit()
    conn.close()

def view():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM book")
    rows = cur.fetchall()
    conn.close()
    return rows

def search(title="", author="", year="", isbn=""):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM book WHERE title=? OR author=? OR year=? OR isbn=?", (title, author, year, isbn))
    rows = cur.fetchall()
    conn.close()
    return rows

def delete(id):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM book WHERE id=?", (id,))
    conn.commit()
    conn.close()

def update(id, title, author, year, isbn):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("UPDATE book SET title=?, author=?, year=?, isbn=? WHERE id=?", (title, author, year, isbn, id))
    conn.commit()
    conn.close()

# GUI Operations
def view_command():
    listbox.delete(0, END)
    for row in view():
        listbox.insert(END, row)

def search_command():
    listbox.delete(0, END)
    for row in search(title_text.get(), author_text.get(), year_text.get(), isbn_text.get()):
        listbox.insert(END, row)

def add_command():
    insert(title_text.get(), author_text.get(), year_text.get(), isbn_text.get())
    listbox.delete(0, END)
    listbox.insert(END, (title_text.get(), author_text.get(), year_text.get(), isbn_text.get()))


def delete_command():
    selected = listbox.curselection()
    if selected:
        item = listbox.get(selected[0])[0]  
        delete(item)                  
        view_command()                   

def close_command():
    window.destroy()

# GUI Design
window = Tk()
window.title("مديريت کتابخانه")

Label(window, text="عنوان").grid(row=0, column=0)
Label(window, text="نويسنده").grid(row=0, column=2)
Label(window, text="سال").grid(row=1, column=0)
Label(window, text="ISBN").grid(row=1, column=2)

title_text = Entry(window)
title_text.grid(row=0, column=1)

author_text = Entry(window)
author_text.grid(row=0, column=3)

year_text = Entry(window)
year_text.grid(row=1, column=1)

isbn_text = Entry(window)
isbn_text.grid(row=1, column=3)

listbox = Listbox(window, height=10, width=40)
listbox.grid(row=2, column=0, rowspan=6, columnspan=2)

scrollbar = Scrollbar(window)
scrollbar.grid(row=2, column=2, rowspan=6)

listbox.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=listbox.yview)


Button(window, text="مشاهده همه", width=12, command=view_command).grid(row=2, column=3)
Button(window, text="جستجوي کتاب", width=12, command=search_command).grid(row=3, column=3)
Button(window, text="اضافه کردن کتاب", width=12, command=add_command).grid(row=4, column=3)
Button(window, text="حذف کردن", width=12, command=delete_command).grid(row=6, column=3)
Button(window, text="بستن", width=12, command=close_command).grid(row=7, column=3)
connect()
window.mainloop()



