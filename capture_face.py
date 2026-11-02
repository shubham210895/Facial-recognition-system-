import cv2
import os


def capture_faces(student_id):

    dataset_path = "dataset"

    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

    cascade_path = "haarcascade/haarcascade_frontalface_default.xml"
    face_detector = cv2.CascadeClassifier(cascade_path)

    if face_detector.empty():
        print("ERROR: Face detector load nahi hua.")
        return

    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not camera.isOpened():
        camera.release()
        camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("ERROR: Camera open nahi ho raha.")
        return

    count = 0

    print("Camera started...")
    print("Face camera ke saamne rakho.")

    while True:

        ret, frame = camera.read()

        if not ret:
            break

        frame = cv2.flip(frame, 1)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_detector.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(80, 80)
        )

        for (x, y, w, h) in faces:

            count += 1

            file_name = os.path.join(
                dataset_path,
                f"User.{student_id}.{count}.jpg"
            )

            cv2.imwrite(
                file_name,
                gray[y:y+h, x:x+w]
            )

            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                (255, 0, 0),
                2
            )

            cv2.putText(
                frame,
                f"Images: {count}/30",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        cv2.imshow("Face Capture", frame)

        if cv2.waitKey(100) & 0xFF == ord("q"):
            break

        if count >= 30:
            break

    camera.release()
    cv2.destroyAllWindows()

    print("Face capture complete!")
    print(f"Total images: {count}")


if __name__ == "__main__":
    # Ye sirf testing ke liye hai.
    student_id = input("Enter Student ID: ").strip()

    if student_id:
        capture_faces(student_id)