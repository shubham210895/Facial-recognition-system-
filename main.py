import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import subprocess
import sys
import os
import csv
from datetime import datetime


# =========================================================
# PATHS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STUDENT_FILE = os.path.join(BASE_DIR, "students.csv")
ATTENDANCE_FOLDER = os.path.join(BASE_DIR, "attendance")

# Galgotias University Logo
LOGO_PATH = os.path.join(
    BASE_DIR,
    "assets",
    "galgotia.jpg"
)

# Galgotias University Campus Image
CAMPUS_IMAGE_PATH = os.path.join(
    BASE_DIR,
    "assets",
    "galgotias.webp"
)


# =========================================================
# COLORS
# =========================================================

BG = "#0A1020"
WHITE = "#111B2D"

NAVY = "#172B4D"
NAVY_DARK = "#0A1428"

BLUE = "#4D8DFF"
GREEN = "#2DD4A7"
ORANGE = "#F6B94A"
RED = "#FF647C"
PURPLE = "#A78BFA"
CYAN = "#39C6E8"

TEXT = "#E8EEF8"
SUBTEXT = "#9AAAC0"
BORDER = "#263650"

LIGHT_BLUE = "#1B3154"
LIGHT_GREEN = "#143B37"
LIGHT_RED = "#482635"


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title(
    "Facial Recognition Attendance System"
)

root.geometry("1400x800")
root.minsize(1100, 700)

root.configure(bg=BG)


# =========================================================
# HELPERS
# =========================================================

def clear_tree(tree):

    for item in tree.get_children():
        tree.delete(item)


def open_python_file(filename):

    file_path = os.path.join(
        BASE_DIR,
        filename
    )

    if not os.path.exists(file_path):

        messagebox.showerror(
            "File Not Found",
            f"{filename} nahi mila.",
            parent=root
        )

        return False

    try:

        subprocess.Popen(
            [sys.executable, file_path],
            cwd=BASE_DIR
        )

        return True

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e),
            parent=root
        )

        return False


# =========================================================
# STUDENT DATA
# =========================================================

