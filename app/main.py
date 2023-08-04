import os
from flask import flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

from app import app
from utils import detect_properties, detect_text, detect_labels

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def upload_form():
    return render_template("upload.html")


@app.route("/", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)

    uploaded_file = request.files["file"]

    if uploaded_file.filename == "":
        flash("No image selected for uploading")
        return redirect(request.url)

    if uploaded_file and allowed_file(uploaded_file.filename):
        # filename = secure_filename(uploaded_file.filename)
        filename = "input"
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        uploaded_file.save(image_path)
        flash("Image successfully uploaded and displayed below")

        detect_text(image_path)
        image_properties = detect_properties(image_path)
        labels = detect_labels(image_path)

        return render_template(
            "upload.html",
            filename=filename,
            image_properties=image_properties,
            annotated_filename="output.png",
            labels=labels,
        )
    else:
        flash("Allowed image types are -> png, jpg, jpeg, gif")
        return redirect(request.url)


@app.route("/display/<filename>")
def display_image(filename):
    return redirect(url_for("static", filename="uploads/" + filename), code=301)


if __name__ == "__main__":
    app.run()
