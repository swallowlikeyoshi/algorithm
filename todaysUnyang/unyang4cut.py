import os
import json
import sqlite3
from datetime import datetime
from urllib.parse import unquote

from flask import session, render_template, request, Blueprint
from PIL import Image

from todaysUnyang import BASE_DIR, exif, IS_DEBUGING

unyang4cut = Blueprint("photo", __name__, url_prefix="/photo")
FOLDER_DIR = os.path.join(BASE_DIR, "static", "unyang4cut")
DB_PATH = os.path.join(FOLDER_DIR, "unyang4cut_log.db")

try:
    f = open(DB_PATH, "r")
except:
    f = open(DB_PATH, "w")
    connection = sqlite3.connect(DB_PATH)
    cur = connection.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS unyang4cutLogs (name text, password text, time DATETIME, status text)"
    )
    connection.commit()
    cur.close()
    connection.close()
finally:
    f.close()


@unyang4cut.route("/", methods=["GET"])
def photo():
    return render_template("unyang4cut.html")


@unyang4cut.route("/download", methods=["GET"])
def download():
    return render_template("unyang4cut_download.html")


@unyang4cut.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        queryParams = request.json

        session["NAME"] = queryParams["NAME"]

        if queryParams["TYPE"] == "START":
            session["PASSWORD"] = queryParams["PASSWORD"]
            session["START_TIME"] = str(datetime.now())
            _shootingLog(
                session["NAME"], session["PASSWORD"], session["START_TIME"], "START"
            )
            try:
                os.mkdir(os.path.join(FOLDER_DIR, session["NAME"]))
            except:
                pass

            # 취소 버튼 엘리먼트를 반환
            # cancelBtnElement = '<div id="terminate" class="p-2 d-flex flex-column justify-content-around text-center"><h3>사진 촬영을 끝마친 후 버튼을 눌러주세요.</h3><button class="btn btn-danger" onclick="stop()">그만 찍기</button></div>'
            endedBtnElement = '<div class="card text-center mb-3 p-2" style="width: 100%;"><div class="card-body"><h5 class="card-title">등록되었습니다.</h5><h6 class="card-subtitle mb-2 text-body-secondary">사진을 찍고 이 화면을 보여주세요.</h6><p class="card-text" id="userName"></p><a href="/photo" class="btn btn-primary">꾸미러 가기</a></div></div>'
            returnElement = {"NEW_CONTENT": endedBtnElement}
            return json.dumps(returnElement)

        elif queryParams["TYPE"] == "END":
            session["PASSWORD"] = queryParams["PASSWORD"]
            session["END_TIME"] = str(datetime.now())
            _shootingLog(
                session["NAME"], session["PASSWORD"], session["END_TIME"], "END"
            )
            endedBtnElement = '<div class="card text-center mb-3" style="width: 18rem;"><div class="card-body"><h5 class="card-title">등록되었습니다.</h5><h6 class="card-subtitle mb-2 text-body-secondary">사진을 찍고 이 화면을 보여주세요.</h6><p class="card-text" id="userName"></p><a href="/photo" class="btn btn-primary">꾸미러 가기</a></div></div>'
            returnElement = {
                "NAME": session["NAME"],
                "START_TIME": session["START_TIME"],
                "END_TIME": session["END_TIME"],
                "NEW_CONTENT": endedBtnElement,
            }
            return json.dumps(returnElement)

        elif queryParams["TYPE"] == "IS_DUPLICATED":
            nameList = os.listdir(FOLDER_DIR)
            if session["NAME"] in nameList:
                return json.dumps({"IS_DUPLICATED": True})
            else:
                return json.dumps({"IS_DUPLICATED": False})
    else:
        return render_template("unyang4cut_registration.html")


