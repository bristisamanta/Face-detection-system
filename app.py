
import os
import cv2
import uuid
from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp", "webp"}

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/", methods=["GET", "POST"])
def home():
    result_image = None
    face_count = None
    error = None

    if request.method == "POST":
        file = request.files.get("image")

        if not file or file.filename == "":
            error = "Please select an image first."

        elif not allowed_file(file.filename):
            error = "Please upload a JPG, PNG, BMP, or WEBP image."

        else:
            filename = secure_filename(file.filename)
            extension = filename.rsplit(".", 1)[1].lower()
            unique_name = f"{uuid.uuid4().hex}.{extension}"
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)

            try:
                file.save(image_path)

                image = cv2.imread(image_path)

                if image is None:
                    os.remove(image_path)
                    error = "The uploaded file is not a valid image."
                else:
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                    faces = face_cascade.detectMultiScale(
                        gray,
                        scaleFactor=1.15,
                        minNeighbors=8,
                        minSize=(40, 40)
                  )

                    for (x, y, w, h) in faces:
                        cv2.rectangle(
                            image,
                            (x, y),
                            (x + w, y + h),
                            (40, 220, 120),
                            3
                        )

                    cv2.imwrite(image_path, image)

                    result_image = url_for(
                        "static",
                        filename=f"uploads/{unique_name}"
                    )
                    face_count = len(faces)

            except Exception:
                error = "Something went wrong while processing the image."

    return render_template(
        "index.html",
        result_image=result_image,
        face_count=face_count,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
