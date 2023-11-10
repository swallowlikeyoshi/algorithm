import requests
import json

#외부에서 사용하려면 함수 형식으로 작성해야함!
def get_time_table(grade1, clroom1, semester1, date1):

    schul_dept_code = 'J10'
    schul_code = '7531103'
    grade = grade1
    clroom = clroom1
    semester = semester1
    date = date1

    url = 'https://open.neis.go.kr/hub/hisTimetable'
    parameters = {
        'KEY': '70b4e18a4ad74cf8b5a745846a43fb17',
        'Type': 'json',
        'ATPT_OFCDC_SC_CODE': schul_dept_code,
        'SD_SCHUL_CODE': schul_code,
        'GRADE': grade,
        'SEM': semester,
        'CLASS_NM': clroom,
        'TI_FROM_YMD': date,
        'TI_TO_YMD': date
    }

    # API 요청 보내기
    response = requests.get(url, params=parameters)

    # API 응답 데이터 확인
    data = response.json()

    try:
        if "hisTimetable" in data:
            itrt_contents = [row["ITRT_CNTNT"] for row in data["hisTimetable"][1]["row"]]

            #while 문 대신 함수를 사용했으므로 return으로 종료하면 됨
            #break
            itrt_contents = str(itrt_contents)
            itrt_contents = itrt_contents.replace(',', '<br>')
            chars = "'[]"
            for i in chars:
                itrt_contents = itrt_contents.replace(i, '')
            return itrt_contents
        else:
            return "잘못된 정보를 입력하셨습니다. 다시 시도해주세요."
    except IndexError:
        return "잘못된 정보를 입력하셨습니다. 다시 시도해주세요."
