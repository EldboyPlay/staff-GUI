import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime

# Функция для обновления времени
def update_time():
    now = datetime.datetime.now()
    time_string = now.strftime("%Y-%m-%d %H:%M:%S")
    time_label.config(text=time_string)
    root.after(1000, update_time)

# Функция для получения выбранного сотрудника
def get_selected_employee():
    try:
        selected_item = tree.selection()[0]  # Получение выбранной строки
        return tree.item(selected_item)['values'][0]  # Возвращение ID сотрудника
    except IndexError:
        messagebox.showwarning("Предупреждение", "Выберите сотрудника")
        return None

# Дополненная функция удаления сотрудника
def delete_selected_employee():
    id = get_selected_employee()
    if id:
        delete_employee(id)
        messagebox.showinfo("Информация", "Сотрудник удален")

# Создание и подключение к базе данных
conn = sqlite3.connect('employees.db')
cursor = conn.cursor()

# Создание таблицы: employees.db
cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    phone_number TEXT,
    email TEXT,
    salary REAL
)
''')
conn.commit()

# Функции для работы с базой данных
def add_employee(full_name, phone_number, email, salary):
    cursor.execute('INSERT INTO employees (full_name, phone_number, email, salary) VALUES (?, ?, ?, ?)',
                   (full_name, phone_number, email, salary))
    conn.commit()
    update_treeview()

def update_employee(id, full_name, phone_number, email, salary):
    cursor.execute('''
    UPDATE employees
    SET full_name = ?, phone_number = ?, email = ?, salary = ?
    WHERE id = ?
    ''', (full_name, phone_number, email, salary, id))
    conn.commit()
    update_treeview()

def delete_employee(id):
    cursor.execute('DELETE FROM employees WHERE id = ?', (id,))
    conn.commit()
    update_treeview()

def search_employees(name):
    cursor.execute('SELECT * FROM employees WHERE full_name LIKE ?', ('%' + name + '%',))
    return cursor.fetchall()

# Функция для обновления данных в Treeview
def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    for row in cursor.execute('SELECT * FROM employees'):
        tree.insert('', 'end', values=row)

# Функция для выполнения поиска
def perform_search():
    search_query = search_entry.get()
    results = search_employees(search_query)
    for row in tree.get_children():
        tree.delete(row)
    if results:
        for row in results:
            tree.insert('', 'end', values=row)
    else:
        messagebox.showinfo("Информация", "Сотрудник не найден, повторите поиск!")

# Создание графического интерфейса
root = tk.Tk()
root.title("Список сотрудников компании")

# Создание Treeview
tree = ttk.Treeview(root, columns=('ID', 'Full Name', 'Phone Number', 'Email', 'Salary'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Full Name', text='ФИО')
tree.heading('Phone Number', text='Номер телефона')
tree.heading('Email', text='Email')
tree.heading('Salary', text='Заработная плата')
tree.pack(fill=tk.BOTH, expand=True)

# Кнопки и поля ввода
add_frame = tk.Frame(root)
add_frame.pack(fill=tk.X, padx=5, pady=5)

search_frame = tk.Frame(root)
search_frame.pack(fill=tk.X, padx=5, pady=5)

tk.Label(search_frame, text="Поиск по ФИО:").pack(side=tk.LEFT, padx=5, pady=5)
search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(search_frame, text="Поиск", command=perform_search).pack(side=tk.LEFT, padx=5, pady=5)

tk.Label(add_frame, text="ФИО").grid(row=0, column=0, padx=5, pady=5)
full_name_entry = tk.Entry(add_frame)
full_name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(add_frame, text="Номер телефона").grid(row=1, column=0, padx=5, pady=5)
phone_number_entry = tk.Entry(add_frame)
phone_number_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(add_frame, text="Email").grid(row=2, column=0, padx=5, pady=5)
email_entry = tk.Entry(add_frame)
email_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(add_frame, text="Заработная плата").grid(row=3, column=0, padx=5, pady=5)
salary_entry = tk.Entry(add_frame)
salary_entry.grid(row=3, column=1, padx=5, pady=5)

# Кнопки управления
tk.Button(add_frame, text="Добавить сотрудника", command=lambda: add_employee(
    full_name_entry.get(),
    phone_number_entry.get(),
    email_entry.get(),
    salary_entry.get()
)).grid(row=4, column=0, columnspan=2, sticky=tk.EW, padx=5, pady=5)

tk.Button(add_frame, text="Обновить список", command=update_treeview).grid(row=5, column=0, columnspan=2, sticky=tk.EW, padx=5, pady=5)

# Добавление кнопки для удаления сотрудника
tk.Button(add_frame, text="Удалить выбранного сотрудника", command=delete_selected_employee).grid(row=6, column=0, columnspan=2, sticky=tk.EW, padx=5, pady=5)

# Метка времени в главном окне
time_label = tk.Label(root, text="", font=('Helvetica', 12))
time_label.pack(fill=tk.X, padx=5, pady=5)

# Запуск обновления времени
update_time()

# Запуск приложения
update_treeview() # Обновление Treeview при запуске
root.mainloop()

# Закрытие соединения с базой данных
conn.close()




