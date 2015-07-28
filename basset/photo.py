from PIL import Image
from cStringIO import StringIO
import base64

def dhash(encoded_image, hash_size = 8):
    image = Image.open(StringIO(base64.b64decode(encoded_image)))

    image = image.convert('L').resize(
        (hash_size + 1, hash_size),
        Image.ANTIALIAS
    )

    pixels = list(image.getdata())

    # Compare adjacent pixels
    difference = []
    for row in xrange(hash_size):
        for col in xrange(hash_size):
            pixel_left = image.getpixel((col, row))
            pixel_right = image.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)

    # Convert the binary array to a hexadecimal string
    decimal_value = 0
    hex_string = []
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2**(index % 8)
        if (index % 8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2,'0'))
            decimal_value = 0

    return ''.join(hex_string)