@unyang4cut.route("/password", methods=["POST"])
def isPasswordCorrect():
    if not request.method == "POST":
        return
    else:
        postParmas = request.json

    try:
        # 디버깅 아닐 시 제거하기!!!
        if postParmas["NAME"] == "1234":
            if IS_DEBUGING: 
                session['CERTIFICATED_FOLDER_NAME'] = []
                session['CERTIFICATED_FOLDER_NAME'].append(postParmas['NAME'])
                return json.dumps({"IS_TRIUMPH": True, "IS_PASSWORD_CORRECT": True})

        queriedUserPassword = _DB_excute(
            "SELECT DISTINCT password FROM unyang4cutLogs WHERE name = ? ORDER BY time DESC LIMIT 1",
            (postParmas["NAME"],),
        )
        session['CERTIFICATED_FOLDER_NAME'] = []

        if str(queriedUserPassword[0][0]) == str(postParmas["PASSWORD"]):
            session['CERTIFICATED_FOLDER_NAME'].append(postParmas['NAME'])
            return json.dumps({"IS_TRIUMPH": True, "IS_PASSWORD_CORRECT": True})
        else:
            raise ("비밀번호가 틀립니다.")

    except sqlite3.OperationalError as op:
        return json.dumps({"IS_TRIUMPH": False, "CONTENT": str(op)})
    except Exception as e:
        return json.dumps({"IS_TRIUMPH": True, "IS_PASSWORD_CORRECT": False})


@unyang4cut.route("/folders", methods=["GET"])
def getAllFiles():
    try:
        # 1. unyang4cut 폴더 내 모든 폴더 이름 가져오기
        foldersArray = [
            folder
            for folder in os.listdir(FOLDER_DIR)
            if os.path.isdir(os.path.join(FOLDER_DIR, folder))
        ]

        folderBlackList = ["FRAMES", "COLLAGED", "RESIZED"]
        foldersArray = [
            folder
            for folder in foldersArray
            if all(blackFolder not in folder for blackFolder in folderBlackList)
        ]

        # 2. HTML화 하기
        if len(foldersArray) <= 0:
            option = {"class": "emptyFolder btn btn-light"}
            ValueError(_elementWrapper("p", "폴더가 없어요.<br>나중에 다시 시도해 주세요.", option))
        else:
            elements = ""
            for folderName in foldersArray:
                option = {
                    "class": "folderName btn btn-light",
                    # 이후 동작을 위해선 htmx보단 자바스크립트에서 처리하는게 나을 듯
                    # 'hx-get': f'/photo/images?file_name={urllib.parse.quote(folderName)}',
                    # 'hx-target': '#box',
                    # 'onclick': f'setFolderName({folderName})'
                    "onclick": f"openFolder('{folderName}')",
                }
                element = _elementWrapper("p", folderName, option)
                elements += element
    except ValueError as e:
        return str(e)
    except Exception:
        return "파일 불러오기 오류."

    # 3. 전송하기
    elements = _elementWrapper(
        "div", elements, {'id': 'imageList', "class": "d-flex flex-column justify-content-top overflow-scroll scrollRemove"}
    )
    return elements


