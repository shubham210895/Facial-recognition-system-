import tkinter as tk
from tkinter import ttk
import os
import csv


def show_attendance():

    # Purani table entries clear
    for item in table.get_children():
        table.delete(item)

    attendance_folder = "attendance"

    if not os.path.exists(attendance_folder):
        return

    # Attendance files read karo
    for file_name in os.listdir(attendance_folder):

        if file_name.endswith(".csv"):

            file_path = os.path.join(
                attendance_folder,
                file_name
            )

            with open(
                file_path,
                "r",
                newline="",
                encoding="utf-8"
            ) as file:

                reader = csv.DictReader(file)

                for row in reader:

                    table.insert(
                        "",
                        tk.END,
                        values=(
                            row["ID"],
                            row["Name"],
                            row["Date"],
                            row["Time"],
                            row["Status"]
                        )
                    )


# Main window
root = tk.Tk()

root.title("Facial Recognition Attendance Dashboard")

root.geometry("900x550")


# Title
title = tk.Label(
    root,
    text="Attendance Dashboard",
    font=("Arial", 24, "bold")
)

title.pack(pady=20)


# Table columns
columns = (
    "ID",
    "Name",
    "Date",
    "Time",
    "Status"
)


table = ttk.Treeview(
    root,
    columns=columns,
    show="headings"
)


# Headings
for column in columns:

    table.heading(
        column,
        text=column
    )

    table.column(
        column,
        width=150
    )


table.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)


# Refresh button
refresh_button = tk.Button(
    root,
    text="Refresh Attendance",
    command=show_attendance,
    width=20,
    height=2
)

refresh_button.pack(pady=15)


# Attendance show karo
show_attendance()


# Start application
root.mainloop()