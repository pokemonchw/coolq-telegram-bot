import urllib.request as request
import re
import os
import json
import plugins.EarthPlugins.MessagePush as messagepush
import plugins.EarthPlugins.CacheHandle as CacheHandle
import time
import datetime

baseDir = os.path.dirname(__file__)

def pushTyphoonInfo():
    typhoonData = getTyphoonData()
    typhoonSonData = typhoonData['typhoonData']
    typhoonNameList = typhoonData['typhoonNameList']
    typhoonIdList = typhoonData['typhoonIdList']
    value = []
    for key in typhoonSonData:
        value.append(key)
    for typhoonSon in typhoonSonData:
        typhoonIdIndex = value.index(typhoonSon)
        typhoonName = typhoonNameList[typhoonIdIndex]
        typhoonId = typhoonIdList[typhoonIdIndex]
        writeData = typhoonSonData[typhoonSon]
        fileJudge(writeData,typhoonId,typhoonName)

def pushNews():
    url = 'http://typhoon.weather.com.cn/'
    http = request.urlopen(url)
    content = http.read().decode('utf-8')
    title = re.findall(r'shtml" target=' + '"_blank' + '" >' + '(.*)' + '</span></h3>-->',content)
    text = re.findall(r'        <p><p>(.*)</p></a></p>',content)
    time = re.findall(r'</a></span><b>(.*)</b></h2>',content)
    newsData = os.path.join(baseDir,'data','typhoon','news',time[0])
    data = {'title':title[0],'text':text[0]}
    if os.path.isfile(newsData):
        fileData = _loadjson(newsData)
        if data in fileData:
            pass
        else:
            CacheHandle.nowMassageId = 'Typhoon'
            message = "心智模型001号通信ing" + '\n' + '气象台发布了新的信息，正在为您同步' + '\n' +  \
                      title[0] + ':' + '\n' + \
                      text[0] + '\n' + \
                      '同步完成，请留意'
            pushMessage(message)
            fileData.append(data)
            fileStr = json.dumps(fileData)
            newsFile = open(newsData, 'w', encoding='utf-8')
            newsFile.write(fileStr)
            newsFile.close()
    else:
        CacheHandle.nowMassageId = 'Typhoon'
        fileData = _loadjson(newsData)
        message = "心智模型001号通信ing" + '\n' + '气象台发布了新的信息，正在为您同步' + '\n' + \
                  title[0] + ':' + '\n' + \
                  text[0] + '\n' + \
                  '同步完成，请留意'
        pushMessage(message)
        fileData.append(data)
        fileStr = json.dumps(fileData)
        newsFile = open(newsData, 'w', encoding='utf-8')
        newsFile.write(fileStr)
        newsFile.close()

def fileJudge(typhoonData,typhoonId,typhoonName):
    fileName = typhoonId + '.json'
    fileData = os.path.join(baseDir,'data','typhoon',fileName)
    if os.path.isfile(fileData):
        fileJson = _loadjson(fileData)
        if typhoonData == fileJson:
            pass
        else:
            typhoonDataValueList = []
            for typhoonDataValue in typhoonData:
                year = typhoonDataValue['year']
                month = typhoonDataValue['month']
                day = typhoonDataValue['day']
                hour = typhoonDataValue['hour']
                minute = typhoonDataValue['minute']
                timeJudgeData = timeJudge(year,month,day,hour,minute)
                if timeJudgeData == '0':
                    typhoonDataValueList.append(typhoonDataValue)
                else:
                    pass
            messageData = typhoonDataValueList[len(typhoonDataValueList) - 1]
            year = messageData['year']
            month = messageData['month']
            day = messageData['day']
            hour = messageData['hour']
            minute = messageData['minute']
            longitude = messageData['longitude']
            latitude = messageData['latitude']
            pressure = messageData['pressure']
            windSpeed = messageData['windSpeed']
            message = "心智模型001号通信ing" + '\n' + "观测站正在向您同步台风" + typhoonName + "的最新信息" + '\n' + \
                      "UTC+8时间:" + year + "年" + month + "月" + day + "日" + hour + "点" + minute + "分" + '\n' + \
                      "经度:" + longitude + ",纬度:" + latitude + '\n' + \
                      "中心气压:" + pressure + 'hPa' + '\n' + \
                      "最大风速:" + windSpeed + 'm/s' + '\n' + \
                      "同步完成，请留意"
            if messageData == fileJson[len(typhoonDataValueList) - 1]:
                pass
            else:
                pass
                #CacheHandle.nowMassageId = 'Typhoon'
                #pushMessage(message)
            typhoonDataStr = json.dumps(typhoonData)
            typhoonFile = open(fileData, 'w', encoding='utf-8')
            typhoonFile.write(typhoonDataStr)
            typhoonFile.close()
    else:
        typhoonDataStr = json.dumps(typhoonData)
        typhoonFile = open(fileData, 'w', encoding='utf-8')
        typhoonFile.write(typhoonDataStr)
        typhoonFile.close()