def get_students():

    students = []

    if not os.path.exists(STUDENT_FILE):
        return students

    try:

        with open(
            STUDENT_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                student_id = row.get(
                    "ID",
                    ""
                ).strip()

                name = row.get(
                    "Name",
                    ""
                ).strip()

                if student_id and name:

                    students.append(
                        {
                            "ID": student_id,
                            "Name": name
                        }
                    )

    except Exception:
        pass

    return students


# =========================================================
# ATTENDANCE DATA
# =========================================================

def get_today_attendance():

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    records = []

    if not os.path.exists(
        ATTENDANCE_FOLDER
    ):
        return records

    for file_name in os.listdir(
        ATTENDANCE_FOLDER
    ):

        if not file_name.endswith(".csv"):
            continue

        file_path = os.path.join(
            ATTENDANCE_FOLDER,
            file_name
        )

        try:

            with open(
                file_path,
                "r",
                newline="",
                encoding="utf-8"
            ) as file:

                reader = csv.DictReader(file)

                for row in reader:

                    if row.get("Date") == today:

                        records.append(row)

        except Exception:
            continue

    return records


def get_recent_attendance():

    records = []

    if not os.path.exists(
        ATTENDANCE_FOLDER
    ):
        return records

    for file_name in os.listdir(
        ATTENDANCE_FOLDER
    ):

        if not file_name.endswith(".csv"):
            continue

        file_path = os.path.join(
            ATTENDANCE_FOLDER,
            file_name
        )

        try:

            with open(
                file_path,
                "r",
                newline="",
                encoding="utf-8"
            ) as file:

                reader = csv.DictReader(file)

                for row in reader:

                    if row.get("ID"):

                        records.append(row)

        except Exception:
            continue

    return records[-10:][::-1]


# =========================================================
# DASHBOARD VALUES
# =========================================================

def get_dashboard_values():

    students = get_students()

    attendance = get_today_attendance()

    total = len(students)

    present_ids = set()

    for row in attendance:

        student_id = row.get("ID")

        if student_id:

            present_ids.add(
                student_id
            )

    present = len(present_ids)

    absent = max(
        total - present,
        0
    )

    if total > 0:

        rate = round(
            (present / total) * 100
        )

    else:

        rate = 0

    return total, present, absent, rate


# =========================================================
# UPDATE STATISTICS
# =========================================================

def update_statistics():

    total, present, absent, rate = (
        get_dashboard_values()
    )

    total_value.config(
        text=str(total)
    )

    present_value.config(
        text=str(present)
    )

    rate_value.config(
        text=f"{rate}%"
    )

    updated_value.config(
        text=datetime.now().strftime(
            "%I:%M %p"
        )
    )

    date_value.config(
        text=datetime.now().strftime(
            "%d %b %Y"
        )
    )

    load_recent_attendance()


# =========================================================
# RECENT ATTENDANCE
# =========================================================

def load_recent_attendance():

    clear_tree(
        attendance_table
    )

    records = get_recent_attendance()

    for row in records:

        student_id = row.get(
            "ID",
            ""
        )

        name = row.get(
            "Name",
            ""
        )

        date = row.get(
            "Date",
            ""
        )

        time = row.get(
            "Time",
            ""
        )

        status = row.get(
            "Status",
            "Present"
        )

        try:

            date_obj = datetime.strptime(
                date,
                "%Y-%m-%d"
            )

            date = date_obj.strftime(
                "%d-%m-%Y"
            )

        except Exception:
            pass

        attendance_table.insert(
            "",
            "end",
            values=(
                student_id,
                name,
                date,
                time,
                status
            )
        )

    color_status_rows()


# =========================================================
# REGISTER STUDENT
# =========================================================

def register_student():

    student_id = simpledialog.askstring(
        "Register Student",
        "Enter Student ID:",
        parent=root
    )

    if not student_id:
        return

    student_id = student_id.strip()

    name = simpledialog.askstring(
        "Register Student",
        "Enter Student Name:",
        parent=root
    )

    if not name:
        return

    name = name.strip()

    for student in get_students():

        if student["ID"] == student_id:

            messagebox.showwarning(
                "Duplicate ID",
                "Ye Student ID already registered hai.",
                parent=root
            )

            return

    try:

        file_exists = os.path.exists(
            STUDENT_FILE
        )

        with open(
            STUDENT_FILE,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            if not file_exists:

                writer.writerow(
                    ["ID", "Name"]
                )

            writer.writerow(
                [student_id, name]
            )

        messagebox.showinfo(
            "Success",
            "Student registered successfully!",
            parent=root
        )

        update_statistics()

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e),
            parent=root
        )


# =========================================================
# CAPTURE FACE
# =========================================================

def capture_face():

    student_id = simpledialog.askstring(
        "Capture Face",
        "Enter Student ID:",
        parent=root
    )

    if not student_id:
        return

    try:

        from capture_face import capture_faces

        capture_faces(
            student_id.strip()
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e),
            parent=root
        )


# =========================================================
# TRAIN MODEL
# =========================================================

