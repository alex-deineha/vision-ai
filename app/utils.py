from PIL import Image, ImageDraw
from google.cloud import vision

SERVICE_ACCOUNT_KEY_FILE_PATH = "app/static/organic-phoenix-387906-e6383a6c9158.json"
ANNOTATED_FILENAME = "app/static/uploads/output.png"
UPLOAD_FOLDER = "app/static/uploads"


def get_image_and_client(file_path):
    """Get image content and client"""
    client = vision.ImageAnnotatorClient.from_service_account_json(
        SERVICE_ACCOUNT_KEY_FILE_PATH
    )

    with open(file_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    return image, client


def draw_boxes(image_path, annotations):
    """Draw bounding box for each detected object"""
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    for annotation in annotations:
        vertices = annotation.bounding_poly.vertices
        draw.polygon(
            [(vertices[i].x, vertices[i].y) for i in range(4)], outline="green", width=5
        )

    image.save(ANNOTATED_FILENAME)


def check_response_error(response):
    """Check for errors in the response"""
    if response.error.message:
        raise Exception(
            f"{response.error.message}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors"
        )


def detect_properties(file_path):
    """Analyze image properties in the file"""
    image, client = get_image_and_client(file_path)
    response = client.image_properties(image=image)
    check_response_error(response)

    image_properties = []
    for color_info in response.image_properties_annotation.dominant_colors.colors:
        r, g, b = color_info.color.red, color_info.color.green, color_info.color.blue
        fraction = color_info.pixel_fraction
        color = f"rgb({r},{g},{b})"
        image_properties.append({"color": color, "fraction": fraction})

    return image_properties


def detect_text(file_path):
    """Detects text in the file"""
    image, client = get_image_and_client(file_path)
    response = client.text_detection(image=image)
    check_response_error(response)

    draw_boxes(file_path, response.text_annotations)


def detect_labels(file_path):
    """Detects labels in the file"""
    image, client = get_image_and_client(file_path)
    response = client.label_detection(image=image)
    check_response_error(response)

    return response.label_annotations


def main(file_path):
    detect_text(file_path)
    detect_properties(file_path)
    detect_labels(file_path)


if __name__ == "__main__":
    image_path = "/path/to/image.png"
    main(image_path)
