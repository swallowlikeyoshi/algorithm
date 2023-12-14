from flask import session, redirect, url_for, render_template, request, Blueprint
import os
#from todaysUnyang import BASE_DIR
from __init__ import BASE_DIR

# wand 라이브러리는 쓰려면 뭘 또 깔아야함... 젠장
# from wand.image import Image
# 차라리 다른 라이브러리를 쓰는게 낫지 https://wikidocs.net/153080
from PIL import Image, ImageDraw, ImageFont

unyang4cut = Blueprint('photo', __name__, url_prefix='/photo')

FOLDER_DIR = BASE_DIR + '\\static\\unyang4cut'

@unyang4cut.route('/', methods = ['GET'])
def lobby():
    # 1. 기본 UI 제작
    # 2. HTMX 요청 코드 제작
    # 3. 템플릿 렌더해서 리턴
    return 'Hello'

@unyang4cut.route('/_getFiles', methods = ['GET'])
def _get_all_files():
    # 1. unyang4cut 폴더 내 모든 폴더 이름 가져오기
    foldersArray = os.listdir(FOLDER_DIR)
    # print(foldersArray)
    # 2. HTML화 하기
    elements = ''
    for folderName in foldersArray:
        element = '<p class="folder">' + folderName + '</p><br>\n'
        elements = elements + element
    # 3. 전송하기
    return elements


@unyang4cut.route('/_getImages', methods = ['GET'])
def _get_all_images():
    # reqName = request.args.get('file_name')

    # 디버그용
    reqName = '20803'

    try:
        # 1. 같은 이름을 가진 폴더 찾기
        foldersArray = os.listdir(FOLDER_DIR)
        folderName = foldersArray[foldersArray.index(reqName)]
        # 2. 폴더 안의 모든 이미지의 이름 가져오기
        IMAGE_DIR = FOLDER_DIR + '\\' + folderName
        imagesArray = os.listdir(IMAGE_DIR)
    except:
        return '사진이 없어요.'
    # 3. 가져온 이미지를 HTML화 하기
    elements = ''
    for imageName in imagesArray:
        HTML_dir = '/unyang4cut/' + folderName + '/' + imageName
        element = '<img class="img-fluid rounded mb-4 mb-lg-0" src="' + HTML_dir +  '" alt="unyang4cut" />'
        # div로 한번 두르는게 나을까?
        element = '<div class="card">' + element + '</div>\n'
        elements = elements + element
    # 4. 전송하기
    return elements

@unyang4cut.route('/sel', methods = ['GET'])
def select():
    file_name = request.args.get('file_name')
    # 1. 사진 선택, 프레임 선택 UI 구현
        # 이미지 합성 로직은 백엔드에서? 프론트에서? -> 백에서 하는게 나을듯 https://wikidocs.net/26375
        # 1. 사진과 프레임 선택 후 확인
        # 2. 선택한 사진과 프레임 프론트 목록 -> 백 전송
        # 3. 백에서 사진과 프레임 합성
        # 4. 동 폴더 아래 저장
        # 5. 이미지 띄우기
    # 2. HTMX 요청 전송 코드 제작
        # 1. 새 창으로 이미지 띄우기 -> 라우트를 하나 더 만들어야 할 듯
        # 2. 다운로드 버튼 만들기
        # 3. 인스타 공유 버튼? 할수있으면 해보고 -> 앱에서만 되는 듯, 웹앱 만들거야? 정말로? x
    # 3. 다운로드
    return

def _imageCollage(frameName, folderName, imagesArray):
    # 1. 프레임 가져오기
    frameName = 'black'
    frameImage = Image.open(fp=FOLDER_DIR + '\\FRAMES\\' + frameName + '.png')
    # 2. 선택한 이미지 불러오기
    IMAGE_DIR = FOLDER_DIR + '\\' + folderName
    images = list()
    for imageName in imagesArray:
        images.append(Image.open(fp=IMAGE_DIR + '\\' + imageName))
    # 3. 이미지 합성하고 저장하기
    margin = 0
    for image in images:
        # 1. 이미지 크기 조절하기
        resizedImage = image.resize((400, 300))
        # 2. 이미지 위치 자동 조절하며 사진 붙여넣기 -> 일단 기본 프레임부터 완성하고 하자
        frameImage.paste(resizedImage, (100, 100 + margin))
        margin += 100
    # frameImage.show()
    frameImage.save(fp=IMAGE_DIR + '\\' + folderName + '.png')
    # 4. 이미지 주소 or 파일명 반환하기
    collagedImage = IMAGE_DIR + '\\' + folderName + '.png'
    return collagedImage


if __name__ == '__main__':
    # print(_get_all_files())
    # print(_get_all_images())
    print(_imageCollage('black', '20803', {'_1311150.jpg'}))