def train_model():

    dataset_path = os.path.join(
        BASE_DIR,
        "dataset"
    )

    if not os.path.exists(
        dataset_path
    ):

        messagebox.showwarning(
            "Dataset Not Found",
            "Pehle student ka face capture karo.",
            parent=root
        )

        return

    image_files = [
        f
        for f in os.listdir(
            dataset_path
        )
        if f.lower().endswith(
            (".jpg", ".jpeg", ".png")
        )
    ]

    if len(image_files) == 0:

        messagebox.showwarning(
            "No Face Images",
            "Dataset mein koi face image nahi hai.\n"
            "Pehle Capture Face karo.",
            parent=root
        )

        return

    train_file = os.path.join(
        BASE_DIR,
        "train.py"
    )

    if not os.path.exists(
        train_file
    ):

        messagebox.showerror(
            "Error",
            "train.py nahi mila.",
            parent=root
        )

        return

    # =====================================================
    # TRAINING WINDOW
    # =====================================================

    training_window = tk.Toplevel(root)

    training_window.title(
        "Train Face Recognition Model"
    )

    training_window.geometry(
        "520x320"
    )

    training_window.configure(
        bg=WHITE
    )

    training_window.resizable(
        False,
        False
    )

    training_window.transient(
        root
    )

    training_window.grab_set()

    # =====================================================
    # ICON
    # =====================================================

    tk.Label(
        training_window,
        text="✥",
        font=("Arial", 42, "bold"),
        fg=PURPLE,
        bg=WHITE
    ).pack(
        pady=(25, 5)
    )

    # =====================================================
    # TITLE
    # =====================================================

    status_title = tk.Label(
        training_window,
        text="Training Model...",
        font=("Arial", 19, "bold"),
        fg=NAVY,
        bg=WHITE
    )

    status_title.pack()

    # =====================================================
    # DESCRIPTION
    # =====================================================

    status_text = tk.Label(
        training_window,
        text=(
            "Please wait while the face recognition model\n"
            "is being trained."
        ),
        font=("Arial", 10),
        fg=SUBTEXT,
        bg=WHITE,
        justify="center"
    )

    status_text.pack(
        pady=(8, 15)
    )

    # =====================================================
    # PROGRESS BAR
    # =====================================================

    progress = ttk.Progressbar(
        training_window,
        mode="indeterminate",
        length=360
    )

    progress.pack(
        pady=5
    )

    progress.start(10)

    # =====================================================
    # TRAINING PROCESS
    # =====================================================

    try:

        process = subprocess.Popen(
            [
                sys.executable,
                train_file
            ],
            cwd=BASE_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

    except Exception as e:

        progress.stop()

        training_window.destroy()

        messagebox.showerror(
            "Training Error",
            str(e),
            parent=root
        )

        return

    # =====================================================
    # CHECK TRAINING
    # =====================================================

    def check_training():

        if process.poll() is None:

            training_window.after(
                300,
                check_training
            )

            return

        progress.stop()

        try:

            output = process.stdout.read()

        except Exception:

            output = ""

        if process.returncode == 0:

            trainer_file = os.path.join(
                BASE_DIR,
                "trainer",
                "trainer.yml"
            )

            if os.path.exists(
                trainer_file
            ):

                status_title.config(
                    text="✓ Model Trained Successfully!",
                    fg=GREEN
                )

                status_text.config(
                    text=(
                        "Face recognition model successfully trained.\n"
                        "Model is ready for attendance."
                    )
                )

                progress.configure(
                    mode="determinate",
                    maximum=1,
                    value=1
                )

                training_window.after(
                    1800,
                    training_window.destroy
                )

            else:

                status_title.config(
                    text="✕ Training Failed",
                    fg=RED
                )

                status_text.config(
                    text=(
                        "trainer.yml create nahi hui.\n"
                        "Training dobara try karo."
                    )
                )

                training_window.after(
                    2500,
                    training_window.destroy
                )

        else:

            status_title.config(
                text="✕ Training Failed",
                fg=RED
            )

            status_text.config(
                text=(
                    "Model training complete nahi ho payi.\n"
                    "Dataset aur train.py check karo."
                )
            )

            training_window.after(
                2500,
                training_window.destroy
            )

    training_window.after(
        300,
        check_training
    )


# =========================================================
# MARK ATTENDANCE
# =========================================================

def start_attendance():

    trainer_path = os.path.join(
        BASE_DIR,
        "trainer",
        "trainer.yml"
    )

    if not os.path.exists(
        trainer_path
    ):

        messagebox.showwarning(
            "Model Not Found",
            "Pehle Capture Face aur Train Model complete karo.",
            parent=root
        )

        return

    if open_python_file(
        "attendance.py"
    ):

        root.after(
            3000,
            update_statistics
        )


# =========================================================
# VIEW RECORDS
# =========================================================

def view_records():

    open_python_file(
        "dashboard.py"
    )


# =========================================================
# SETTINGS
# =========================================================

def settings():

    messagebox.showinfo(
        "Settings",
        "Settings module future version mein add kiya ja sakta hai.",
        parent=root
    )


# =========================================================
# EXIT
# =========================================================

def exit_application():

    answer = messagebox.askyesno(
        "Exit Application",
        "Kya aap application close karna chahte ho?",
        parent=root
    )

    if answer:

        root.destroy()


# =========================================================
# SIDEBAR
# =========================================================

sidebar = tk.Frame(
    root,
    bg=NAVY,
    width=270
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)


# =========================================================
# SIDEBAR LOGO
# =========================================================

logo_frame = tk.Frame(
    sidebar,
    bg=WHITE,
    width=235,
    height=82
)

logo_frame.pack(
    pady=(20, 28),
    padx=18
)

logo_frame.pack_propagate(False)


if os.path.exists(
    LOGO_PATH
):

    try:

        logo_image = Image.open(
            LOGO_PATH
        )

        logo_image.thumbnail(
            (220, 72)
        )

        logo_photo = ImageTk.PhotoImage(
            logo_image
        )

        logo_label = tk.Label(
            logo_frame,
            image=logo_photo,
            bg=WHITE
        )

        logo_label.image = logo_photo

        logo_label.pack(
            expand=True
        )

    except Exception:

        tk.Label(
            logo_frame,
            text="GALGOTIAS\nUNIVERSITY",
            font=("Arial", 15, "bold"),
            fg=NAVY,
            bg=WHITE
        ).pack(
            expand=True
        )

else:

    tk.Label(
        logo_frame,
        text="GALGOTIAS\nUNIVERSITY",
        font=("Arial", 15, "bold"),
        fg=NAVY,
        bg=WHITE
    ).pack(
        expand=True
    )


# =========================================================
# SIDEBAR BUTTON
# =========================================================

def create_sidebar_button(
    text,
    icon,
    command,
    active=False
):

    frame = tk.Frame(
        sidebar,
        bg=RED if active else NAVY
    )

    frame.pack(
        fill="x",
        padx=15,
        pady=3
    )

    button = tk.Button(
        frame,
        text=f"{icon}   {text}",
        command=command,
        font=(
            "Arial",
            11,
            "bold" if active else "normal"
        ),
        fg=WHITE,
        bg=RED if active else NAVY,
        activebackground=RED,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        anchor="w",
        padx=18,
        cursor="hand2"
    )

    button.pack(
        fill="x",
        ipady=10
    )

    return button


create_sidebar_button(
    "Dashboard",
    "⌂",
    update_statistics,
    True
)

create_sidebar_button(
    "Register Student",
    "♙",
    register_student
)

create_sidebar_button(
    "Capture Face",
    "▣",
    capture_face
)

create_sidebar_button(
    "Train Model",
    "✥",
    train_model
)

create_sidebar_button(
    "Mark Attendance",
    "✓",
    start_attendance
)

create_sidebar_button(
    "Attendance Records",
    "▥",
    view_records
)


# =========================================================
# SIDEBAR SEPARATOR
# =========================================================

tk.Frame(
    sidebar,
    bg="#A9B8CD",
    height=1
).pack(
    fill="x",
    padx=25,
    pady=18
)


create_sidebar_button(
    "Settings",
    "⚙",
    settings
)

create_sidebar_button(
    "Exit",
    "⇥",
    exit_application
)


# =========================================================
# SIDEBAR FOOTER
# =========================================================

tk.Label(
    sidebar,
    text="Learning Today\nLeading Tomorrow",
    font=("Arial", 12, "italic"),
    fg="#263650",
    bg=NAVY,
    justify="left"
).pack(
    side="bottom",
    anchor="w",
    padx=38,
    pady=(0, 80)
)


# =========================================================
# MAIN AREA
# =========================================================

main = tk.Frame(
    root,
    bg=BG
)

main.pack(
    side="left",
    fill="both",
    expand=True
)


# =========================================================
# TOP HEADER
# =========================================================

top_header = tk.Frame(
    main,
    bg=WHITE,
    height=105
)

top_header.pack(
    fill="x"
)

top_header.pack_propagate(False)


header_left = tk.Frame(
    top_header,
    bg=WHITE
)

header_left.pack(
    side="left",
    padx=38,
    pady=18
)


tk.Label(
    header_left,
    text="Facial Recognition Attendance System",
    font=("Arial", 25, "bold"),
    fg=NAVY,
    bg=WHITE
).pack(
    anchor="w"
)


tk.Label(
    header_left,
    text="Smart Attendance   |   Secure Campus   |   Better Tomorrow",
    font=("Arial", 11),
    fg="#9AAAC0",
    bg=WHITE
).pack(
    anchor="w",
    pady=(7, 0)
)


# =========================================================
# UNIVERSITY HEADER RIGHT
# =========================================================

university_header = tk.Frame(
    top_header,
    bg=WHITE
)

university_header.pack(
    side="right",
    padx=35
)


tk.Label(
    university_header,
    text="🎓",
    font=("Arial", 25),
    fg=NAVY,
    bg=WHITE
).pack(
    side="left",
    padx=(0, 12)
)


university_text = tk.Frame(
    university_header,
    bg=WHITE
)

university_text.pack(
    side="left"
)


tk.Label(
    university_text,
    text="Galgotias University",
    font=("Arial", 12, "bold"),
    fg=NAVY,
    bg=WHITE
).pack(
    anchor="w"
)


tk.Label(
    university_text,
    text="Greater Noida, Uttar Pradesh",
    font=("Arial", 9),
    fg=SUBTEXT,
    bg=WHITE
).pack(
    anchor="w"
)


# =========================================================
# SCROLLABLE CONTENT
# =========================================================

canvas = tk.Canvas(
    main,
    bg=BG,
    highlightthickness=0
)

scrollbar = ttk.Scrollbar(
    main,
    orient="vertical",
    command=canvas.yview
)

scrollable = tk.Frame(
    canvas,
    bg=BG
)

scrollable.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas_window = canvas.create_window(
    (0, 0),
    window=scrollable,
    anchor="nw"
)

canvas.configure(
    yscrollcommand=scrollbar.set
)


def resize_canvas(event):

    canvas.itemconfig(
        canvas_window,
        width=event.width
    )


canvas.bind(
    "<Configure>",
    resize_canvas
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)


# =========================================================
# DASHBOARD CONTENT
# =========================================================

dashboard_content = tk.Frame(
    scrollable,
    bg=BG
)

dashboard_content.pack(
    fill="both",
    expand=True,
    padx=28,
    pady=25
)


# =========================================================
# STAT CARDS
# =========================================================

stats_frame = tk.Frame(
    dashboard_content,
    bg=BG
)

stats_frame.pack(
    fill="x"
)


def create_stat_card(
    parent,
    color,
    icon,
    title,
    value,
    subtitle
):

    card = tk.Frame(
        parent,
        bg=color,
        height=155
    )

    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=5
    )

    card.pack_propagate(False)

    tk.Label(
        card,
        text=icon,
        font=("Arial", 28, "bold"),
        fg=WHITE,
        bg=color
    ).pack(
        anchor="w",
        padx=23,
        pady=(15, 0)
    )

    value_label = tk.Label(
        card,
        text=value,
        font=("Arial", 27, "bold"),
        fg=WHITE,
        bg=color
    )

    value_label.pack(
        anchor="w",
        padx=23,
        pady=(2, 0)
    )

    tk.Label(
        card,
        text=title,
        font=("Arial", 12, "bold"),
        fg=WHITE,
        bg=color
    ).pack(
        anchor="w",
        padx=23
    )

    tk.Label(
        card,
        text=subtitle,
        font=("Arial", 9),
        fg=WHITE,
        bg=color
    ).pack(
        anchor="w",
        padx=23,
        pady=(3, 0)
    )

    return value_label


