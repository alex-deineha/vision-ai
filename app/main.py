import os
from app import app
from flask import flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

from detect_text import analyze_image_properties, detect_text

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and extension(filename) in ALLOWED_EXTENSIONS


def extension(filename):
    return filename.rsplit(".", 1)[1].lower()


@app.route("/")
def upload_form():
    return render_template("upload.html")


@app.route("/", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        flash("No image selected for uploading")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        # print('upload_image filename: ' + filename)
        flash("Image successfully uploaded and displayed below")

        detect_text(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        image_properties = analyze_image_properties(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        print(filename)
        return render_template("upload.html",
                               filename=filename,
                               image_properties=image_properties,
                               annotated_filename="output.png")
    else:
        flash("Allowed image types are -> png, jpg, jpeg, gif")
        return redirect(request.url)


@app.route("/display/<filename>")
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for("static", filename="uploads/" + filename), code=301)


if __name__ == "__main__":
    app.run()
