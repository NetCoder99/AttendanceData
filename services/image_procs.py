import base64
import io
import re
from io import BytesIO
from PIL import Image
from PIL.ExifTags import TAGS


def GetImageTypeBase64(base64_string: str) -> dict:
    if base64_string is None:
        return {
            'image_type' : None,
            'image_date': None
        }
    img_bytes  = base64.b64decode(base64_string)
    img_file   = BytesIO(img_bytes)
    img        = Image.open(img_file)
    image_type = img.format

    exif_data = img.getexif()
    exif_dict = {}
    for tag_id, value in exif_data.items():
        tag_name = TAGS.get(tag_id, tag_id)
        exif_dict[tag_name] = value
        #print(f"{tag_name}: {value}")

    image_date = exif_dict['DateTime'].replace(":", "-", 2)
    rtn_dict   = {
        'image_type' : image_type,
        'image_date': image_date
    }
    return rtn_dict


def GetImageTypeBytes(image_bytes: bytes) -> dict:
    # img_bytes  = base64.b64decode(base64_string)
    # img_file   = BytesIO(img_bytes)
    img = Image.open(io.BytesIO(image_bytes))
    #img        = Image.frombytes(image_bytes)
    image_type = img.format

    exif_data = img.getexif()
    exif_dict = {}
    for tag_id, value in exif_data.items():
        tag_name = TAGS.get(tag_id, tag_id)
        exif_dict[tag_name] = value
        #print(f"{tag_name}: {value}")

    image_date = exif_dict['DateTime'].replace(":", "-", 2)
    rtn_dict   = {
        'image_type' : image_type,
        'image_date': image_date
    }
    return rtn_dict


# # Your base64 encoded image string
# b64_string = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
#
# # 1. Decode the base64 string into raw bytes
# img_bytes = base64.b64decode(b64_string)
#
# # 2. Convert bytes into a file-like object using BytesIO
# img_file = BytesIO(img_bytes)
#
# # 3. Open the image with Pillow
# img = Image.open(img_file)
#
# # 4. Extract the image type (e.g., 'PNG', 'JPEG', 'GIF')
# image_type = img.format
#
# print(f"The image type is: {image_type}")