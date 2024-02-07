import requests
import re
# import는 한 줄에 하나씩 해주는게 좋음!(필수는 아닌데 관례상)

url = "https://www.kma.go.kr/w/rss/dfs/hr1-forecast.do?zone=4157058000"


def get_weather_info():
  response = requests.get(url)
  wfor = re.findall("<wfKor>(.+)</wfKor>", response.text)[0]
  temp = re.findall("<temp>(.+)</temp>", response.text)[0]
  humi = re.findall("<reh>(.+)</reh>", response.text)[0]
  
  # 함수 설계는 완벽하다!
  # 다만 우리가 해야할 것은 인터넷에서 받아온 날씨 정보를 반환해주는 것!
  # 이 함수에서 프린트를 해버리면 받아온 정보를 웹 사이트에서 사용할 수 없다!

  # print("=======실시간 날씨 예보=======")
  # print("기상상태: {}".format(wfor))
  # print("현재온도: {}°C".format(temp))
  # print("현재습도: {}%".format(humi))


  # 이렇게 데이터를 반환해야 웹 사이트에서 사용할 수 있다!
  weather_info = "기상상태: {}\n".format(wfor) + "현재온도: {}°C\n".format(temp) + "현재습도: {}%\n".format(humi)
  weather_info = weather_info.replace('\n', '<br>')
  return weather_info


# schedule.every(10).seconds.do(get_weather_information)

# while True:
#   now = datetime.datetime.now()
#   now = now.strftime("%Y/%n/%d %H:%S")
#   schedule.run_pending()
#   time.sleep(2)

if __name__ == "__main__":
  print(get_weather_info())