total_value = create_stat_card(
    stats_frame,
    BLUE,
    "♟",
    "Total Students",
    "0",
    "Registered Students"
)


present_value = create_stat_card(
    stats_frame,
    GREEN,
    "✓",
    "Present Today",
    "0",
    "Marked Present"
)


rate_value = create_stat_card(
    stats_frame,
    ORANGE,
    "▣",
    "Attendance Rate",
    "0%",
    "Today's Attendance"
)


# =========================================================
# LAST UPDATED CARD
# =========================================================

last_card = tk.Frame(
    stats_frame,
    bg=RED,
    height=155
)

last_card.pack(
    side="left",
    fill="both",
    expand=True,
    padx=5
)

last_card.pack_propagate(False)


tk.Label(
    last_card,
    text="◷",
    font=("Arial", 29, "bold"),
    fg=WHITE,
    bg=RED
).pack(
    anchor="w",
    padx=23,
    pady=(15, 0)
)


updated_value = tk.Label(
    last_card,
    text="--:--",
    font=("Arial", 25, "bold"),
    fg=WHITE,
    bg=RED
)

updated_value.pack(
    anchor="w",
    padx=23,
    pady=(3, 0)
)


tk.Label(
    last_card,
    text="Last Updated",
    font=("Arial", 12, "bold"),
    fg=WHITE,
    bg=RED
).pack(
    anchor="w",
    padx=23
)


