let availableFrame = [false, false, false, false]
let frame = 'black'
let folderName = ''
let imageNames = ['', '', '', '']
var imageFrameContainer = document.querySelectorAll('.imageFrameContainer')

function pushImage(imageSrc) {
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
    var p = imageFrameContainer[imageIdx].querySelector('.designator')
    image.src = imageSrc
    imageNames[imageIdx] = imageSrc
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