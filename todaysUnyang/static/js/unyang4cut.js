let isFrameFilled = [false, false, false, false]
let filledImageInfo = [{}, {}, {}, {}]
let frame = 'WHITE'
let folderName = ''
var imageFrameContainer = document.querySelectorAll('.imageFrameContainer')
let isFrameSelected = false

function startUp() {
    takenImageArray = document.querySelectorAll('.takenImages')
    if (takenImageArray) {
        for (const takenImage of takenImageArray) {
            takenImage.classList.remove('hide')
        }
        isFrameSelected = true
    }
}

function setFolderName(currentFolderName) {
    if (folderName == '') {
        folderName = currentFolderName
    }
}

function pushImage(pushedImageSrc, pushedImageName) {
    // 프레임 위의 이미지가 꽉 찼는지 확인
    imageIdx = isFrameFilled.indexOf(false)
    if (imageIdx < 0 || imageIdx > 3) {
        return
    }

    if (!isFrameSelected) {
        return
    }

    isFrameFilled[imageIdx] = true

    var image = imageFrameContainer[imageIdx].querySelector('.imageFrame')
    image.src = pushedImageSrc

    filledImageInfo[imageIdx] = { url: image.src, fileName: pushedImageName }

    var p = imageFrameContainer[imageIdx].querySelector('.designator')
    image.classList.remove('disabled')
    p.classList.add('disabled')

    let collage = {
        'frame': frame,
        'folderName': folderName,
        'images': filledImageInfo
    }
    var imageCollage = document.getElementById('imageCollage')
    imageCollage.value = JSON.stringify(collage)
}

function popImage(alt) {
    for (var idx = 0; idx < 4; idx++) {
        var image = imageFrameContainer[idx].querySelector('.imageFrame')
        var p = imageFrameContainer[idx].querySelector('.designator')
        if (image.alt == alt) {
            image.classList.add('disabled')
            image.src = '#'
            p.classList.remove('disabled')
            isFrameFilled[idx] = false
            break
        }
    }
}

function download() {
    var collagedImage = document.getElementById('collagedImage')
    collagepushedImageSrc = collagedImage.src
    var downloadBtn = document.getElementById('downloadBtn')
    downloadBtn.href = collagedImage.src
}

function setFrame(selectedFrameSrc, selectedFrameName, overlayFrameSrc) {
    console.log(selectedFrameSrc)
    console.log(selectedFrameName)
    console.log(overlayFrameSrc)

    frame = selectedFrameName
    frameImageElement = document.getElementById('backgroundFrameImage')
    frameImageElement.src = selectedFrameSrc
    frameImageElement.alt = selectedFrameName
    overlayImageElement = document.getElementById('overlayFrameImage')
    overlayImageElement.src = overlayFrameSrc
    frameModalCloseBtn = document.getElementById('frameModalClose').click()

    startUp()
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