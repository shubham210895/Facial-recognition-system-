import tkinter as tk
from tkinter import messagebox
import subprocess
import sys


def open_register():
    subprocess.Popen([sys.executable, "register.py"])


def open_capture():
    subprocess.Popen([sys.executable, "capture_face.py"])


def train_model():
    result = subprocess.run([sys.executable, "train.py"])

    if result.returncode == 0:
        messagebox.showinfo(
            "Training",
            "Face training complete!"
        )


def open_attendance():
    subprocess.Popen([sys.executable, "attendance.py"])


def open_dashboard():
    subprocess.Popen([sys.executable, "dashboard.py"])


def exit_application():
    root.destroy()


# Main window
root = tk.Tk()

root.title("Facial Recognition Attendance System")

root.geometry("550x650")


# Title
title = tk.Label(
    root,
    text="Facial Recognition\nAttendance System",
    font=("Arial", 24, "bold")
)

title.pack(pady=40)


# Register button
register_button = tk.Button(
    root,
    text="1. Register Student",
    command=open_register,
    width=30,
    height=2
)

register_button.pack(pady=10)


# Capture button
capture_button = tk.Button(
    root,
    text="2. Capture Face",
    command=open_capture,
    width=30,
    height=2
)

capture_button.pack(pady=10)


# Training button
train_button = tk.Button(
    root,
    text="3. Train Face Model",
    command=train_model,
    width=30,
    height=2
)

train_button.pack(pady=10)


# Attendance button
attendance_button = tk.Button(
    root,
    text="4. Start Attendance",
    command=open_attendance,
    width=30,
    height=2
)

attendance_button.pack(pady=10)


# Dashboard button
dashboard_button = tk.Button(
    root,
    text="5. View Attendance",
    command=open_dashboard,
    width=30,
    height=2
)

dashboard_button.pack(pady=10)


# Exit button
exit_button = tk.Button(
    root,
    text="Exit",
    command=exit_application,
    width=30,
    height=2
)

exit_button.pack(pady=25)


# Start application
root.mainloop()