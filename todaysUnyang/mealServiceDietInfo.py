import requests, json

DIET_INFO_API_KEY = 'b72c971c69c14bfe87cecb165d696fbf' # API 키
SCHUL_DEPT_CODE = 'J10' #경기도교육청 코드
SCHUL_CODE = 7531103 #운양고등학교 코드

def getDietInfo(today):
    dietInfo = _getMealServiceDietInfo(today)
    try:
        return str(dietInfo['mealServiceDietInfo'][1]['row'][0]['DDISH_NM']) 
    except:
        return str(dietInfo['RESULT']['MESSAGE'])

def _getMealServiceDietInfo(today): #함수명 앞 '_'는 내부 함수임을 뜻함.
    try:
        with open('todaysUnyang/mealDietInfo.json', 'r', encoding='utf-8') as f:
            savedDietInfo = json.load(f)

        if (str(savedDietInfo['mealServiceDietInfo'][1]['row'][0]['MLSV_YMD']) == str(today)):
            return savedDietInfo
        else:
            raise
    except:
        url = 'https://open.neis.go.kr/hub/mealServiceDietInfo' #사이트에 기재된 API 요청 주소
        parameters = {
            'KEY' : env.DIET_INFO_API_KEY,                          #사이트에서 발급받은 API 인증키
            'Type' : 'json',                                    #받아올 데이터의 자료 구조
            'ATPT_OFCDC_SC_CODE' : SCHUL_DEPT_CODE,         
            'SD_SCHUL_CODE' : SCHUL_CODE,                       #각각에 대한 설명은 API 사이트에 설명되어 있다.
            'MLSV_FROM_YMD' : today,
            'MLSV_TO_YMD' : today
        }
        requestsResponseData = requests.get(url, params=parameters)
        newDietInfo = json.loads(requestsResponseData.text)
        with open('todaysUnyang/mealDietInfo.json', 'w') as f:
            json.dump(newDietInfo, f, indent="\t")
        return newDietInfo