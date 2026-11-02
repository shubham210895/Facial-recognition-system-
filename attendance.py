import cv2
import csv
import os
import time
from datetime import datetime
from database import get_student_name


def mark_attendance(student_id):
    attendance_folder = "attendance"

    if not os.path.exists(attendance_folder):
        os.makedirs(attendance_folder)

    today = datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join(
        attendance_folder,
        f"attendance_{today}.csv"
    )

    file_exists = os.path.exists(file_path)
    already_marked = False

    if file_exists:
        with open(
            file_path,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:
                if row["ID"] == str(student_id):
                    already_marked = True
                    break

    if not already_marked:

        current_time = datetime.now().strftime("%H:%M:%S")
        name = get_student_name(student_id)

        with open(
            file_path,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(
                    ["ID", "Name", "Date", "Time", "Status"]
                )

            writer.writerow(
                [
                    student_id,
                    name,
                    today,
                    current_time,
                    "Present"
                ]
            )

        print("--------------------------------")
        print("ATTENDANCE MARKED!")
        print("--------------------------------")
        print("Name:", name)
        print("ID:", student_id)
        print("Date:", today)
        print("Time:", current_time)
        print("--------------------------------")

        return True

    else:
        print("Attendance already marked for today.")
        return False


def recognize_faces():

    print("Loading model...")

    model_path = "trainer/trainer.yml"

    if not os.path.exists(model_path):
        print("ERROR: trainer.yml nahi mila.")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(model_path)

    print("Model loaded successfully.")

    cascade_path = (
        "haarcascade/"
        "haarcascade_frontalface_default.xml"
    )

    if not os.path.exists(cascade_path):
        print("ERROR: Haar Cascade XML nahi mila.")
        return

    face_cascade = cv2.CascadeClassifier(cascade_path)

    if face_cascade.empty():
        print("ERROR: Face detector load nahi hua.")
        return

    print("Face detector loaded.")
    print("Camera start ho raha hai...")

    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not camera.isOpened():

        print("Camera method 1 failed.")

        camera.release()
        camera = cv2.VideoCapture(0)

    if not camera.isOpened():

        print("ERROR: Camera open nahi ho raha.")
        return

    print("--------------------------------")
    print("CAMERA STARTED!")
    print("--------------------------------")
    print("Face camera ke saamne rakho.")
    print("Face recognize hone ke baad camera")
    print("automatically close ho jayega.")
    print("--------------------------------")

    attendance_done = False
    recognized_name = ""

    while True:

        ret, frame = camera.read()

        if not ret:
            print("Camera se frame nahi mil raha.")
            break

        frame = cv2.flip(frame, 1)

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(100, 100)
        )

        for (x, y, w, h) in faces:

            student_id, confidence = recognizer.predict(
                gray[y:y+h, x:x+w]
            )

            confidence_percentage = round(
                100 - confidence
            )

            if confidence_percentage >= 50:

                name = get_student_name(student_id)

                label = (
                    f"{name} "
                    f"({confidence_percentage}%)"
                )

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x+w, y+h),
                    (0, 255, 0),
                    3
                )

                cv2.putText(
                    frame,
                    "ATTENDANCE MARKED",
                    (x, y-40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    label,
                    (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

                if not attendance_done:

                    mark_attendance(student_id)

                    attendance_done = True
                    recognized_name = name

                    cv2.imshow(
                        "Facial Recognition Attendance",
                        frame
                    )

                    cv2.waitKey(2000)

                    camera.release()
                    cv2.destroyAllWindows()

                    print("--------------------------------")
                    print(
                        f"Welcome {recognized_name}!"
                    )
                    print(
                        "Attendance successfully marked."
                    )
                    print("Camera closed automatically.")
                    print("--------------------------------")

                    return

            else:

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x+w, y+h),
                    (0, 0, 255),
                    2
                )

                cv2.putText(
                    frame,
                    "Unknown",
                    (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

        cv2.imshow(
            "Facial Recognition Attendance",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

    print("Face recognition stopped.")


if __name__ == "__main__":
    recognize_faces()