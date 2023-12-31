let isContainImage = [false, false, false, false]
let filledImageInfo = [{}, {}, {}, {}]
let frame = 'WHITE'
let folderName = ''
var imageFrameContainer = document.querySelectorAll('.imageFrameContainer')
let isFrameSelected = false

window.onload = function() {
    sizeReload();
};

window.onresize = function() {
    sizeReload();
};

function sizeReload() {
    var leftDiv = document.getElementById('imagePeeker');
    var rightDiv = document.getElementById('framePeeker');

    // 프레임 프리뷰 div의 높이 가져오기
    var rightDivHeight = rightDiv.clientHeight;

    // 이미지 피커 div에 높이 적용
    leftDiv.style.height = rightDivHeight + 'px';    

    var framePeekerWidth = document.getElementById('selectedImageViewer').clientWidth;
    var calculatedMargin = framePeekerWidth * (50 / 1000);
    var calculatedWidth = framePeekerWidth * (900 / 1000);
    var calculatedHeight = calculatedWidth * (2 / 3)
    var imageContainerList = document.querySelectorAll('.imageFrameContainer');

    count = 1
    imgCount = 0
    for (const imageContainer of imageContainerList) {
        imageContainer.style.position = 'absolute';
        // 픽셀 값을 명시적으로 지정하고, 단위를 'px'로 사용합니다.
        var newWidth = framePeekerWidth - (2 * calculatedMargin) + 'px';
        imageContainer.style.width = newWidth;
        imageContainer.style.left = calculatedMargin + 'px';
        imageContainer.style.top = calculatedMargin * count + (calculatedHeight * imgCount) + 'px';
        count++
        imgCount++
    }
};

function startUp() {
    // 프레임이 선택되면 클릭을 허용하는 함수
    console.log('프레임 선택됨.')
    userImages = document.querySelectorAll('.takenImages')
    if (userImages) {
        for (const image of userImages) {
            image.classList.remove('click_block')
        }
        isFrameSelected = true
    }
}

async function getFolderList() {
    const folderListElement = await httpRequest('/photo/folders', 'GET', '', {})
    var imagePeekerElement = document.getElementById('box')
    replaceContent(folderListElement, imagePeekerElement)
}

function showFrameInfo(status) {
    if (!isFrameSelected) {
        var frameInfoElement = document.getElementById('frameInfo')

        if (status) {
            frameInfoElement.classList.remove('visually-hidden')
        } else {
            frameInfoElement.classList.add('visually-hidden')
        }
    }
}

async function openFolder(reqFolderName) {

    password = prompt("'" + reqFolderName + "' 폴더 비밀번호를 입력해주세요.", undefined)
    if (password == '' || password == undefined) {
        return
    }

    queryParams = {
        'NAME': reqFolderName,
        'PASSWORD': password
    }
    
    const isPasswordCorrect = await httpRequest('/photo/password', 'POST', {}, queryParams);

    isPasswordCorrectObject = JSON.parse(isPasswordCorrect)
    console.log("폴더 '" + reqFolderName + "'에 대해 인증되었습니다.")

    if (isPasswordCorrectObject['IS_TRIUMPH']) {
        if (isPasswordCorrectObject['IS_PASSWORD_CORRECT']) {
            // 성공
            folderName = reqFolderName
            queryParams = {
                'file_name': reqFolderName
            }
            
            const imagesElement = await httpRequest('/photo/images', 'GET', {}, queryParams)

            boxElement = document.getElementById('box')
            replaceContent(imagesElement, boxElement)

            // imagePeeker 상단 버튼이 항상 위에 고정되기 위해...
            var takenImagePeekerElement = document.getElementById('takenImagePeeker')
            var imagePeekerElement = document.getElementById('imagePeeker')
            var controlBtnElement = document.getElementById('controlBtn')
            takenImagePeekerElement.style.height = (imagePeekerElement.clientHeight - controlBtnElement.clientHeight) + 'px';
        
            showFrameInfo(true)
        }
        else {
            // 비밀번호 틀림
            alert('비밀번호가 틀립니다.')
            return
        }
    } else {
        // DB 에러
        alert('DB 에러입니다.')
    }
}

function pushImage(pushedImageSrc, pushedImageName) {
    // 프레임 위의 이미지가 꽉 찼는지 확인
    imageIdx = isContainImage.indexOf(false)
    if (imageIdx < 0 || imageIdx > 3) {
        return
    }

    if (!isFrameSelected) {
        return
    }

    isContainImage[imageIdx] = true

    var image = imageFrameContainer[imageIdx].querySelector('.imageFrame')
    image.src = pushedImageSrc

    filledImageInfo[imageIdx] = { url: image.src, fileName: pushedImageName }

    image.classList.remove('hide')

    createBtnAllower()
}

function createBtnAllower() {
    if (!isFrameSelected) {
        return
    }

    var btnElement = document.getElementById('generate')

    for (var bool of isContainImage) {
        if (!bool) {
            btnElement.classList.add('disabled')
            return
        }
    }
    btnElement.classList.remove('disabled')
}

