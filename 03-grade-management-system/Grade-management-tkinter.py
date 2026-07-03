import sqlite3
from tkinter import *
from tkinter import ttk

# ==========================
# دیتابیس
# ==========================
conn = sqlite3.connect("students.db")
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                book TEXT,
                score REAL,
                grade TEXT
            )''')
conn.commit()

# ==========================
# وضعیت نمره
# ==========================
def get_grade(score):
    if score > 17:
        return "عالی"
    elif score >= 14:
        return "خوب"
    elif score >= 10:
        return "متوسط"
    elif score >= 5:
        return "ضعیف"
    else:
        return "خیلی ضعیف"

# ==========================
# افزودن نمره
# ==========================
def add_score():
    name = name_entry.get()
    book = book_entry.get()
    score = float(score_entry.get())

    grade = get_grade(score)

    c.execute(
        "INSERT INTO grades (name, book, score, grade) VALUES (?, ?, ?, ?)",
        (name, book, score, grade)
    )
    conn.commit()

    name_entry.delete(0, END)
    book_entry.delete(0, END)
    score_entry.delete(0, END)

    display_scores()

# ==========================
# نمایش داده‌ها
# ==========================
def display_scores():
    for row in tree.get_children():
        tree.delete(row)

    c.execute("SELECT * FROM grades")
    for row in c.fetchall():
        tree.insert("", END, values=row)

# ==========================
# حذف نمره
# ==========================
def delete_score():
    selected = tree.selection()

    for item in selected:
        c.execute("DELETE FROM grades WHERE id=?",
                  (tree.item(item)["values"][0],))

    conn.commit()
    display_scores()

# ==========================
# رابط گرافیکی
# ==========================
root = Tk()
root.title("ثبت نمرات دانش آموزان")
root.geometry("500x400")

# فریم ورودی
input_frame = LabelFrame(root, text="ثبت نمره جدید")
input_frame.pack(fill=X, padx=10, pady=10)

Label(input_frame, text="نام دانش‌آموز:").grid(row=0, column=0, padx=5, pady=5)
name_entry = Entry(input_frame)
name_entry.grid(row=0, column=1)

Label(input_frame, text="نام درس:").grid(row=1, column=0, padx=5, pady=5)
book_entry = Entry(input_frame)
book_entry.grid(row=1, column=1)

Label(input_frame, text="نمره:").grid(row=2, column=0, padx=5, pady=5)
score_entry = Entry(input_frame)
score_entry.grid(row=2, column=1)

# دکمه‌ها
Button(input_frame, text="ثبت نمره", bg="green", fg="white",
       command=add_score,width=10).grid(row=0, column=2, padx=40)

Button(input_frame, text="حذف", bg="red", fg="white",
       command=delete_score,width=10).grid(row=1, column=2, padx=40)

# جدول
columns = ("id", "name", "book", "score", "grade")

tree = ttk.Treeview(root, columns=columns, show="headings")

tree.heading("id", text="ID")
tree.heading("name", text="نام")
tree.heading("book", text="درس")
tree.heading("score", text="نمره")
tree.heading("grade", text="وضعیت")

tree.column("id", width=30)
tree.column("name", width=120)
tree.column("book", width=120)
tree.column("score", width=70)
tree.column("grade", width=100)

tree.pack(fill=BOTH, expand=True)

display_scores()

root.mainloop()

conn.close()
