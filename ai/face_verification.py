import cv2


def detect_face(file_path):

    try:
        image = cv2.imread(file_path)

        if image is None:
            return {
                "face_detected": False,
                "face_count": 0,
                "error": "Unable to read image"
            }

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        cascade_path = (
            cv2.data.haarcascades
            + "haarcascade_frontalface_default.xml"
        )

        face_cascade = cv2.CascadeClassifier(cascade_path)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        return {
            "face_detected": len(faces) > 0,
            "face_count": len(faces)
        }

    except Exception as e:
        return {
            "face_detected": False,
            "face_count": 0,
            "error": str(e)
        }
