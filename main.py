import sqlite3
import tkinter as tk
from tkinter import ttk

#Класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view()
    
    #Метод вызывающий дочернее окно
    def open_child(self):
        Child()

    def open_update_child(self):
        Update()

    def open_search(self):
        Search() 

    #Инициализация виджетов
    def init_main(self):
        toolbar = tk.Frame(bg='gray75', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
 
        #Кнопка обновления
        self.img_ref = tk.PhotoImage(file='img/refresh.png')
        btn_ref = tk.Button(toolbar, text='Обновить', bg='gray75',
                             bd = 0, image = self.img_ref,
                            command=self.view)
        btn_ref.pack(side=tk.LEFT)
       
        #Кнопка добавления
        self.img_add = tk.PhotoImage(file='img/add.png')
        btn_add = tk.Button(toolbar, text='Добавить', bg='gray75',
                             bd = 0, image = self.img_add,
                              command=self.open_child)
        btn_add.pack(side=tk.LEFT)
                
        #Кнопка изменения
        self.img_upd = tk.PhotoImage(file='img/update.png')
        btn_upd = tk.Button(toolbar, text='Изменить', bg='gray75',
                             bd = 0, image = self.img_upd,
                              command=self.open_update_child)
        btn_upd.pack(side=tk.LEFT)

        #Кнопка удаления
        self.img_del = tk.PhotoImage(file='img/delete.png')
        btn_del = tk.Button(toolbar, text='Удалить', bg='gray75',
                             bd = 0, image = self.img_del,
                              command=self.delete_records)
        btn_del.pack(side=tk.LEFT)

        #Кнопка поиска
        self.img_search = tk.PhotoImage(file='img/search.png')
        btn_search = tk.Button(toolbar, text='Найти', bg='gray75',
                             bd = 0, image = self.img_search,
                              command=self.open_search)
        btn_search.pack(side=tk.LEFT)
        
        self.tree = ttk.Treeview(self, 
                                 columns=('id', 'name', 'email', 'phone', 'salary'),
                                 height=30, show='headings')
        self.tree.column('id', width=80, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('email', width=300, anchor=tk.CENTER)
        self.tree.column('phone', width=200, anchor=tk.CENTER)
        self.tree.column('salary', width=100, anchor=tk.CENTER)

        self.tree.heading('id', text='id')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('salary', text='Зарплата')

        self.tree.pack(side=tk.LEFT)

    #Метод добавления данных
    def records(self, name, phone, email, salary):
        self.db.insert_data(name, phone, email, salary)
        self.view()

    #Отображение данных в таблице
    def view(self):
        self.db.cursor.execute('SELECT * FROM users')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=i) for i in self.db.cursor.fetchall()]

    #Метод поиска данных
    def search_records(self, name):
        self.db.cursor.execute('SELECT * FROM users WHERE name LIKE ?', ('%' + name + '%', ))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=i) for i in self.db.cursor.fetchall()]

    #Метод изменения данных
    def update_record(self, name, phone, email, salary):
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cursor.execute('''
            UPDATE users
            SET name = ?, phone = ?, email = ?, salary = ?
            WHERE id = ?
        ''',(name, phone, email, salary, id))
        self.db.connect.commit()
        self.view()

    #Метод удаления данных
    def delete_records(self):
        for row in self.tree.selection():
            self.db.cursor.execute('DELETE FROM users WHERE id = ?',
                                   (self.tree.set(row, '#1'), ))
        self.db.connect.commit()
        self.view()

#Класс дочернего окна
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    #Инициализация виджетов дочернего окна
    def init_child(self):
        self.title('Добавить сотрудника')
        self.geometry('400x300')
        self.resizable(False, False)
        self.iconbitmap('img/logo.ico')
        #Перехватываем все события
        self.grab_set()
        #Перехватываем фокус
        self.focus_set()


        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)
        
        label_phone = tk.Label(self, text='Телефон:')
        label_phone.place(x=50, y=80)
   
        label_email = tk.Label(self, text='E-mail:')
        label_email.place(x=50, y=110)

        label_salary = tk.Label(self, text='Зарплата:')
        label_salary.place(x=50, y=140)
       
        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=200, y=50)
        
        self.entry_phone = tk.Entry(self)
        self.entry_phone.place(x=200, y=80)
   
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=200, y=110)

        self.entry_salary = tk.Entry(self)
        self.entry_salary.place(x=200, y=140)

        btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=200, y=200)

        self.btn_add = tk.Button(self, text='Добавить')
        self.btn_add.bind('<Button-1>', lambda ev: self.view.records(self.entry_name.get(),
                                                                self.entry_phone.get(),
                                                                self.entry_email.get(),
                                                                self.entry_salary.get()))

        self.btn_add.place(x=280, y=200)


#Класс дочернего окна для изменения данных
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.db = db
        self.default()

    def init_update(self):
        self.title('Редактирование Сотрудника')
        self.btn_add.destroy()
        self.btn_upd = tk.Button(self, text='Изменить')
        self.btn_upd.bind('<Button-1>', lambda ev: self.view.update_record(self.entry_name.get(),
                                                                self.entry_phone.get(),
                                                                self.entry_email.get(),
                                                                self.entry_salary.get()))
        self.btn_upd.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        self.btn_upd.place(x=280, y=200)

    def default(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cursor.execute('SELECT * FROM users WHERE id = ?', (id, ))
        row = self.db.cursor.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_phone.insert(0, row[3])
        self.entry_salary.insert(0, row[4])

#Класс окна для поиска
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_search()
        self.view = app

    #Инициализация виджетов дочернего окна для поиска
    def init_search(self):
        self.title('Поиск сотрудника')
        self.geometry('300x100')
        self.resizable(False, False)
        self.iconbitmap('img/logo.ico')
        #Перехватываем все события
        self.grab_set()
        #Перехватываем фокус
        self.focus_set()


        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=40, y=35)
       
        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=100, y=35)
        
        btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=100, y=70)

        self.btn_search = tk.Button(self, text='Найти')
        self.btn_search.bind('<Button-1>', lambda ev: self.view.search_records(self.entry_name.get()))
        self.btn_search.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        self.btn_search.place(x=175, y=70)

#Класс БД
class Db():
    def __init__(self) -> None:
        self.connect = sqlite3.connect('Workers.db')
        self.cursor = self.connect.cursor()
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        phone TEXT,
                        email TEXT,
                        salary TEXT
                    )''')                    
        self.connect.commit()
    
    def insert_data(self, name, phone, email, salary):
        self.cursor.execute('''
                        INSERT INTO users ('name', 'phone', 'email', salary)
                        VALUES (?,?,?,?)''', (name, phone, email, salary))
        self.connect.commit()
#Создание главного окна
if __name__ == '__main__':
    root = tk.Tk()
    db = Db()
    app = Main(root)
    app.pack()
    root.title('Список сотрудников компании')
    root.geometry('1000x720')
    root.resizable(False, False)
    root.iconbitmap('img/logo.ico')
    root.mainloop()