date_value = tk.Label(
    last_card,
    text="",
    font=("Arial", 9),
    fg=WHITE,
    bg=RED
)

date_value.pack(
    anchor="w",
    padx=23,
    pady=(3, 0)
)


# =========================================================
# MIDDLE AREA
# =========================================================

middle = tk.Frame(
    dashboard_content,
    bg=BG
)

middle.pack(
    fill="x",
    pady=(20, 0)
)


# =========================================================
# QUICK ACTIONS PANEL
# =========================================================

quick_panel = tk.Frame(
    middle,
    bg=WHITE,
    highlightbackground=BORDER,
    highlightthickness=1
)

quick_panel.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 10)
)


quick_title = tk.Frame(
    quick_panel,
    bg=WHITE
)

quick_title.pack(
    fill="x",
    padx=20,
    pady=(15, 10)
)


tk.Label(
    quick_title,
    text="⚡  Quick Actions",
    font=("Arial", 15, "bold"),
    fg=NAVY,
    bg=WHITE
).pack(
    side="left"
)


# =========================================================
# ACTION CARDS
# =========================================================

actions_grid = tk.Frame(
    quick_panel,
    bg=WHITE
)

actions_grid.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=(0, 20)
)


def create_action_card(
    parent,
    row,
    column,
    color,
    icon,
    title,
    description,
    command
):

    card = tk.Button(
        parent,
        text=(
            f"{icon}\n\n"
            f"{title}\n"
            f"{description}"
        ),
        command=command,
        font=("Arial", 10, "bold"),
        fg=WHITE,
        bg=color,
        activebackground=color,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        cursor="hand2",
        justify="left",
        anchor="w",
        padx=18
    )

    card.grid(
        row=row,
        column=column,
        sticky="nsew",
        padx=5,
        pady=5
    )

    return card


