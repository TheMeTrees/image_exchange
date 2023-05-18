from PIL import Image
from .Exceptions.image_not_found_error import ImageNotFoundError


class Utils:

    @staticmethod
    def open_image(image_path):
        try:
            # Open the JPG file
            image = Image.open(image_path)
            return image
        except FileNotFoundError:
            raise ImageNotFoundError(image_path)
