import csv
import os

STUDENT_FILE = "students.csv"


def create_database():
    if not os.path.exists(STUDENT_FILE):
        with open(STUDENT_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name"])


def add_student(student_id, name):
    create_database()

    with open(STUDENT_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([student_id, name])


def get_student_name(student_id):
    create_database()

    with open(STUDENT_FILE, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["ID"] == str(student_id):
                return row["Name"]

    return "Unknown"