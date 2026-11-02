import cv2
import os
import numpy as np
from PIL import Image


def train_faces():

    dataset_path = "dataset"
    trainer_path = "trainer"

    # Trainer folder create karo
    if not os.path.exists(trainer_path):
        os.makedirs(trainer_path)

    # Haar Cascade XML
    cascade_path = "haarcascade/haarcascade_frontalface_default.xml"

    detector = cv2.CascadeClassifier(cascade_path)

    if detector.empty():
        print("ERROR: Haar Cascade load nahi hua.")
        return

    # LBPH Face Recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    face_samples = []
    ids = []

    # Dataset check
    if not os.path.exists(dataset_path):
        print("Dataset folder nahi mila.")
        return

    image_files = os.listdir(dataset_path)

    if len(image_files) == 0:
        print("Dataset empty hai.")
        print("Pehle capture_face.py run karo.")
        return

    print("Training ke liye images read ho rahi hain...")

    # Images read karo
    for file_name in image_files:

        if not file_name.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        image_path = os.path.join(dataset_path, file_name)

        # Image open
        pil_image = Image.open(image_path).convert("L")

        image_numpy = np.array(pil_image, "uint8")

        # Filename se student ID nikalo
        # Example: User.101.1.jpg
        try:
            student_id = int(file_name.split(".")[1])
        except:
            print("Invalid file:", file_name)
            continue

        # Face detect
        faces = detector.detectMultiScale(
            image_numpy,
            scaleFactor=1.1,
            minNeighbors=5
        )

        for (x, y, w, h) in faces:

            face_samples.append(
                image_numpy[y:y + h, x:x + w]
            )

            ids.append(student_id)

    # Check faces
    if len(face_samples) == 0:
        print("Koi face detect nahi hua.")
        return

    print("--------------------------------")
    print("Training start ho rahi hai...")
    print("Please wait...")
    print("--------------------------------")

    # Train model
    recognizer.train(
        face_samples,
        np.array(ids)
    )

    # Model save
    model_path = os.path.join(
        trainer_path,
        "trainer.yml"
    )

    recognizer.write(model_path)

    print("--------------------------------")
    print("TRAINING COMPLETE!")
    print("--------------------------------")
    print(f"Total faces trained: {len(face_samples)}")
    print(f"Model saved at: {model_path}")
    print("--------------------------------")


if __name__ == "__main__":
    train_faces()