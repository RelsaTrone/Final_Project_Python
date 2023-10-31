import tkinter as tk
from tkinter import ttk
import sqlite3


# Класс Main
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

# Главное окно
    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='add.png')
        btn_open_dialog = tk.Button(toolbar, text='Добавить ',
                                    command=self.open_dialog, bg='#d7d8e0',
                                    bd=0, compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='edit.png')
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='#d7d8e0',
                                    bd=0, image=self.update_img,
                                    compound=tk.TOP,
                                    command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='delete.png')
        btn_delete = tk.Button(toolbar, text='Удалить', bg='#d7d8e0',
                               bd=0, image=self.delete_img,
                               compound=tk.TOP,
                               command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='search.png')
        btn_search = tk.Button(toolbar, text='Поиск', bg='#d7d8e0', bd=0,
                               image=self.search_img, compound=tk.TOP,
                               command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='refresh.png')
        btn_refresh = tk.Button(toolbar, text='Обновить', bg='#d7d8e0', bd=0,
                                image=self.refresh_img,
                                compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'employee', 'salary', 'phone', 'email'),
                                 height=15, show='headings')
        
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=200, anchor=tk.CENTER)
        self.tree.column('employee', width=100, anchor=tk.CENTER)
        self.tree.column('salary', width=80, anchor=tk.CENTER)
        self.tree.column('phone', width=100, anchor=tk.CENTER)
        self.tree.column('email', width=100, anchor=tk.CENTER)
          
        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('employee', text='Должность')
        self.tree.heading('salary', text='Зарплата')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='E-mail')

        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

# Добавление данных
    def records(self, name, employee, salary, phone, email):
        self.db.insert_data(name, employee, salary, phone, email)
        self.view_records()

# Обновление данных
    def update_record(self, name, employee, salary, phone, email):
        self.db.c.execute('''UPDATE users SET name=?,
                        employee=?, salary=?, phone=?, email=?
                          WHERE ID=?''',
                          (name, employee, salary, phone, email,
                           self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

# Вывод данных
    def view_records(self):
        self.db.c.execute('''SELECT * FROM users''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=i) for i in self.db.c.fetchall()]

# Удаление данных
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM users WHERE id=? ''',
                              (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

# Поиск данных
    def search_records(self, employee):
        self.db.c.execute('''SELECT * FROM users WHERE employee LIKE ?''',
                          ("%" + employee + "%", ))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

# Открытие дочернего окна
    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()


# Дочернее окно
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить сотрудника')
        self.geometry('400x250+400+300')
        self.resizable(False, False)

        label_name = tk.Label(self, text='ФИО ')
        label_name.place(x=50, y=50)
        
        label_employee = tk.Label(self, text='Должность ')
        label_employee.place(x=50, y=80)

        label_salary = tk.Label(self, text='Зарплата ')
        label_salary.place(x=50, y=110)

        label_phone = tk.Label(self, text='Телефон ')
        label_phone.place(x=50, y=140)

        label_email = tk.Label(self, text='E-mail ')
        label_email.place(x=50, y=170)
        
        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=200, y=50)

        self.entry_employee = tk.Entry(self)
        self.entry_employee.place(x=200, y=80)

        self.entry_salary = tk.Entry(self)
        self.entry_salary.place(x=200, y=110)

        self.entry_phone = tk.Entry(self)
        self.entry_phone.place(x=200, y=140)

        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=200, y=170)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=200)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=200)
        self.btn_ok.bind('<Button-1>',
                         lambda event: self.view.records(self.entry_name.get(),
                                                         self.entry_employee.get(),
                                                         self.entry_salary.get(),
                                                         self.entry_phone.get(),
                                                         self.entry_email.get()))

        self.grab_set()
        self.focus_set()

# Класс обновления унаследованный от дочернего окна
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()


    def init_edit(self):
        self.title('Редактировать сотрудников')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=200)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_name.get(),
                                                                          self.entry_employee.get(),
                                                                          self.entry_salary.get(),
                                                                          self.entry_phone.get(),
                                                                          self.entry_email.get()))
        self.btn_ok.destroy()


    def default_data(self):
        self.db.c.execute('''SELECT * FROM users WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_employee.insert(0, row[2])
        self.entry_salary.insert(0, row[3])
        self.entry_phone.insert(0, row[4])
        self.entry_email.insert(0, row[5])
        


# Поиск по наименованию
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>',
                        lambda event: self.view.search_records(
                            self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


# Создание базы данных
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.c = self.conn.cursor()
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS users (
                         id INTEGER PRIMARY KEY,
                         name TEXT,
                         employee TEXT,
                         salary TEXT,
                         phone INTEGER,
                         email TEXT
        )""")
        self.conn.commit()

    def insert_data(self, name, employee, salary, phone, email):
        self.c.execute("""
                         INSERT INTO users (name, employee, salary, phone, email)
                         Values (?, ?, ?, ?, ?)""", (name, employee, salary, phone, email))
        self.conn.commit()


# Основной код для запуска
if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Список сотрудников")
    root.geometry("800x450+300+200")
    root.resizable(False, False)
    root.mainloop()