@unyang4cut.route("/images", methods=["GET"])
def getAllImages():
    reqName = request.args.get("file_name")

    # GPT
    try:
        if reqName not in session['CERTIFICATED_FOLDER_NAME']:
            raise ValueError(f"폴더 '{reqName}'에 대해 인증되어있지 않습니다.")
        # 1. 같은 이름을 가진 폴더 찾기
        if reqName not in os.listdir(FOLDER_DIR):
            raise ValueError(f"폴더 '{reqName}'을 찾을 수 없습니다.")
        folderName = reqName

        # 1.5 이미지 리사이징 하기
        _imageResize(folderName)

        # 2. 폴더 안의 모든 이미지의 이름 가져오기
        IMAGE_DIR = os.path.join(FOLDER_DIR, folderName, "RESIZED")
        filesArray = os.listdir(IMAGE_DIR)
        filesArray = [fileName for fileName in os.listdir(IMAGE_DIR)]
        imagesArray = []
        for fileName in filesArray:
            if ".jpg" or ".JPG" in fileName:
                imagesArray.append(fileName)

    except ValueError as ve:
        return f"이미지 불러오기 오류: {str(ve)}"
    except Exception as e:
        return f"이미지 불러오기 오류."

    # 3. 가져온 이미지를 HTML화 하기
    elements = ""
    for imageName in imagesArray:
        HTML_dir = f"/static/unyang4cut/{folderName}/RESIZED/{imageName}"
        # 가져온 이미지들을 요소화 하기
        option = {
            "class": "takenImages img-fluid rounded mb-4 mb-lg-0 p-1",
            "src": HTML_dir,
            "alt": imageName,
            "onclick": "pushImage(this.src, this.alt)",
        }
        element = _inline_elementWrapper("img", option)
        elements = elements + element

    # 현재 폴더 표시용 버튼
    option = {"type": "button disabled", "class": "btn btn-primary", "id": "indicator"}
    indicator = _elementWrapper("button", folderName, option)

    # 뒤로가기 버튼
    option = {
        "type": "button",
        "class": "btn btn-secondary",
        # "hx-get": "/photo/folders",
        # "hx-target": "#box",
        "onclick": "getFolderList()",
    }
    btn = _elementWrapper("button", "뒤로 가기", option)

    backButton = _elementWrapper(
        "div",
        indicator + btn,
        {"class": "d-flex p-2 justify-content-around", "id": "controlBtn"},
    )
    elements = backButton + _elementWrapper(
        "div",
        elements,
        {"class": "overflow-auto", "id": "takenImagePeeker"},
    )

    # 4. 전송하기
    return elements


@unyang4cut.route("/frames", methods=["GET"])
def getAllFrames():
    FRAME_DIR = os.path.join(FOLDER_DIR, "FRAMES")
    HTML_DIR = f"/static/unyang4cut/FRAMES"

    # 1. 프레임 JSON 파일 가져오기
    try:
        with open(
            os.path.join(FRAME_DIR, "FRAMES.json"), "r", encoding="UTF-8"
        ) as json_file:
            framesData = json.load(json_file)
    except Exception as e:
        return f"프레임 정보를 가져오는 중에 오류가 발생했어요."

    # 2. 각 프레임 html화 하기
    frameElements = []
    for frame in framesData["FRAMES"]:
        if frame["IS_OVERLAYED"]:
            overlayFileName = frame["OVERLAY_FILE_NAME"]
        else:
            overlayFileName = "clear.png"
        # 1. img 태그 이용해서 프레임 이미지 띄우는 요소
        option = {
            "class": "frameImage p-2 click_block",
            "onclick": "setFrame(this.src, this.alt, this.getAttribute('overlay'))",
            "src": f'{HTML_DIR}/{frame["FILE_NAME"]}',
            "alt": f'{frame["NAME"]}',
            "overlay": f"{HTML_DIR}/{overlayFileName}",
        }
        imageElement = _inline_elementWrapper("img", option)

        # 2. 이미지 아래 프레임 이름 띄우는 요소
        option = {
            "class": "frameName p-2 click_block",
            "onclick": "setFrame(this.src, this.alt, this.getAttribute('overlay'))",
            "src": f'{HTML_DIR}/{frame["FILE_NAME"]}',
            "alt": f'{frame["NAME"]}',
            "overlay": f"{HTML_DIR}/{overlayFileName}",
        }
        nameElement = _elementWrapper("p", frame["DISPLAY_NAME"], option)

        # 두 개를 하나로 묶기
        option = {
            "class": "card p-2",
            "style": "width: 45%; margin-right: 10px; min-width: 100px;",
            "onclick": "setFrame(this.getAttribute('alt'))",
            "alt": f'{frame["NAME"]}'
        }
        element = _elementWrapper("div", imageElement + nameElement, option)
        frameElements.append(element)

    finalElement = ""
    for frame in frameElements:
        finalElement = finalElement + frame
    finalElement = _elementWrapper(
        "div", finalElement, {"class": "d-flex flex-row overflow-auto"}
    )
    return finalElement


