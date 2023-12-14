from flask import session, redirect, url_for, render_template, request, Blueprint
import os
#from todaysUnyang import BASE_DIR
from __init__ import BASE_DIR

unyang4cut = Blueprint('photo', __name__, url_prefix='/photo')

FOLDER_DIR = BASE_DIR + '\\static\\unyang4cut'

@unyang4cut.route('/', methods = ['GET'])
def lobby():

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
        # 이미지 합성 로직은? 백엔드에서? 프론트에서? -> 백에서 하는게 나을듯 https://wikidocs.net/26375
    # 2. HTMX 요청 전송 코드 제작
    # 3. 다운로드
    return

if __name__ == '__main__'
    print(_get_all_files())
    print(_get_all_images())