from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
from lunardate import LunarDate

today = datetime.now()
start_date = os.environ['START_DATE']
last_date = "2024-01-06"
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
    url = "https://restapi.amap.com/v3/weather/weatherInfo?city=141031&key=5a7f41e01808834cb30a5fac73607b23&extensions=all"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        forecast = data["forecasts"][0]["casts"][0]  # 获取第一个日期的天气预报信息
        daytemp_float = forecast["daytemp_float"]
        nighttemp_float = forecast["nighttemp_float"]
        dayweather  = forecast["dayweather"]
        nightweather = forecast["nightweather"]
    else:
        print("请求失败，状态码:", res.status_code)
    return daytemp_float,nighttemp_float ,dayweather,nightweather

def get_count():
  global start_date
  today = datetime.now()
  start_date_1 = datetime.strptime(start_date, "%Y-%m-%d")
  delta = today- start_date_1
  return delta.days
    
def not_meet():
  today = datetime.now()
  global last_date
  last_date_1 = datetime.strptime(last_date, "%Y-%m-%d")
  missU = today- last_date_1
  return missU

def get_birthday():
  today = datetime.now()
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

def get_today():
  today = datetime.now()
  formatted_date = today.strftime("%Y年%m月%d日")
  return formatted_date
    
def get_lunar_birthday():
    birthday_year = 2001
    birthday_month = 1
    birthday_day = 10
    today = datetime.now().date()
    lunar_today = LunarDate.fromSolarDate(today.year, today.month, today.day)

    lunar_birthday = LunarDate(birthday_year, birthday_month, birthday_day)
    
    if (lunar_birthday.month, lunar_birthday.day) < (lunar_today.month, lunar_today.day):
        lunar_birthday = LunarDate(lunar_today.year + 1, birthday_month, birthday_day)
    else:
        lunar_birthday = LunarDate(lunar_today.year, birthday_month, birthday_day)

    days_to_birthday = (lunar_birthday.toSolarDate() - today).days

    return days_to_birthday


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
daytemp_float,nighttemp_float ,dayweather,nightweather= get_weather()
data = {"weather":{"value":dayweather},
        "max_temperature":{"value":daytemp_float},
        "min_temperature":{"value":nighttemp_float},
        "love_days":{"value":get_count()},
        "birthday_left":{"value":get_birthday()},
        "words":{"value":get_words(), 
        "color":get_random_color()},
        "name":{"value":"傻宝儿"},
        "date":{"value":get_today()},
        "city":{"value":"山西省临汾市隰县"},
        "lunardate":{"value":get_lunar_birthday()},
        "missu":{"value":not_meet()}
        }
res = wm.send_template(user_id, template_id, data)
print(res)