actions_grid.grid_columnconfigure(
    0,
    weight=1
)

actions_grid.grid_columnconfigure(
    1,
    weight=1
)

actions_grid.grid_columnconfigure(
    2,
    weight=1
)

actions_grid.grid_rowconfigure(
    0,
    weight=1
)

actions_grid.grid_rowconfigure(
    1,
    weight=1
)


create_action_card(
    actions_grid,
    0,
    0,
    BLUE,
    "♙",
    "Register Student",
    "Add new student",
    register_student
)

create_action_card(
    actions_grid,
    0,
    1,
    GREEN,
    "▣",
    "Capture Face",
    "Collect 30 face images",
    capture_face
)

create_action_card(
    actions_grid,
    0,
    2,
    PURPLE,
    "✥",
    "Train Model",
    "Train recognition model",
    train_model
)

create_action_card(
    actions_grid,
    1,
    0,
    ORANGE,
    "✓",
    "Mark Attendance",
    "Start live recognition",
    start_attendance
)

create_action_card(
    actions_grid,
    1,
    1,
    CYAN,
    "▥",
    "View Records",
    "Check attendance history",
    view_records
)


# =========================================================
# CAMPUS PROMO PANEL
# =========================================================

promo_panel = tk.Frame(
    middle,
    bg=NAVY,
    width=300
)

