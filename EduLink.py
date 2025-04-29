import time, datetime, requests, json, TTS, logging, random, os, siot, configparser
from requests.exceptions import RequestException
from unihiker import GUI, Audio
config = configparser.ConfigParser()
audio, gui = Audio(), GUI()
if not os.path.exists(os.path.join(os.getcwd(), "log")):
    os.mkdir(os.path.join(os.getcwd(), "log"))
if not os.path.exists(os.path.join(os.getcwd(), "audio")):
    os.mkdir(os.path.join(os.getcwd(), "audio"))
logging.basicConfig(filename='log/'+time.strftime("%Y-%m-%d %H:%M:%S")+'.log', filemode='w', level=logging.DEBUG, format = '%(asctime)s at %(name)s %(levelname)s : %(message)s')
log = logging.getLogger(__name__)
WEATHER_KEY=""
MQTT_TOPIC=""
MQTT_USER=""
MQTT_PWD=""
try:
    config.read('config.ini')
    TTS.API_KEY=config.get('TTS', 'API_KEY')
    TTS.SECRET_KEY=config.get('TTS', 'SECRET_KEY')
    WEATHER_KEY=config.get('WEATHER', 'KEY')
    MQTT_TOPIC=config.get('MQTT', 'TOPIC')
    MQTT_USER=config.get('MQTT', 'USER')
    MQTT_PWD=config.get('MQTT', 'PASSWORD')
except Exception:
    log.critical("配置文件读取失败",exc_info=True)
    exit(0)
try:
    log.info("开始尝试连接MQTT")
    siot.init(client_id=MQTT_TOPIC,server="iot.dfrobot.com.cn",port=1883,user=MQTT_USER,password=MQTT_PWD)
    siot.connect()
    siot.loop()
    log.info("开始尝试订阅")
    siot.getsubscribe(topic=MQTT_TOPIC)
except Exception:
    log.critical("MQTT错误",exc_info=True)
weatherDic = {
    "晴": 61900,
    "少云": 61902,
    "晴间多云": 61903,
    "多云": 61901,
    "阴": 61904,
    "有风": 62187,
    "平静": 62187,
    "微风": 62187,
    "和风": 62187,
    "清风": 62187,
    "强风/劲风": 62022,
    "疾风": 62022,
    "大风": 62022,
    "烈风": 62022,
    "风暴": 62022,
    "狂爆风": 62022,
    "飓风": 61767,
    "热带风暴": 61767,
    "霾": 61744,
    "中度霾": 61751,
    "重度霾": 61752,
    "严重霾": 61753,
    "阵雨": 61909,
    "雷阵雨": 61911,
    "雷阵雨并伴有冰雹": 61937,
    "小雨": 61914,
    "中雨": 61915,
    "大雨": 61916,
    "暴雨": 61917,
    "大暴雨": 61919,
    "特大暴雨": 61920,
    "强阵雨": 61910,
    "强雷阵雨": 61911,
    "极端降雨": 61921,
    "毛毛雨/细雨": 61918,
    "雨": 61930,
    "小雨-中雨": 61923,
    "中雨-大雨": 61924,
    "大雨-暴雨": 61925,
    "暴雨-大暴雨": 61926,
    "大暴雨-特大暴雨": 61927,
    "雨雪天气": 61935,
    "雨夹雪": 61936,
    "阵雨夹雪": 61937,
    "冻雨": 61922,
    "雪": 61944,
    "阵雪": 61938,
    "小雪": 61931,
    "中雪": 61932,
    "大雪": 61933,
    "暴雪": 61934,
    "小雪-中雪": 61939,
    "中雪-大雪": 61940,
    "大雪-暴雪": 61941,
    "浮尘": 61949,
    "扬沙": 61948,
    "沙尘暴": 61950,
    "强沙尘暴": 61951,
    "龙卷风": 61768,
    "雾": 61947,
    "浓雾": 61955,
    "强浓雾": 61956,
    "轻雾": 61947,
    "大雾": 61954,
    "特强浓雾": 61956,
    "热": 61959,
    "冷": 61960,
    "未知": 61961
}

timetable = {}
def randName():
    ID=""
    for i in range(10):
        ID+=chr(random.randint(33,126))
    return "audio/"+ID

def on_message_callback(client, userdata, msg):
    log.info("收到远程消息 内容为 "+msg.payload.decode())
    log.info("开始生成远程消息语音")
    voiceName=randName()
    TTS.run(msg.payload.decode(),voiceName)
    currentClass = get_current_course(timetable)
    time.sleep(1)
    try:
        log.info("开始播放语音")
        audio.play(voiceName+".mp3")
    except pygame.Exception:
        log.error("播放错误",exc_info=True)
        log.info("播放完毕")

siot.set_callback(on_message_callback)

