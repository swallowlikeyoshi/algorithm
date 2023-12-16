from flask import render_template, request, Blueprint
import os
import json
from todaysUnyang import BASE_DIR
#from __init__ import BASE_DIR

# wand 라이브러리는 쓰려면 뭘 또 깔아야함... 젠장
# from wand.image import Image
# 차라리 다른 라이브러리를 쓰는게 낫지 https://wikidocs.net/153080
from PIL import Image, ImageDraw, ImageFont

unyang4cut = Blueprint('photo', __name__, url_prefix='/photo')

FOLDER_DIR = BASE_DIR + '\\static\\unyang4cut'

@unyang4cut.route('/', methods = ['GET'])
def photo():
    # 1. 기본 UI 제작
    # 2. HTMX 요청 코드 제작
    # 3. 템플릿 렌더해서 리턴
    return render_template('unyang4cut.html')

@unyang4cut.route('/folders', methods = ['GET'])
def getAllFiles():
    # 1. unyang4cut 폴더 내 모든 폴더 이름 가져오기
    foldersArray = os.listdir(FOLDER_DIR)
    foldersArray.remove('FRAMES')
    # print(foldersArray)
    # 2. HTML화 하기
    if len(foldersArray) == 0:
        option = {
            'class': 'emptyFolder btn btn-light'
        }
        elements = _elementWrapper('p', '폴더가 없어요.<br>나중에 다시 시도해 주세요.', option)
    else:
        elements = ''
        for folderName in foldersArray:
            option = {
                'class': 'folderName btn btn-light',
                'hx-get': f'/photo/images?file_name={folderName}',
                'hx-target': '#box'
            }
            element = _elementWrapper('p', folderName, option)
            elements = elements + element
        # 3. 전송하기
    elements = _elementWrapper('div', elements, { 'class': 'd-flex flex-column justify-content-around' })
    return elements

@unyang4cut.route('/images', methods = ['GET'])
def getAllImages():
    reqName = request.args.get('file_name')
    # reqName = '20803'
    try:
        # 1. 같은 이름을 가진 폴더 찾기
        foldersArray = os.listdir(FOLDER_DIR)
        folderName = foldersArray[foldersArray.index(reqName)]
        # 2. 폴더 안의 모든 이미지의 이름 가져오기
        IMAGE_DIR = FOLDER_DIR + '\\' + folderName
        filesArray = os.listdir(IMAGE_DIR)
        imagesArray = []
        for fileName in filesArray:
            if '.jpg' in fileName:
                imagesArray.append(fileName)
    except:
        return '사진이 없어요.'
    
    # 3. 가져온 이미지를 HTML화 하기
    elements = ''
    for imageName in imagesArray:
        HTML_dir = f'/static/unyang4cut/{folderName}/{imageName}'
        # element = f'<img class="img-fluid rounded mb-4 mb-lg-0" src="{HTML_dir}" alt="{imageName}" onclick="pushImage(this.src)"/>'
        
        # 가져온 이미지들을 요소화 하기
        option = {
            'class': 'takenImages img-fluid rounded mb-4 mb-lg-0',
            'src': HTML_dir,
            'alt': imageName,
            'onclick': 'pushImage(this.src, this.alt)'
        }
        element = _inline_elementWrapper('img', option)

        elements = elements + element
    # 4. 전송하기

    # 현재 폴더 표시용 버튼
    option = {
        'type': 'button',
        'class': 'btn btn-primary',
        'id': 'indicator'
    }
    indicator = _elementWrapper('button', folderName, option)

    # 뒤로가기 버튼
    option = { 
        'type': 'button',
        'class': 'btn btn-secondary',
        'hx-get': '/photo/folders',
        'hx-target': '#box'
    }
    btn = _elementWrapper('button', '뒤로 가기', option)

    backButton = _elementWrapper('div', indicator+btn, { 'class': 'd-flex p-2 justify-content-center' })
    elements = backButton + elements
    return elements