promo_panel.pack(
    side="right",
    fill="y"
)

promo_panel.pack_propagate(False)


if os.path.exists(
    CAMPUS_IMAGE_PATH
):

    try:

        campus_image = Image.open(
            CAMPUS_IMAGE_PATH
        )

        campus_image = campus_image.resize(
            (300, 280)
        )

        campus_photo = ImageTk.PhotoImage(
            campus_image
        )

        campus_label = tk.Label(
            promo_panel,
            image=campus_photo,
            bg=NAVY
        )

        campus_label.image = campus_photo

        campus_label.pack(
            fill="x"
        )

    except Exception:

        tk.Label(
            promo_panel,
            text="GALGOTIAS\nUNIVERSITY",
            font=("Arial", 22, "bold"),
            fg=WHITE,
            bg=NAVY
        ).pack(
            pady=70
        )

else:

    if os.path.exists(
        LOGO_PATH
    ):

        try:

            promo_logo_image = Image.open(
                LOGO_PATH
            )

            promo_logo_image.thumbnail(
                (220, 120)
            )

            promo_logo = ImageTk.PhotoImage(
                promo_logo_image
            )

            promo_logo_label = tk.Label(
                promo_panel,
                image=promo_logo,
                bg=NAVY
            )

            promo_logo_label.image = promo_logo

            promo_logo_label.pack(
                pady=(45, 25)
            )

        except Exception:
            pass


tk.Label(
    promo_panel,
    text="Technology for a\nSmarter Tomorrow",
    font=("Arial", 16, "bold"),
    fg=WHITE,
    bg=NAVY,
    justify="center"
).pack(
    pady=20
)


tk.Label(
    promo_panel,
    text="Smart Attendance\n"
         "Secure Campus\n"
         "Better Tomorrow",
    font=("Arial", 10),
    fg="#263650",
    bg=NAVY,
    justify="center"
).pack()


# =========================================================
# RECENT ATTENDANCE
# =========================================================

recent_panel = tk.Frame(
    dashboard_content,
    bg=WHITE,
    highlightbackground=BORDER,
    highlightthickness=1
)

recent_panel.pack(
    fill="both",
    expand=True,
    pady=(20, 20)
)


recent_header = tk.Frame(
    recent_panel,
    bg=WHITE
)

recent_header.pack(
    fill="x",
    padx=20,
    pady=(14, 8)
)


tk.Label(
    recent_header,
    text="◷  Recent Attendance",
    font=("Arial", 14, "bold"),
    fg=NAVY,
    bg=WHITE
).pack(
    side="left"
)


# =========================================================
# SEARCH
# =========================================================

search_var = tk.StringVar()


search_entry = tk.Entry(
    recent_header,
    textvariable=search_var,
    font=("Arial", 9),
    relief="solid",
    bd=1,
    width=28
)

search_entry.pack(
    side="right",
    padx=(10, 5),
    ipady=6
)

search_entry.insert(
    0,
    " Search by ID or Name..."
)


def search_records():

    query = search_var.get().strip().lower()

    clear_tree(
        attendance_table
    )

    records = get_recent_attendance()

    for row in records:

        student_id = row.get(
            "ID",
            ""
        )

        name = row.get(
            "Name",
            ""
        )

        if (
            query
            and query != "search by id or name..."
        ):

            if (
                query not in student_id.lower()
                and query not in name.lower()
            ):
                continue

        date = row.get(
            "Date",
            ""
        )

        time = row.get(
            "Time",
            ""
        )

        status = row.get(
            "Status",
            "Present"
        )

        try:

            date_obj = datetime.strptime(
                date,
                "%Y-%m-%d"
            )

            date = date_obj.strftime(
                "%d-%m-%Y"
            )

        except Exception:
            pass

        attendance_table.insert(
            "",
            "end",
            values=(
                student_id,
                name,
                date,
                time,
                status
            )
        )

    color_status_rows()


