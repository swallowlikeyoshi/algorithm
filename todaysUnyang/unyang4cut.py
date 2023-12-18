from flask import render_template, request, Blueprint
import urllib
from urllib.parse import unquote
import os
import json
from todaysUnyang import BASE_DIR
#from __init__ import BASE_DIR

# wand 라이브러리는 쓰려면 뭘 또 깔아야함... 젠장
# from wand.image import Image
# 차라리 다른 라이브러리를 쓰는게 낫지 https://wikidocs.net/153080
from PIL import Image, ImageDraw, ImageFont


unyang4cut = Blueprint('photo', __name__, url_prefix='/photo')

FOLDER_DIR = os.path.join(BASE_DIR, 'static', 'unyang4cut')

@unyang4cut.route('/', methods = ['GET'])
def photo():
    # 1. 기본 UI 제작
    # 2. HTMX 요청 코드 제작
    # 3. 템플릿 렌더해서 리턴
    return render_template('unyang4cut.html')

@unyang4cut.route('/folders', methods=['GET'])
def getAllFiles():
    try:
        # 1. unyang4cut 폴더 내 모든 폴더 이름 가져오기
        foldersArray = [folder for folder in os.listdir(FOLDER_DIR) if os.path.isdir(os.path.join(FOLDER_DIR, folder))]

        folderBlackList = ['FRAMES', 'COLLAGED']
        foldersArray = [folder for folder in foldersArray if all(blackFolder not in folder for blackFolder in folderBlackList)]

        # 2. HTML화 하기
        if not foldersArray:
            option = {
                'class': 'emptyFolder btn btn-light'
            }
            ValueError(_elementWrapper('p', '폴더가 없어요.<br>나중에 다시 시도해 주세요.', option))
        else:
            elements = ''
            for folderName in foldersArray:
                option = {
                    'class': 'folderName btn btn-light',
                    'hx-get': f'/photo/images?file_name={urllib.parse.quote(folderName)}',
                    'hx-target': '#box'
                }
                element = _elementWrapper('p', folderName, option)
                elements += element
    except ValueError as e:
        return str(e)
    except Exception:
        return '파일 불러오기 오류.'

    # 3. 전송하기
    elements = _elementWrapper('div', elements, {'class': 'd-flex flex-column justify-content-around'})
    return elements