@unyang4cut.route("/collage", methods=["GET", "POST"])
def getCollagedImage():
    if request.method == 'GET':
        getJson = request.args.get("json")
        collage = json.loads(getJson)
    elif request.method == 'POST':
        queryParams = request.json
        collage = queryParams

    # 1. HTML 경로에서 PATH로 바꾸기
    selectedImageInfo = []
    for image in collage["images"]:
        decoded_path = unquote(image["url"].split("/static/unyang4cut/")[-1]).replace(
            "%20", " "
        )
        windows_path = os.path.join(*decoded_path.split("/"))
        selectedImageInfo.append(
            {
                "dir": FOLDER_DIR + "\\" + windows_path,
                "fileName": image["fileName"].replace("%20", " "),
            }
        )

    # 2. PATH를 이용해서 이미지 합치기
    collagedImageName = _imageCollage(collage["frame"], selectedImageInfo)

    HTML_dir = f"/static/unyang4cut/COLLAGED/{collagedImageName}"
    option = {
        "class": "img-fluid rounded mb-4 mb-lg-0",
        "id": "collagedImage",
        "src": HTML_dir,
        "alt": collagedImageName,
    }
    collagedImageElement = _inline_elementWrapper("img", option)

    modal_body = _elementWrapper(
        "div",
        collagedImageElement,
        {
            "id": "result",
            "class": "d-flex justify-content-center text-center p-2",
            "style": "background-color: grey;",
        },
    )
    modal_footer = '<button type="button" class="btn btn-secondary" data-bs-dismiss="modal" hx-get="/photo/closeDownloadModal" hx-target="#collageLoading">닫기</button><button type="button" class="btn btn-primary" onclick="download()">네컷만 저장하기</button><button type="button" class="btn btn-success" onclick="downloadAllFiles()">네컷과 이미지 모두 저장하기</button>'
    modal_footer = _elementWrapper("div", modal_footer, { "class": "modal-footer" })
    return modal_body + modal_footer


@unyang4cut.route("/closeDownloadModal", methods=["GET"])
def closeDownloadModal():
    indicator = (
        _inline_elementWrapper(
            "img",
            {
                "id": "indicator",
                "class": "htmx-indicator",
                "src": "/static/spinner.gif",
            },
        )
        + "<br><h5>제작중...</h5>"
    )
    result = _elementWrapper(
        "div",
        indicator,
        {"id": "result", "class": "d-flex justify-content-center text-center"},
    )
    modal_body = _elementWrapper("div", result, {"class": "modal-body"})
    return modal_body