search_button = tk.Button(
    recent_header,
    text="🔎 Search",
    command=search_records,
    font=("Arial", 9, "bold"),
    bg=LIGHT_BLUE,
    fg=NAVY,
    relief="flat",
    bd=0,
    cursor="hand2"
)

search_button.pack(
    side="right",
    padx=5,
    ipadx=8,
    ipady=5
)


refresh_records_button = tk.Button(
    recent_header,
    text="⟳ Refresh",
    command=update_statistics,
    font=("Arial", 9, "bold"),
    bg=LIGHT_BLUE,
    fg=NAVY,
    relief="flat",
    bd=0,
    cursor="hand2"
)

refresh_records_button.pack(
    side="right",
    padx=5,
    ipadx=8,
    ipady=5
)


# =========================================================
# TABLE STYLE
# =========================================================

style = ttk.Style()

try:

    style.theme_use(
        "clam"
    )

except Exception:
    pass


style.configure(
    "Attendance.Treeview",
    background=WHITE,
    foreground=TEXT,
    rowheight=35,
    fieldbackground=WHITE,
    font=("Arial", 9),
    borderwidth=0
)

style.configure(
    "Attendance.Treeview.Heading",
    background="#1A2940",
    foreground=NAVY,
    font=("Arial", 9, "bold"),
    relief="flat"
)

style.map(
    "Attendance.Treeview",
    background=[
        ("selected", "#213A63")
    ],
    foreground=[
        ("selected", TEXT)
    ]
)


# =========================================================
# ATTENDANCE TABLE
# =========================================================

table_frame = tk.Frame(
    recent_panel,
    bg=WHITE
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=(0, 15)
)


attendance_table = ttk.Treeview(
    table_frame,
    columns=(
        "ID",
        "Name",
        "Date",
        "Time",
        "Status"
    ),
    show="headings",
    style="Attendance.Treeview",
    height=7
)


attendance_table.heading(
    "ID",
    text="ID"
)

attendance_table.heading(
    "Name",
    text="Name"
)

attendance_table.heading(
    "Date",
    text="Date"
)

attendance_table.heading(
    "Time",
    text="Time"
)

attendance_table.heading(
    "Status",
    text="Status"
)


attendance_table.column(
    "ID",
    width=100,
    anchor="center"
)

attendance_table.column(
    "Name",
    width=220,
    anchor="w"
)

attendance_table.column(
    "Date",
    width=160,
    anchor="center"
)

attendance_table.column(
    "Time",
    width=160,
    anchor="center"
)

attendance_table.column(
    "Status",
    width=140,
    anchor="center"
)


attendance_table.pack(
    fill="both",
    expand=True
)


# =========================================================
# STATUS COLORS
# =========================================================

def color_status_rows():

    attendance_table.tag_configure(
        "present",
        background="#143B37",
        foreground="#2DD4A7"
    )

    for item in attendance_table.get_children():

        values = attendance_table.item(
            item,
            "values"
        )

        if len(values) >= 5:

            status = str(
                values[4]
            ).lower()

            if status == "present":

                attendance_table.item(
                    item,
                    tags=("present",)
                )


# =========================================================
# SEARCH ENTRY BEHAVIOR
# =========================================================

def clear_search_placeholder(event):

    if (
        search_entry.get().strip()
        == "Search by ID or Name..."
    ):

        search_entry.delete(
            0,
            "end"
        )


search_entry.bind(
    "<FocusIn>",
    clear_search_placeholder
)

search_entry.bind(
    "<Return>",
    lambda event: search_records()
)


# =========================================================
# INITIAL LOAD
# =========================================================

update_statistics()

root.mainloop()