@unyang4cut.route('/images', methods = ['GET'])
def getAllImages():
    reqName = request.args.get('file_name')

    # GPT
    try:
        # 1. 같은 이름을 가진 폴더 찾기
        if reqName not in os.listdir(FOLDER_DIR):
            raise ValueError(f"폴더 '{reqName}'을 찾을 수 없습니다.")
        folderName = reqName

        # 1.5 이미지 리사이징 하기
        _imageResize(folderName)

        # 2. 폴더 안의 모든 이미지의 이름 가져오기
        IMAGE_DIR = os.path.join(FOLDER_DIR, folderName, 'RESIZED')
        filesArray = os.listdir(IMAGE_DIR)
        filesArray = [fileName for fileName in os.listdir(IMAGE_DIR)]
        imagesArray = []
        for fileName in filesArray:
            if '.jpg' or '.JPG' in fileName:
                imagesArray.append(fileName)

    except ValueError as ve:
        return f'이미지 불러오기 오류: {str(ve)}'
    except Exception as e:
        return f'이미지 불러오기 오류.'
    
    # 3. 가져온 이미지를 HTML화 하기
    elements = ''
    for imageName in imagesArray:
        HTML_dir = f'/static/unyang4cut/{folderName}/RESIZED/{imageName}'
        # 가져온 이미지들을 요소화 하기
        option = {
            'class': 'takenImages img-fluid rounded mb-4 mb-lg-0',
            'src': HTML_dir,
            'alt': imageName,
            'onclick': 'pushImage(this.src, this.alt)'
        }
        element = _inline_elementWrapper('img', option)
        elements = elements + element

    # 현재 폴더 표시용 버튼
    option = {
        'type': 'button',
        'class': 'btn btn-primary',
        'id': 'indicator',
        'onload': 'setFolderName(this.alt)',
        'alt': folderName
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

    # 4. 전송하기
    return elements

@unyang4cut.route('/frames', methods = ['GET'])
def getAllFrames():
    FRAME_DIR = os.path.join(FOLDER_DIR, 'FRAMES')
    HTML_DIR = f'/static/unyang4cut/FRAMES'

    # 1. 프레임 JSON 파일 가져오기
    try:
        with open(os.path.join(FRAME_DIR, 'FRAMES.json'), 'r', encoding='UTF-8') as json_file:
            framesData = json.load(json_file)
    except Exception as e:
        return f'프레임 정보를 가져오는 중에 오류가 발생했어요.'
    
    # 2. 각 프레임 html화 하기
    frameElements = []
    for frame in framesData['FRAMES']:
        if frame['IS_OVERLAYED']:
            overlayFileName = frame['OVERLAY_FILE_NAME']
        else:
            overlayFileName = 'clear.png'
        # 1. img 태그 이용해서 프레임 이미지 띄우는 요소
        option = {
            'class': 'frameImage p-2',
            'onclick': "setFrame(this.src, this.alt, this.getAttribute('overlay'))",
            'src': f'{HTML_DIR}/{frame["FILE_NAME"]}',
            'alt': f'{frame["NAME"]}',
            'overlay': f'{HTML_DIR}/{overlayFileName}'
        }
        imageElement = _inline_elementWrapper('img', option)

        # 2. 이미지 아래 프레임 이름 띄우는 요소
        option = {
            'class': 'frameName p-2',
            'onlick': 'setFrame(this.src, this.alt, this.overlay)',
            'src': f'{HTML_DIR}/{frame["FILE_NAME"]}',
            'alt': f'{frame["NAME"]}',
            'overlay': f'{HTML_DIR}/{overlayFileName}'
        }
        nameElement = _elementWrapper('p', frame["DISPLAY_NAME"], option)

        option = {
            'class': 'card p-2',
            'style': 'width: 45%; margin-right: 10px; min-width: 100px;'
        }
        element = _elementWrapper('div', imageElement + nameElement, option)
        frameElements.append(element)

    finalElement = ''
    for frame in frameElements:
        finalElement = finalElement + frame
    finalElement = _elementWrapper('div', finalElement, { 'class': 'd-flex flex-row overflow-auto' })
    return finalElement

@unyang4cut.route('/collage', methods = ['GET'])
def getCollagedImage():
    getJson = request.args.get('json')
    collage = json.loads(getJson)

    # 1. HTML 경로에서 PATH로 바꾸기
    selectedImageInfo = []
    for image in collage['images']:
        decoded_path = unquote(image['url'].split("/static/unyang4cut/")[-1])
        windows_path = os.path.join(*decoded_path.split("/"))
        selectedImageInfo.append({ 'dir': FOLDER_DIR + '\\' + windows_path, 'fileName': image['fileName'].replace('%20', ' ') })

    # 2. PATH를 이용해서 이미지 합치기
    collagedImageName = _imageCollage(collage['frame'], selectedImageInfo)

    HTML_dir = f'/static/unyang4cut/COLLAGED/{collagedImageName}'
    option = {
        'class': 'img-fluid rounded mb-4 mb-lg-0',
        'id': 'collagedImage',
        'src': HTML_dir,
        'alt': collagedImageName
    }
    collagedImageElement = _inline_elementWrapper('img', option)
    
    modal_body = _elementWrapper('div', collagedImageElement, { 'id': 'result', 'class': 'd-flex justify-content-center text-center p-2', 'style': 'background-color: grey;'})
    modal_footer = '<button type="button" class="btn btn-secondary" data-bs-dismiss="modal" hx-get="/photo/closeDownloadModal" hx-target="#collageLoading">닫기</button><a href="#" id="downloadBtn" download><button type="button" class="btn btn-primary" onclick="download()">네컷만 저장하기</button></a><button type="button" class="btn btn-success" onclick="downloadAllFiles()">네컷과 이미지 모두 저장하기</button>'
    modal_footer = _elementWrapper('div', modal_footer, { 'class': 'modal-footer'})
    return modal_body + modal_footer

@unyang4cut.route('/closeDownloadModal', methods = ['GET'])
def closeDownloadModal():
    return '<div class="modal-body"><div id="result" class="d-flex justify-content-center text-center"><img id="indicator" class="htmx-indicator" src="/static/spinner.gif" /><br><h5>제작중...</h5></div></div>'

def _imageCollage(frameName: str, selectedImageInfo: dict):
    JSON_PATH = os.path.join(FOLDER_DIR, 'FRAMES', 'FRAMES.json')

    # 0. json 데이터 가져오기
    try:
        with open(JSON_PATH, 'r', encoding='UTF-8') as json_file:
            framesData = json.load(json_file)
    except Exception as e:
        return f'프레임 정보를 여는 중에 오류가 발생했어요.'
    
    # 1. 프레임 가져오기
    try:
        if frameName in framesData['FRAMES']:
            selectedFrameInfo = framesData[framesData['FRAMES'].index(frameName)]
            frameImage = Image.open(os.path.join(FOLDER_DIR, 'FRAMES', selectedFrameInfo['FILE_NAME'])).convert("RGBA")
            if selectedFrameInfo['IS_OVERLAYED']:
                overlayImage = Image.open(os.path.join(FOLDER_DIR, 'FRAMES', selectedFrameInfo['OVERLAY_FILE_NAME'])).convert("RGBA")
            else:
                overlayImage = frameImage
        else:
            ValueError(f'{frameName} 프레임을 찾을 수 없습니다.')
    except ValueError as e:
        return str(e)
    except:
        return '프레임을 여는 중에 오류가 발생했어요.'

    # for frame in framesData['FRAMES']:
    #     if frame['NAME'] == frameName:
    #         frameImage = Image.open(os.path.join(FOLDER_DIR, 'FRAMES', frame['FILE_NAME'])).convert("RGBA")
    #         selectedFrameInfo = frame
    #         if frame['IS_OVERLAYED'] == True:
    #             overlayImage = Image.open(os.path.join(FOLDER_DIR, 'FRAMES', frame['OVERLAY_FILE_NAME'])).convert("RGBA")
    #         else:
    #             overlayImage = frameImage
    #         break

    # 2. 선택한 이미지 불러오기
    images = []
    try:
        for objectImage in selectedImageInfo:
            IMAGE_DIR = os.path.dirname(objectImage['dir'])
            images.append(Image.open(fp=os.path.join(IMAGE_DIR, objectImage['fileName'])).convert("RGBA"))
    except Exception as e:
        return f'합칠 이미지를 가져오는 중에 오류가 발생했어요.'

    try:
        # 3.2.5. 이미지 합성하기
        for idx in range(0, selectedFrameInfo['IMAGE']):
            frameImage.paste(images[idx], (selectedFrameInfo['POSITION'][idx]['POINT_X'], selectedFrameInfo['POSITION'][idx]['POINT_Y']))
        
        # 이미지를 복사하여 overlayImage에 변경 적용
        frameImage.alpha_composite(overlayImage, (0,0))
    except:
        return '이미지를 만드는 중에 오류가 발생했어요.'


    # 3.5. 이미지 저장하기, 근데 중복이면 이름 바꾸기
    try:
        os.mkdir(FOLDER_DIR + '\\COLLAGED')
    except:
        pass
    imagesArray = os.listdir(FOLDER_DIR + '\\COLLAGED')
    frameImage.save(f'{FOLDER_DIR}\\COLLAGED\\{len(imagesArray)}.png')
    return f'{len(imagesArray)}.png'

# GPT
def _imageResize(folderName: str):
    IMAGE_DIR = os.path.join(FOLDER_DIR, folderName)
    RESIZED_DIR = os.path.join(IMAGE_DIR, 'RESIZED')

    # 이미지 디렉토리 확인 및 생성
    if 'RESIZED' not in os.listdir(IMAGE_DIR):
        os.mkdir(RESIZED_DIR)

    if os.listdir(RESIZED_DIR):
        return

    # 이미지 목록 가져오기 및 필터링
    imagesArray = [image for image in os.listdir(IMAGE_DIR) if image.lower().endswith('.jpg')]
    images = [Image.open(os.path.join(IMAGE_DIR, imageName)) for imageName in imagesArray]

    # 이미지 리사이징 및 저장
    for image, imageName in zip(images, imagesArray):
        originalRatio = image.width / image.height
        resizedImage = image.resize((900, int(900 * (1 / originalRatio))))
        resizedImage = resizedImage.crop((0, int((resizedImage.height - 600) / 2), resizedImage.width, int(((resizedImage.height - 600) / 2) + 600)))
        resizedImage.save(os.path.join(RESIZED_DIR, imageName))

# GPT
def _elementWrapper(tag: str, contents: str, option: dict):
    optstr = ' '.join(f'{k}="{v}"' for k, v in option.items())
    return f'<{tag} {optstr}>{contents}</{tag}>'

def _inline_elementWrapper(tag: str, option: dict):
    optstr = ' '.join(f'{k}="{v}"' for k, v in option.items())
    return f'<{tag} {optstr}/>'

if __name__ == '__main__':
    # print(_get_all_files())
    # print(_get_all_images())
    print(_imageCollage('BLACK', '테스트', ['_1311150.jpg', '_1311150.jpg', '_1311150.jpg', '_1311150.jpg']))
    #print(getCollagedImage('{"frame":"black","folderName":"20803","images":["http://127.0.0.1/static/unyang4cut/10101/2.jpg","http://127.0.0.1/static/unyang4cut/10101/2.jpg","http://127.0.0.1/static/unyang4cut/10101/2.jpg","http://127.0.0.1/static/unyang4cut/10101/2.jpg"]}'))
    #_imageResize('테스트')