def _imageCollage(frameName: str, selectedImageInfo: dict):
    JSON_PATH = os.path.join(FOLDER_DIR, "FRAMES", "FRAMES.json")

    # 0. json 데이터 가져오기
    try:
        with open(JSON_PATH, "r", encoding="UTF-8") as json_file:
            framesData = json.load(json_file)
    except Exception as e:
        return f"프레임 정보를 여는 중에 오류가 발생했어요."

    # 1. 프레임 가져오기
    try:
        for frame in framesData["FRAMES"]:
            if frame["NAME"] == frameName:
                frameImage = Image.open(
                    os.path.join(FOLDER_DIR, "FRAMES", frame["FILE_NAME"])
                ).convert("RGBA")
                selectedFrameInfo = frame
                if frame["IS_OVERLAYED"] == True:
                    overlayImage = Image.open(
                        os.path.join(FOLDER_DIR, "FRAMES", frame["OVERLAY_FILE_NAME"])
                    ).convert("RGBA")
                else:
                    overlayImage = Image.open(
                        os.path.join(FOLDER_DIR, "FRAMES", frame["FILE_NAME"])
                    ).convert("RGBA")
                break
        else:
            ValueError(f"{frameName} 프레임을 찾을 수 없습니다.")
    except ValueError as e:
        return str(e)
    except:
        return "프레임을 여는 중에 오류가 발생했어요."

    # 2. 선택한 이미지 불러오기
    images = []
    try:
        for objectImage in selectedImageInfo:
            IMAGE_DIR = os.path.dirname(objectImage["dir"])
            images.append(
                Image.open(fp=os.path.join(IMAGE_DIR, objectImage["fileName"])).convert(
                    "RGBA"
                )
            )
    except Exception as e:
        return f"합칠 이미지를 가져오는 중에 오류가 발생했어요."

    try:
        # 3.2.5. 이미지 합성하기
        for idx in range(0, selectedFrameInfo["IMAGE"]):
            frameImage.paste(
                images[idx],
                (
                    selectedFrameInfo["POSITION"][idx]["POINT_X"],
                    selectedFrameInfo["POSITION"][idx]["POINT_Y"],
                ),
            )

        # 이미지를 복사하여 overlayImage에 변경 적용
        frameImage.alpha_composite(overlayImage, (0, 0))
    except Exception as e:
        return f"이미지를 만드는 중에 오류가 발생했어요. {e}"

    # 3.5. 이미지 저장하기, 근데 중복이면 이름 바꾸기
    try:
        os.mkdir(FOLDER_DIR + "\\COLLAGED")
    except:
        pass
    imagesArray = os.listdir(FOLDER_DIR + "\\COLLAGED")
    numOfImage = len(imagesArray) + 1
    # alpha. EXIF 추가하기
        # frameImage.save(f"{FOLDER_DIR}\\COLLAGED\\{len(imagesArray)}.png", exif=exif_data)
    exif.add_exif_and_save(frameImage, f"{FOLDER_DIR}\\COLLAGED\\{numOfImage}.jpg")

    return f"{numOfImage}.jpg"

def _imageResize(folderName: str):
    IMAGE_DIR = os.path.join(FOLDER_DIR, folderName)
    RESIZED_DIR = os.path.join(IMAGE_DIR, "RESIZED")

    # 이미지 디렉토리 확인 및 생성
    if "RESIZED" not in os.listdir(IMAGE_DIR):
        os.mkdir(RESIZED_DIR)

    if os.listdir(RESIZED_DIR):
        return

    # 이미지 목록 가져오기 및 필터링
    imagesArray = [
        image for image in os.listdir(IMAGE_DIR) if image.lower().endswith(".jpg")
    ]
    images = [
        Image.open(os.path.join(IMAGE_DIR, imageName)) for imageName in imagesArray
    ]

    # 이미지 리사이징 및 저장
    for image, imageName in zip(images, imagesArray):
        originalRatio = image.width / image.height
        resizedImage = image.resize((900, int(900 * (1 / originalRatio))))
        resizedImage = resizedImage.crop(
            (
                0,
                int((resizedImage.height - 600) / 2),
                resizedImage.width,
                int(((resizedImage.height - 600) / 2) + 600),
            )
        )
        resizedImage.save(os.path.join(RESIZED_DIR, imageName))

def _elementWrapper(tag: str, contents: str, option: dict):
    optstr = " ".join(f'{k}="{v}"' for k, v in option.items())
    return f"<{tag} {optstr}>{contents}</{tag}>"

def _inline_elementWrapper(tag: str, option: dict):
    optstr = " ".join(f'{k}="{v}"' for k, v in option.items())
    return f"<{tag} {optstr}/>"

def _shootingLog(name: str, password: str, time: datetime, status: str):
    _DB_excute(
        "INSERT INTO unyang4cutLogs (name, password, time, status) VALUES (?, ?, ?, ?)",
        [name, password, time, status],
    )
    return

def _DB_excute(cmd: str, params):
    DB = sqlite3.connect(DB_PATH)
    CURSOR = DB.cursor()
    CURSOR.execute(cmd, params)
    query = CURSOR.fetchall()
    DB.commit()
    DB.close()
    return query

if __name__ == "__main__":
    # print(_get_all_files())
    # print(_get_all_images())
    print(getCollagedImage())
    # _imageResize('테스트')