rootUrl = '${window.location.origin}/photo'

var inputName = ''
var inputPassword = ''

async function isNameDuplicated(inputName) {
    console.log('중복 확인중...');

    try {
        const queryParams = {
            'NAME': inputName,
            'TYPE': 'IS_DUPLICATED'
        };

        const isDuplicatedQuery = await httpRequest('/photo/registration', 'POST', {}, queryParams);
        const isDuplicateObject = JSON.parse(isDuplicatedQuery);

        return isDuplicateObject['IS_DUPLICATED'];
    } catch (error) {
        console.error('중복 확인 중 문제가 발생했어요.', error);
        throw new Error('중복 확인 중 문제가 발생했어요.');
    }
}

// 폼이 제출될 때 실행될 함수
async function onSubmitForm() {
    try {
        var NoticeModalCloseBtn = document.getElementById('notice-modal-close')
        if (NoticeModalCloseBtn) {
            NoticeModalCloseBtn.click()
        }

        // 여기에 원하는 동작을 추가
        inputName = document.getElementById('inputName').value;
        inputPassword = document.getElementById('inputPassword').value;

        if (inputName.length <= 0) {
            alert('이름을 입력해주세요.');
            return
        }

        if (inputPassword.length <= 0) {
            alert('비밀번호를 입력해주세요.')
            return
        }

        // isNameDuplicated 함수가 비동기로 동작하므로 await 사용
        if (await isNameDuplicated(inputName)) {
            alert('이미 사용된 이름이에요.\n다른 이름을 사용해주세요.');
            return;
        }

        const queryParams = {
            'NAME': inputName,
            'PASSWORD': inputPassword,
            'TYPE': 'START'
        };

        const endBtnQuery = await httpRequest('/photo/registration', 'POST', {}, queryParams);
        const endBtnElement = JSON.parse(endBtnQuery);
        const targetElement = document.getElementById('registration');
        replaceContent(endBtnElement['NEW_CONTENT'], targetElement);

        const userNameElement = document.getElementById('userName')
        userNameElement.textContent = '이름: ' + inputName
    } catch (error) {
        console.error('' + error + '\n일시적인 네트워크 문제이거나, 서버의 문제일 수 있어요.', error);
        alert('' + error + '\n일시적인 네트워크 문제이거나, 서버의 문제일 수 있어요.\n반복될 경우 관리자에게 문의해주세요.');
    }
}

// async function start() {
//     try {
//         name = document.getElementById('name').value
//         password = document.getElementById('password').value

//         if (isNameDuplicated(name)) {
//             alert('이미 사용된 이름이에요.\n다른 이름을 사용해 주세요.');
//             return
//         }

//         // 종료 버튼 가져오기
//         queryParams = {
//             'NAME': name,
//             'PASSWORD': password,
//             'TYPE': 'START'
//         }

//         // 종료 버튼 요청
//         const endBtnData = await httpRequest('/photo/registration', 'POST', {}, queryParams);

//         // Handle the response data for start
//         console.log('시작 버튼 쿼리:', endBtnData);
//         const endBtnObject = JSON.parse(endBtnData);

//         const targetElement = document.getElementById('infoForm');
//         replaceContent(endBtnObject['NEW_CONTENT'], targetElement);
//     } catch (error) {
//         // Handle errors
//         console.error('Error while starting:', error);
//     }
// }

async function stop() {
    try {
        queryParams = {
            'NAME': inputName,
            'PASSWORD': inputPassword,
            'TYPE': 'END'
        }

        const endedBtnData = await httpRequest('/photo/registration', 'POST', {}, queryParams);
        const endedBtnObject = JSON.parse(endedBtnData);

        const targetElement = document.getElementById('terminate')
        replaceContent(endedBtnObject['NEW_CONTENT'], targetElement)

        const nameElement = document.getElementById('name')
        const startTimeElement = document.getElementById('startTime')
        const endTimeElement = document.getElementById('endTime')
        nameElement.textContent = '이름 혹은 학번: ' + endedBtnObject['NAME']
        startTimeElement.textContent = '시작 시각: ' + endedBtnObject['START_TIME'].split('.')[0]
        endTimeElement.textContent = '종료 시각: ' + endedBtnObject['END_TIME'].split('.')[0]

    } catch (error) {
        console.error('Error while ending: ', error)
    }
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