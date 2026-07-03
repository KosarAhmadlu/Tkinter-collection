from tkinter import *
import sqlite3

# اتصال به دیتابیس
conn = sqlite3.connect("contacts.db")
cursor = conn.cursor()

# ساخت جدول
cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT
)
""")
conn.commit()


# ذخیره مخاطب
def add_contact():
    name = entry_name.get()
    phone = entry_phone.get()

    if name != "" and phone != "":
        cursor.execute(
            "INSERT INTO contacts (name, phone) VALUES (?, ?)",
            (name, phone)
        )

        conn.commit()

        entry_name.delete(0, END)
        entry_phone.delete(0, END)

        show_contacts()


# نمایش همه مخاطبین
def show_contacts():
    listbox.delete(0, END)

    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()

    for row in rows:
        listbox.insert(
            END,
            f"{row[0]} | {row[1]} | {row[2]}"
        )


# حذف مخاطب
def delete_contact():
    selected = listbox.curselection()

    if selected:
        item = listbox.get(selected[0])

        contact_id = item.split("|")[0].strip()

        cursor.execute(
            "DELETE FROM contacts WHERE id=?",
            (contact_id,)
        )

        conn.commit()

        show_contacts()


# ویرایش مخاطب
def edit_contact():
    selected = listbox.curselection()

    if selected:
        item = listbox.get(selected[0])

        contact_id = item.split("|")[0].strip()

        new_name = entry_name.get()
        new_phone = entry_phone.get()

        cursor.execute(
            "UPDATE contacts SET name=?, phone=? WHERE id=?",
            (new_name, new_phone, contact_id)
        )

        conn.commit()

        entry_name.delete(0, END)
        entry_phone.delete(0, END)

        show_contacts()


# جستجو
def search_contact():
    name = entry_search.get()

    listbox.delete(0, END)

    cursor.execute(
        "SELECT * FROM contacts WHERE name LIKE ?",
        ('%' + name + '%',)
    )

    rows = cursor.fetchall()

    for row in rows:
        listbox.insert(
            END,
            f"{row[0]} | {row[1]} | {row[2]}"
        )


# پنجره اصلی
root = Tk()

root.title("دفترچه تلفن ساده")
root.geometry("550x450")



# نام
Label(
    root,
    text="نام",
    font=("B Nazanin", 12)
).grid(row=0, column=0, pady=10)

entry_name = Entry(root,width=20)
entry_name.grid(row=0, column=1, pady=10)


# شماره
Label(
    root,
    text="شماره",
    font=("B Nazanin", 12)
).grid(row=1, column=0, padx=10, pady=10)

entry_phone = Entry(root,width=20)
entry_phone.grid(row=1, column=1, padx=10, pady=10)


# دکمه‌ها
Button(
    root,
    text="ذخیره مخاطب",
    width=12,
    bg="SteelBlue1",
    command=add_contact
).grid(row=2, column=0, pady=10, padx=5)

Button(
    root,
    text="حذف مخاطب",
    width=12,
    bg="SteelBlue1",
    command=delete_contact
).grid(row=2, column=1, pady=10, padx=5)

Button(
    root,
    text="ویرایش",
    width=12,
    bg="SteelBlue1",
    command=edit_contact
).grid(row=2, column=2, pady=10, padx=5)

Button(
    root,
    text="نمایش همه",
    width=12,
    bg="SteelBlue1",
    command=show_contacts).grid(row=2, column=3, pady=10, padx=15)


# لیست باکس
listbox = Listbox(root, width=54, height=15)
listbox.grid(
    row=3,
    column=0,
    columnspan=3,
    padx=50,
    pady=10
)


# جستجو
Label(root,text='جستجو:').grid(row=4,column=0)
entry_search = Entry(root,width=25)
entry_search.grid(
    row=4,
    column=1,
    columnspan=1,
    pady=10
)

Button(
    root,
    text="جستجو",
    width=12,
    bg='SteelBlue1',
    command=search_contact).grid(row=4, column=2, pady=10, padx=30)


# نمایش اولیه
show_contacts()

root.mainloop()

conn.close()