def timeJudge(year,month,day,hour,minute):
    year = int(year)
    month = int(month)
    day = int(day)
    hour = int(hour)
    minute = int(minute)
    try:
        localTime = datetime.datetime(year,month,day,hour,minute)
    except ValueError:
        return '1'
    utcTime = local2utc(localTime)
    nowTime = datetime.datetime.now() + datetime.timedelta(hours=+8)
    utcTime = time.mktime(utcTime.timetuple())
    nowTime = time.mktime(nowTime.timetuple())
    if utcTime - nowTime < 0:
        return '0'
    else:
        return '1'

def pushMessage(message):
    messagepush.messagePush(message)

def getTyphoonData():
    url = 'http://typhoon.weather.com.cn/data/typhoonFlash/taifeng1.xml'
    http = request.urlopen(url)
    content = http.read().decode('utf-8')
    readTyphoonList = content.split('\n')
    typhoonList = []
    typhoonNameList = []
    for readTyphoon in readTyphoonList:
        if '<tfProps code=' in readTyphoon:
            typhoonId = re.findall(r'<tfProps code="' +  '(.*)' + '"  title=',readTyphoon)
            typhoonName = re.findall(r'  title="' + '(.*)' + '" data=',readTyphoon)
            typhoonId = listToStr(typhoonId)
            typhoonName = listToStr(typhoonName)
            typhoonList.append(typhoonId)
            typhoonNameList.append(typhoonName)
        else:
            pass
    typhoonData = typhoonJudgment(typhoonList)
    return {'typhoonData':typhoonData,'typhoonNameList':typhoonNameList,'typhoonIdList':typhoonList}

def typhoonJudgment(typhoonList):
    data = {}
    for typhoonId in typhoonList:
        url = 'http://typhoon.weather.com.cn/data/typhoonFlash/' + typhoonId + '.xml'
        http = request.urlopen(url)
        content = http.read().decode('utf-8')
        typhoonInfoList = getTyphoonInfoData(content)
        data[typhoonId] = typhoonInfoList
    return data

def getTyphoonInfoData(typhoonInfo):
    readInfoList = typhoonInfo.split('\n')
    infoData = []
    for readInfo in readInfoList:
        if '<tfProps y=' in readInfo:
            year = re.findall(r'<tfProps y="' +  '(.*)' + '" m=',readInfo)
            year = listToStr(year)
            month = re.findall(r' m="' + '(.*)' + '" d=',readInfo)
            month = listToStr(month)
            day = re.findall(r' d="' + '(.*)' + '" h=',readInfo)
            day = listToStr(day)
            hour = re.findall(r' h="' + '(.*)' + '" t=',readInfo)
            hour = listToStr(hour)
            minute = re.findall(r' t="' + '(.*)' + '" jd=',readInfo)
            minute = listToStr(minute)
            longitude = re.findall(r' jd="' + '(.*)' + '" wd=',readInfo)
            longitude = listToStr(longitude)
            latitude = re.findall(r' wd="' + '(.*)' + '" qy=',readInfo)
            latitude = listToStr(latitude)
            pressure = re.findall(r' qy="' + '(.*)' + '" fs=',readInfo)
            pressure = listToStr(pressure)
            windSpeed =re.findall(r' fs="' + '(.*)' + '" en7=',readInfo)
            windSpeed = listToStr(windSpeed)
            data = {
                'year' : year,
                'month' : month,
                'day' : day,
                'hour' : hour,
                'minute':minute,
                'longitude' : longitude,
                'latitude' : latitude,
                'pressure' : pressure,
                'windSpeed' : windSpeed
            }
            infoData.append(data)
        else:
            pass
    return infoData

def listToStr(list):
    string = ''
    for i in list:
        string = string + i
    return string

def _loadjson(filepath):
    try:
        if is_utf8bom(filepath):
            ec = 'utf-8-sig'
        else:
            ec = 'utf-8'
        with open(filepath, 'r', encoding=ec) as f:
            jsondata = json.loads(f.read())
    except json.decoder.JSONDecodeError:
        jsondata = []
    except FileNotFoundError:
        jsondata = []
    return jsondata

def is_utf8bom(pathfile):
    if b'\xef\xbb\xbf' == open(pathfile, mode='rb').read(3):
        return True
    return False

def local2utc(local_st):
    time_struct = time.mktime(local_st.timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st
