from PIL import Image, ImageDraw
from google.cloud import vision

def draw_boxes(image_path, response):
    # Open the image file
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # For each detected object, draw the bounding box
    for annotation in response.text_annotations:
        vertices = annotation.bounding_poly.vertices
        draw.polygon([
            vertices[0].x, vertices[0].y,
            vertices[1].x, vertices[1].y,
            vertices[2].x, vertices[2].y,
            vertices[3].x, vertices[3].y], outline='green')

    # Save the new image
    image.save('output.jpg')

def analyze_image_properties(path):
    """Analyze image properties in the file."""
    service_account_key_file_path = "/Users/alexanderdeineha/PycharmProjects/vision-ai/app/static/organic-phoenix-387906-f9a188e350aa.json"
    client = vision.ImageAnnotatorClient.from_service_account_json(service_account_key_file_path)

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.image_properties(image=image)
    props = response.image_properties_annotation
    print('Properties of the image:')

    for color in props.dominant_colors.colors:
        print('Fraction: {}'.format(color.pixel_fraction))
        print('\tR: {}'.format(color.color.red))
        print('\tG: {}'.format(color.color.green))
        print('\tB: {}'.format(color.color.blue))
        print('\tAlpha: {}'.format(color.color.alpha))

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )


def detect_text(path):
    """Detects text in the file."""
    service_account_key_file_path = "/Users/alexanderdeineha/PycharmProjects/vision-ai/app/static/organic-phoenix-387906-f9a188e350aa.json"
    client = vision.ImageAnnotatorClient.from_service_account_json(service_account_key_file_path)

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)


    response = client.text_detection(image=image)
    print(response.text_annotations)
    draw_boxes(path, response)

    texts = response.text_annotations
    print("Texts:")

    for text in texts:
        print(f'\n"{text.description}"')

        vertices = [
            f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
        ]

        print("bounds: {}".format(",".join(vertices)))

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )


if __name__ == '__main__':
    image_path = "/Users/alexanderdeineha/PycharmProjects/vision-ai/app/static/uploads/sample"
    detect_text(image_path)
    analyze_image_properties(image_path)
