#!/usr/bin/python3
import datetime
import urllib.request
import urllib.error
import re
import os
import time
from plugins.EarthPlugins import MessagePush
import plugins.EarthPlugins.CacheHandle as CacheHandle

# 抓取网页数据
def getSeismicInformation():
    url = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.atom'
    http = urlopen(url)
    content = http.read().decode('utf-8')
    nation = re.findall(r'</id><title>M(.*?) - (.*?)</title><updated>',content)
    utcTime = re.findall(r'Time</dt><dd>(.*) (.*) UTC</dd><dd>', content)
    dimension = re.findall(r'</dd><dt>Location</dt><dd>(.*)&deg;(.*) (.*)&deg;(.*)</dd><dt>', content)
    informationProcessing(nation,utcTime,dimension)
    pass

def urlopen(url):
    try:
        http = urllib.request.urlopen(url)
    except urllib.error.URLError:
        time.sleep(1)
        http = urlopen(url)
    return http

# 处理数据
def informationProcessing(nation,utcTime,dimension):
    for loop in range(0, len(nation), 1):
        #时间处理
        utc8Time = utcTime[loop]
        utc8TimeS = str(utc8Time)
        utc8T = time.strptime(utc8TimeS,"('%Y-%m-%d', '%H:%M:%S')")
        utc8D = datetime.datetime(*utc8T[:6])
        localTime = utc2local(utc8D)
        localTimeS = str(localTime)
        utcTimeS = str(utc8TimeS)
        utcT = time.strptime(utcTimeS, "('%Y-%m-%d', '%H:%M:%S')")
        utcD = datetime.datetime(*utcT[:6])
        utcS = str(utcD)
        #地名处理
        if str(nation[loop][1]).find(',') < 1:
            nationS = str(nation[loop][1])
            nationS = nationS + ","
            seismicInformation = "nagnitude:" + nation[loop][0] + \
                                 ",place:" + nationS + \
                                 ",utcTime:" + utcS + \
                                 ",localTime:" + localTimeS + \
                                 ",dimension:" + dimension[loop][0]
            nagnitudeJudgment(seismicInformation, nation[loop][0], localTimeS)
        else:
            seismicInformation = "nagnitude:" + nation[loop][0] + \
                                 ",place:" + nation[loop][1] + \
                                 ",utcTime:" + utcS + \
                                 ",localTime:" + localTimeS + \
                                 ",dimension:" + dimension[loop][0]
            nagnitudeJudgment(seismicInformation, nation[loop][0], localTimeS)
    pass

# 震级判断
def nagnitudeJudgment(seimicInformation,nagnitude,localTimeS):
    dataTime = localTimeS[0:10]
    if 'Volcanic Eruption' in nagnitude:
        nagnitudeJudge = float(nagnitude.strip('Volcanic Eruption'))
    elif 'Explosion' in nagnitude:
        nagnitudeJudge = float(nagnitude.strip('Explosion'))
    else:
        nagnitudeJudge = float(nagnitude)
    if nagnitudeJudge >= 6.5:
        baseDir = os.path.dirname(__file__)
        filePath = os.path.join(baseDir, 'data/seismicInformation', 'strongShock.csv')
        alertMessage = 0
        writeJudgment(seimicInformation,filePath,alertMessage)
    else:
        baseDir = os.path.dirname(__file__)
        filePath = os.path.join(baseDir, 'data/seismicInformation', dataTime + '.csv')
        alertMessage = 1
        writeJudgment(seimicInformation, filePath,alertMessage)
    pass

# 读写判断
def writeJudgment(seimicInformation,filePath,alertMessage):
    if os.path.exists(filePath) and os.path.isfile(filePath):
        file = open(filePath,'r')
        line = file.readlines()
        file.close()
        line = list(line)
        while str(line).find(seimicInformation) == -1:
            while alertMessage == 0:
                message = "心智模型001号通信ing \n 正在向您传输高等地震灾害实况，具体信息为:" + "\n" +\
                           seimicInformation + "\n" +\
                           "该信息已保存至日志中，请留意"
                CacheHandle.nowMassageId = 'Seismic'
                MessagePush.messagePush(message)
                break
            writeSeismicInformation(seimicInformation, filePath)
            break
    else:
        while alertMessage == 0:
            message = "心智模型001号通信ing \n 正在向您传输高等地震灾害实况，具体信息为:" + "\n" +\
                       seimicInformation + "\n" +\
                       "该信息已保存至日志中，请留意"
            CacheHandle.nowMassageId = 'Seismic'
            MessagePush.messagePush(message)
            break
        writeSeismicInformation(seimicInformation, filePath)
    pass

# 写入文件
def writeSeismicInformation(seimicInformation,filePath):
    if os.path.exists(filePath) and os.path.isfile(filePath):
        file = open(filePath, 'a', encoding='utf-8')
        file.write(seimicInformation + "\n")
        file.close()
    else:
        file = open(filePath, 'w', encoding='utf-8')
        file.write(seimicInformation + "\n")
        file.close()
    pass

# UTC时间转本地时间（+8:00）
def utc2local(utc_st):
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = utc_st + offset
    return local_st
