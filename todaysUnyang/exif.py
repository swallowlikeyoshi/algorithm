import piexif
from PIL import Image, ExifTags

from todaysUnyang import exif_data

def exif_key_name_converter(exif_dict: dict):
    new_exif_dict = dict()

    for first in exif_dict.keys():
        if first == "thumbnail":
            continue
        new_exif_dict[first] = dict()
        for second in exif_dict[first].keys():
            try:
                new_exif_dict[first][ExifTags.TAGS[second]] = exif_dict[first][second]
            except:
                new_exif_dict[first][second] = exif_dict[first][second]

    return new_exif_dict

def get_exif(image: Image):
    exif_dict = piexif.load(image.info['exif'])
    return exif_dict

def save_exif(image: Image, path: str, exif: dict):
    exif_dump = piexif.dump(exif)
    image.save(path, exif = exif_dump, format='JPEG', quality=100)

def add_exif_and_save(image: Image, path: str):
    image = image.convert("RGB")
    image_exif = piexif.dump(exif_data.exif_data_changed)
    image.save(path, exif=image_exif, format='JPEG', quality=100)

if __name__ == '__main__':
    # 이미지 파일 경로
    image_path = input()
    print(get_exif(Image.open(image_path)))