import tkinter as tk
from tkinter import messagebox
import sqlite3



def create_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()



def register_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        messagebox.showinfo('Успех', 'Пользователь зарегистрирован успешно.')
    except sqlite3.IntegrityError:
        messagebox.showerror('Ошибка', 'Пользователь с таким именем уже существует.')
    finally:
        conn.close()



def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user



def authorize_window():
    def login():
        username = entry_username.get()
        password = entry_password.get()
        user = authenticate_user(username, password)
        if user:
            messagebox.showinfo('Успех', 'Авторизация прошла успешно.')
        else:
            messagebox.showerror('Ошибка', 'Неверный логин или пароль.')

    def open_registration_window():
        reg_window = tk.Toplevel(root)
        reg_window.title("Регистрация")

        tk.Label(reg_window, text="Логин:").grid(row=0, column=0)
        tk.Label(reg_window, text="Пароль:").grid(row=1, column=0)

        entry_reg_username = tk.Entry(reg_window)
        entry_reg_password = tk.Entry(reg_window, show='*')

        entry_reg_username.grid(row=0, column=1)
        entry_reg_password.grid(row=1, column=1)

        button_register = tk.Button(reg_window, text="Зарегистрироваться",
                                    command=lambda: register_user(entry_reg_username.get(), entry_reg_password.get()))
        button_register.grid(row=2, columnspan=2)

    root = tk.Tk()
    root.title("Авторизация")

    tk.Label(root, text="Логин:").grid(row=0, column=0)
    tk.Label(root, text="Пароль:").grid(row=1, column=0)

    entry_username = tk.Entry(root)
    entry_password = tk.Entry(root, show='*')

    entry_username.grid(row=0, column=1)
    entry_password.grid(row=1, column=1)

    button_login = tk.Button(root, text="Войти", command=login)
    button_login.grid(row=2, columnspan=2)

    button_register = tk.Button(root, text="Регистрация", command=open_registration_window)
    button_register.grid(row=3, columnspan=2)

    root.mainloop()



if __name__ == '__main__':
    create_db()
    authorize_window()

