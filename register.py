import tkinter as tk
from tkinter import messagebox

from database import add_student, create_database


def register_student():
    student_id = id_entry.get().strip()
    name = name_entry.get().strip()

    if student_id == "" or name == "":
        messagebox.showerror("Error", "ID aur Name dono enter karo.")
        return

    create_database()
    add_student(student_id, name)

    messagebox.showinfo(
        "Success",
        f"Student registered successfully!\n\nID: {student_id}\nName: {name}"
    )

    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)


root = tk.Tk()
root.title("Student Registration")
root.geometry("400x300")

title = tk.Label(
    root,
    text="Student Registration",
    font=("Arial", 20, "bold")
)
title.pack(pady=30)

tk.Label(root, text="Student ID").pack()

id_entry = tk.Entry(root, width=30)
id_entry.pack(pady=5)

tk.Label(root, text="Student Name").pack()

name_entry = tk.Entry(root, width=30)
name_entry.pack(pady=5)

register_button = tk.Button(
    root,
    text="Register Student",
    command=register_student,
    width=20
)
register_button.pack(pady=20)

root.mainloop()