import piexif
from PIL import Image, ExifTags
from todaysUnyang import exif_data_original

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
    image_exif = piexif.dump(exif_data_original.exif_data_changed)
    image.save(path, exif=image_exif, format='JPEG', quality=100)

if __name__ == '__main__':
    # 이미지 파일 경로
    exif_data_image_path = "E:\\OneDrive\\Algorithm\\Front end\\todaysUnyang\\todaysUnyang\\static\\20231122_153331.jpg"
    image_path = "E:\\OneDrive\\Algorithm\\Front end\\todaysUnyang\\todaysUnyang\\static\\unyang4cut\\COLLAGED\\33.png"
    path_100 = "E:\\OneDrive\\자료 및 출력\\김도현_첫돌사진_070707\\CRW_3175-DPP.JPG"
    # img = Image.open(exif_data_image_path)
    # exif_dict = piexif.load(img.info["exif"])
    # targetImg = Image.open(image_path)

    # targetImg.info["exif"] = piex if.dump(exif_dict)
    # exif_dump = piexif.dump(exif_dict)
    # targetImg.save(image_path, exif=exif_dump)

    # new_exif = exif_key_name_converter(exif_dict)

    # from exif_data_original import exif_data_changed

    # image = Image.open(image_path)
    # save_exif(image, image_path.replace('.png', '.jpg'), exif_data_changed)

    print(get_exif(Image.open(path_100)))