@unyang4cut.route('/collage', methods = ['GET'])
def getCollagedImage():
    getJson = request.args.get('json')
    collage = json.loads(getJson)
    imageNames = []
    for image in collage['images']:
        imageNames.append(image['fileName'].replace('%20', ' '))
    collagedImageName = _imageCollage(collage['frame'], collage['folderName'], imageNames)
    HTML_dir = f'/static/unyang4cut/{collage["folderName"]}/COLLAGED/{collagedImageName}'
    option = {
        'class': 'img-fluid rounded mb-4 mb-lg-0',
        'id': 'collagedImage',
        'src': HTML_dir,
        'alt': collagedImageName
    }
    element = _inline_elementWrapper('img', option)
    return element

def _imageCollage(frameName: str, folderName: str, imagesArray: list):
    FRAME_WIDTH = 1000
    FRAME_HEIGHT = 3000
    MARGIN = 40

    # 1. 프레임 가져오기
        # frameName = 'black'
    frameImage = Image.open(fp=f'{FOLDER_DIR}\\FRAMES\\{frameName}.png')
    overlayImage = frameImage

    # 2. 선택한 이미지 불러오기
    IMAGE_DIR = FOLDER_DIR + '\\' + folderName
    # images = list()
    # for imageName in imagesArray:
    #     images.append(Image.open(fp=IMAGE_DIR + '\\' + imageName))
    images = [Image.open(fp=IMAGE_DIR + '\\' + imageName) for imageName in imagesArray]

    # 3. 이미지 합성하기
    imageNum = 0
    for image in images:
        if imageNum > 3:
            break
        # 1. 이미지 크기 조절하기
            # 이거 원본 이미지랑 비율 어긋나면 나중가서 이상해질 듯
            # 인생네컷 비율은 3:2인듯
            # 1. 원본 비율에 맞게 가로가 900으로 리사이징하기
        # image = Image.open('')
        ratio = image.width / image.height
        resizedImage = image.resize((FRAME_WIDTH - (MARGIN * 2), int(900 * (1 / ratio))))
            # 2. 위아래를 잘라서 높이 600에 맞추기
        resizedImage = resizedImage.crop((0, int((resizedImage.height - 600) / 2), resizedImage.width, int(((resizedImage.height - 600) / 2) + 600)))
        # 2. 이미지 위치 자동 조절하며 사진 붙여넣기 -> 일단 기본 프레임부터 완성하고 하자
        frameImage.paste(resizedImage, ((MARGIN, MARGIN + ((600 + MARGIN) * imageNum))))
        imageNum += 1
    frameImage.paste(overlayImage, (0,0))

    # 3.5. 이미지 저장하기, 근데 중복이면 이름 바꾸기
    try:
        os.mkdir(IMAGE_DIR + '\\COLLAGED')
    except:
        pass
    imagesArray = os.listdir(IMAGE_DIR + '\\COLLAGED')
    if len(imagesArray) == 0 :
        frameImage.save(f'{IMAGE_DIR}\\COLLAGED\\{folderName}.png')
        return f'{folderName}.png'
    else:
        frameImage.save(f'{IMAGE_DIR}\\COLLAGED\\{folderName} ({str(len(imagesArray))}).png')
        return f'{folderName} ({str(len(imagesArray))}).png'

def _elementWrapper(tag: str, contents: str, option: dict):
    optstr = ''
    for i in option.keys():
        optstr += f' {i}="{option[i]}"'
    element = f'<{tag} {optstr}>{contents}</{tag}>'
    return element

def _inline_elementWrapper(tag: str, option: dict):
    optstr = ''
    for i in option.keys():
        optstr += f' {i}="{option[i]}"'
    element = f'<{tag} {optstr}/>'
    return element


if __name__ == '__main__':
    # print(_get_all_files())
    # print(_get_all_images())
    #print(_imageCollage('black', '10101', ['1.jpg', '2.jpg', '3.jpg', '4.jpg']))
    print(getCollagedImage('{"frame":"black","folderName":"20803","images":["http://127.0.0.1/static/unyang4cut/10101/2.jpg","http://127.0.0.1/static/unyang4cut/10101/2.jpg","http://127.0.0.1/static/unyang4cut/10101/2.jpg","http://127.0.0.1/static/unyang4cut/10101/2.jpg"]}'))