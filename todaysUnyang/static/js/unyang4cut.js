let availableFrame = [false, false, false, false]
var imageFrameContainer = document.querySelectorAll('.imageFrameContainer')

function pushImage(imageSrc) {
    // framesDiv = document.getElementsByClassName('imageFrame')
    // framesDiv[imageIdx].src = imageSrc
    // framesDiv[imageIdx].classList.remove('disabled');
    // imageIdx += 1
    imageIdx = availableFrame.indexOf(false)

    if (imageIdx < 0 || imageIdx > 3) {
        return
    }

    availableFrame[imageIdx] = true
    var image = imageFrameContainer[imageIdx].querySelector('.imageFrame')
    var p = imageFrameContainer[imageIdx].querySelector('.designator')
    image.src = imageSrc
    image.classList.remove('disabled')
    p.classList.add('disabled')
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