def get_current_course(timetable):
    try:
        now = datetime.datetime.now()
        current_weekday = now.strftime("%A")
        current_time = now.time()
        daily_courses = timetable.get(current_weekday, [])
        for course in daily_courses:
            start = datetime.datetime.strptime(course["start"], "%H:%M").time()
            end = datetime.datetime.strptime(course["end"], "%H:%M").time()
            if start <= current_time <= end:
                return format_course_output(course)
        for course in daily_courses:
            start = datetime.datetime.strptime(course["start"], "%H:%M").time()
            start_dt = datetime.datetime.combine(now.date(), start)
            if 0 < (start_dt - current_datetime).total_seconds() <= 120:
                return format_reminder_output(course)
        return format_no_class_output()
    except KeyError:
        log.error("错误：课表字段缺失",exc_info=True)
        return "当前没有课程\n "
    except Exception as e:
        log.error(f"未知错误",exc_info=True)
        return "当前没有课程\n "

def format_course_output(course):
    return (
        f"🏫{course['name']}\n"
        f"{course['start']} - {course['end']}"
    )

def format_reminder_output(course):
    return (
        f"🔔{course['name']}\n"
        f"{course['start']} - {course['end']}"
    )

def format_no_class_output():
    return "🏫🔔当前没有课程\n"

def weatherUpdate():
    global realweather,weatherPicText
    while True:
        try:
            log.info("天气请求开始发送")
            weatherJSON = requests.get("https://restapi.amap.com/v3/weather/weatherInfo?city=310106&key=f59801dded2d7b1c4f61c766a495038c")
            log.info(f"天气请求返回\n{weatherJSON.text}")
            log.info("开始JSON解码")
            weather = json.loads(weatherJSON.text)
            log.info("JSON解码完毕")
        except RequestException as e:
            log.error(f"天气请求失败",exc_info=True)
            weatherJSON = "{\"status\":\"0\"}"
            weather = json.loads(weatherJSON)
        except json.decoder.JSONDecodeError:
            log.error(f"JSON转化失败{str(e)}",exc_info=True)
            weatherJSON = "{}"
            weather = json.loads(weatherJSON)
        realweather = "--"
        weatherPicText = chr(61961)
        if weather["status"] == "1":
            weatherPicText = chr(weatherDic.get(weather['lives'][0]['weather'],61961))
            realweather = weather['lives'][0]['temperature_float']+"°C\n"+ weather['lives'][0]['weather']
        else:
            realweather = "--°C\n未知"
        time.sleep(60*60)

def scheduleUpdate():
    global currentClass
    while True:
        if(currentClass!=get_current_course(timetable) and "当前没有课程\n"!=get_current_course(timetable)):
            log.info("开始生成提醒语音")
            voiceName=randName()
            TTS.run(get_current_course(timetable).split('\n')[0]+"课，开始了！",voiceName)
            currentClass = get_current_course(timetable)
            time.sleep(1)
            try:
                log.info("开始播放语音")
                audio.play(voiceName+".mp3")
            except pygame.Exception:
                log.error("播放错误",exc_info=True)
            log.info("播放完毕")
        currentClass = get_current_course(timetable)
        time.sleep(0.5)

timetableJSON = {}
try:
    log.info("课表请求开始发送")
    timetableJSON = requests.get("https://timetables.2025.techfestival.yccj.ryanincn11.top/timetable.json")
    log.info(f"课表请求返回\n{timetableJSON.text}")
    log.info("开始JSON解码")
    timetable = json.loads(timetableJSON.text)
    log.info("JSON解码完毕")
except RequestException:
    log.error(f"课表请求失败",exc_info=True)
    timetableJSON = "{}"
    timetable = json.loads(timetableJSON)
realweather=""
weatherPicText=""
currentClass="\n"
gui.start_thread(weatherUpdate)
gui.start_thread(scheduleUpdate)
try:
    log.info("开始尝试加载背景")
    background=gui.draw_image(image="images/bg.jpg",x=0,y=0)
    log.info("加载背景成功")
    log.info("开始尝试加载字体")
    boldFont = gui.load_font('fonts/AdobeGothicStd-Bold.otf')
    ChineseFont = gui.load_font('fonts/Dengb.ttf')
    weatherFont = gui.load_font('fonts/qweather-icons.ttf')
    log.info("所有字体加载成功")
except Exception:
    log.critical("字体/背景加载失败",exc_info=True)
    exit(1)
weatherText=gui.draw_text(text=realweather,x=20,y=20,font_size=10, color="#FFFFFF")
weatherPic=gui.draw_text(text=weatherPicText,x=180,y=20,font_size=30, color="#FFFFFF", font_family=weatherFont)
timeText1=gui.draw_text(text=time.strftime("%H:%M:%S"),x=20,y=70,font_size=20, color="#FFFFFF", font_family=boldFont)
timeText2=gui.draw_text(text=time.strftime("%Y年%m月%d日"),x=20,y=100,font_size=15, color="#FFFFFF", font_family=boldFont)
classText1=gui.draw_text(text=currentClass.split('\n')[0],x=20,y=150,font_size=20, color="#FFFFFF", font_family=ChineseFont)
classText2=gui.draw_text(text=currentClass.split('\n')[1],x=20,y=180,font_size=15, color="#FFFFFF", font_family=ChineseFont)
while True:
    weatherText.config(text=realweather)
    weatherPic.config(text=weatherPicText)
    timeText1.config(text=time.strftime("%H:%M:%S"))
    timeText2.config(text=time.strftime("%Y年%m月%d日"))
    classText1.config(text=currentClass.split('\n')[0])
    classText2.config(text=currentClass.split('\n')[1])
    time.sleep(0.1)
