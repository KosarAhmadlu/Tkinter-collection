from tkinter import *
import sqlite3

def connect():
    conn = sqlite3.connect('todo.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS todo (id INTEGER PRIMARY KEY, task TEXT, status TEXT)')
    conn.commit()
    conn.close()

def insert(task):
    conn = sqlite3.connect('todo.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO todo VALUES (NULL,?, ?)', (task, 'در حال انجام'))
    conn.commit()
    conn.close()

def view():
    conn = sqlite3.connect('todo.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM todo')
    rows = cur.fetchall()
    conn.close()
    return rows

def delete(id):
    conn = sqlite3.connect('todo.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM todo WHERE id=?', (id,))
    conn.commit()
    conn.close()

def mark_done(id):
    conn = sqlite3.connect('todo.db')
    cur = conn.cursor()
    cur.execute('UPDATE todo SET status=? WHERE id=?', ('انجام شده', id))
    conn.commit()
    conn.close()

task_ids = []  
def show_tasks():
    listbox.delete(0, END)
    task_ids.clear()
    for task in view():
        display_text = f"{task[1]}  [{task[2]}]"
        listbox.insert(END, display_text)
        task_ids.append(task[0])

def add_task():
    task = task_text.get()
    if task:
        insert(task)
        task_text.delete(0, END)
        show_tasks()

def delete_task():
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        task_id = task_ids[index]
        delete(task_id)
        show_tasks()

def mark_task_done():
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        task_id = task_ids[index]
        mark_done(task_id)
        show_tasks()

window = Tk()
window.title("مدیریت کارهای روزانه")

Label(window, text="کار جدید:").grid(row=0, column=0, padx=5, pady=5)

task_text = Entry(window, width=30)
task_text.grid(row=0, column=1, padx=5, pady=5)

Button(window, text="افزودن", width=12, command=add_task).grid(row=0, column=2, padx=5)

listbox = Listbox(window, width=50, height=15)
listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

Button(window, text="حذف", width=12, command=delete_task).grid(row=2, column=0, pady=5)
Button(window, text="انجام شد", width=12, command=mark_task_done).grid(row=2, column=1, pady=5)
Button(window, text="مشاهده همه", width=12, command=show_tasks).grid(row=2, column=2, pady=5)

connect()
show_tasks()
window.mainloop()
