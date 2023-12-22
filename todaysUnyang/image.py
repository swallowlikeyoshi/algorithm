from PIL import Image, ExifTags

def modify_exif(image_path, new_exif_data):
    # 이미지 열기
    image = Image.open(image_path)

    # 이미지의 현재 EXIF 정보 가져오기
    exif_data = image.info.get('exif', b'')

    # 새로운 EXIF 데이터 추가 또는 기존 데이터 수정
    exif_data += new_exif_data

    # 수정된 EXIF 데이터를 이미지에 적용
    image.save(image_path, exif=exif_data)

# 이미지 파일 경로
image_path = "E:\\OneDrive\\Algorithm\\Front end\\todaysUnyang\\todaysUnyang\\static\\image.jpg"

# # 수정할 EXIF 데이터 (예: 제조사, 모델)
# new_exif_data = {
#     ExifTags.TAGS[271]: 'YourMake'
#     # 추가적인 EXIF 태그 및 값은 필요에 따라 추가할 수 있습니다.
# }

new_exif_data = b'Make\x00YourMake\x00Model\x00YourModel\x00'

# for idx in ExifTags.TAGS.keys():
#     if ExifTags.TAGS[idx] == 'Make':
#         print(idx)

# EXIF 수정 함수 호출
modify_exif(image_path, new_exif_data)

