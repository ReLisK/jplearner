import io
import os
import configparser
import constants
import utils

# Imports the Google Cloud client library
from google.cloud import vision
from google.oauth2 import service_account
config = configparser.ConfigParser()
config.read(constants.CONFIG_FILE)



def google_vision_ocr(path):
    credentials = service_account.Credentials.from_service_account_file(config['DEFAULT']['G_ocr'])
    """Detects text in the file."""
    from google.cloud import vision
    import io
    # Instantiates a client
    client = vision.ImageAnnotatorClient(credentials=credentials)

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    tokens = []
    try:
        for text in texts:
            tokens.append("{}".format(text.description))

            # Bounding boxes, dnt need this right now..
            # vertices = (['({},{})'.format(vertex.x, vertex.y)
            #             for vertex in text.bounding_poly.vertices])
            #
            # print('bounds: {}'.format(','.join(vertices)))

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))
        else:
            return tokens
    except Exception as e:
        utils.qt_alert(f"Error: \n{e}")
