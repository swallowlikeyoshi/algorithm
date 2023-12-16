let availableFrame = [false, false, false, false]
let frame = 'black'
let folderName = ''
let imageNames = [{}, {}, {}, {}]
var imageFrameContainer = document.querySelectorAll('.imageFrameContainer')

function pushImage(imageSrc, imageAlt) {
    // framesDiv = document.getElementsByClassName('imageFrame')
    // framesDiv[imageIdx].src = imageSrc
    // framesDiv[imageIdx].classList.remove('disabled');
    // imageIdx += 1
    if (folderName == '') {
        folderName = document.getElementById('indicator').textContent
    }

    imageIdx = availableFrame.indexOf(false)
    if (imageIdx < 0 || imageIdx > 3) {
        return
    }
    availableFrame[imageIdx] = true
    var image = imageFrameContainer[imageIdx].querySelector('.imageFrame')

    image.src = imageSrc
    imageNames[imageIdx] = { url: image.src, fileName: imageAlt }

    var p = imageFrameContainer[imageIdx].querySelector('.designator')
    image.classList.remove('disabled')
    p.classList.add('disabled')

    let collage = {
        'frame': frame,
        'folderName': folderName,
        'images': imageNames
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
            availableFrame[idx] = false
            break
        }
    }
}

function download() {
    var collagedImage = document.getElementById('collagedImage')
    collageImageSrc = collagedImage.src
    var downloadBtn = document.getElementById('downloadBtn')
    downloadBtn.href = collagedImage.src
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
        files.push({ url: takenImage.src, fileName: takenImage.alt });
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