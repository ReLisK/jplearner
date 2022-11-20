import os

from PIL import Image, ImageGrab


def get_snippet(location, filename, coordinates=None):
    if coordinates is not None:
        if coordinates[0] > coordinates[2] and coordinates[1] > coordinates[3]:
            temp = (coordinates[2], coordinates[3], coordinates[0], coordinates[1])
            coordinates = temp
    snapshot = ImageGrab.grab(bbox=coordinates)
    save_path = os.path.join(
        location,
        filename
    )
    snapshot.save(save_path)
    return save_path
