import os

from PIL import Image, ImageGrab


def get_snippet(location, filename, coordinates=None):
    snapshot = ImageGrab.grab(bbox=coordinates)
    save_path = os.path.join(
        location,
        filename
    )
    snapshot.save(save_path)
    return save_path