function popImage(alt) {
    for (var idx = 0; idx < 4; idx++) {
        var image = imageFrameContainer[idx].querySelector('.imageFrame')
        if (image.alt == alt) {
            image.classList.add('hide')
            image.src = '#'
            isContainImage[idx] = false
            break
        }
    }
    createBtnAllower()
}

async function create() {
    collage = {
        'frame': frame,
        'folderName': folderName,
        'images': filledImageInfo
    }

    var collagedImageElement = await httpRequest('/photo/collage', 'POST', {}, collage)

    var indicatorElement = document.getElementById('collageLoading')

    indicatorElement.innerHTML = collagedImageElement
}

async function download() {
    var resultImageElement = document.getElementById('collagedImage')
    var resultSrc = resultImageElement.src
    var resultFileName = resultImageElement.alt
    downloadFile(resultSrc, resultFileName)
}

async function setFrame(selectedFrameName) {

    showFrameInfo(false)

    const FRAMES_BASE_PATH = '/static/unyang4cut/FRAMES/'

    const FRAME_JSON_QUERY = await httpRequest(FRAMES_BASE_PATH + 'FRAMES.json', 'GET', {}, {})
    const FRAME_JSON = JSON.parse(FRAME_JSON_QUERY)
    var frame_info = ''
    for (const FRAME of FRAME_JSON['FRAMES']) {
        if (FRAME['NAME'] == selectedFrameName) {
            frame_info = FRAME
        }
    }

    frame = selectedFrameName

    frameImageElement = document.getElementById('backgroundFrameImage')
    frameImageElement.src = FRAMES_BASE_PATH + frame_info['FILE_NAME']
    frameImageElement.alt = selectedFrameName

    overlayImageElement = document.getElementById('overlayFrameImage')

    if (frame_info['IS_OVERLAYED']) {
        overlayImageElement.src = FRAMES_BASE_PATH + frame_info['OVERLAY_FILE_NAME']
    } else {
        overlayImageElement.src = FRAMES_BASE_PATH + frame_info['FILE_NAME']
    }

    frameModalCloseBtn = document.getElementById('frameModalClose').click()

    console.log('현재 프레임: ' + frame)

    if (!isFrameSelected) {
        startUp()
    }
}

function downloadFile(url, fileName) {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.responseType = 'blob';

        xhr.onload = function () {
            if (xhr.status === 200) {
                const blob = new Blob([xhr.response], { type: 'application/octet-stream' });
                const link = document.createElement('a');
                link.href = window.URL.createObjectURL(blob);
                link.download = fileName;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                resolve();
            } else {
                reject(new Error(`Failed to download file: ${xhr.status}`));
            }
        };

        xhr.onerror = function () {
            reject(new Error('Network error occurred'));
        };

        xhr.send();
    });
}

// 여러 파일을 동시에 다운로드하는 함수
function downloadAllFiles() {
    var files = [];
    var takenImages = document.getElementsByClassName('img-fluid rounded mb-4 mb-lg-0 takenImages');

    for (const takenImage of takenImages) {
        files.push({ url: takenImage.src.replace('/RESIZED', ''), fileName: takenImage.alt });
    }

    var collagedImage = document.getElementById('collagedImage')
    files.push({ url: collagedImage.src, fileName: collagedImage.alt })

    // Promise 배열을 생성하여 각 다운로드 작업을 시작
    const downloadPromises = files.map(file => downloadFile(file.url, file.fileName));

    // 모든 다운로드 작업이 완료될 때까지 대기
    Promise.all(downloadPromises)
        .then(() => {
            console.log('All files downloaded successfully');
        })
        .catch(error => {
            console.error(`Error downloading files: ${error.message}`);
        });
}

function httpRequest(url, method, header, params) {
    let options = {
        method: method,
        headers: header || {},  // Ensure headers is defined
    };

    // Append query parameters for GET requests
    if (method.toUpperCase() === 'GET' && params) {
        const queryString = Object.keys(params)
            .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
            .join('&');
        url += `?${queryString}`;
    } else if (params) {
        // For other methods (e.g., POST), include params in the request body
        options = {
            method: method,
            body: JSON.stringify(params),
            headers: {
                'Content-Type': 'application/json'
            }
        }
    }

    return new Promise((resolve, reject) => {
        fetch(url, options)
            .then(response => {
                if (!response.ok) {
                    reject(new Error(`HTTP error! Status: ${response.status}`));
                }
                return response.text();  // or response.json() if the response is JSON
            })
            .then(data => {
                resolve(data);
            })
            .catch(error => {
                reject(error);
            });
    });
}


function replaceContent(newContent, container) {
    // Simulate an asynchronous operation
        // // New content to replace the existing content
        // const newContent = '<p>This is the new content after replacement.</p>';

        // // Find the container element
        // const container = document.getElementById('container');

        // Replace the content of the container with the new content
    container.innerHTML = newContent;
     // Simulating a delay of 1 second (you can remove this in a real scenario)
}