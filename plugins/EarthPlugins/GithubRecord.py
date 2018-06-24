#!/usr/bin/python3
import os
import urllib.request
import urllib.error
import json
from plugins.EarthPlugins import MessagePush
import time
import plugins.EarthPlugins.CacheHandle as CacheHandle

# 读取github数据
def getGithubRecord():
    url = 'https://api.github.com/users/pokemonchw/repos'
    try:
        http = urllib.request.urlopen(url)
        httpJson = json.load(http)
        for loop in range(0, len(httpJson), 1):
            commitsUrl = httpJson[loop]['commits_url']
            commitName = httpJson[loop]['name']
            commitsUrl = str(commitsUrl[0:-6])
            getCommits(commitsUrl, commitName)
    except urllib.error.HTTPError:
        time.sleep(10)
        getGithubRecord()
    pass

# 读取commits数据
def getCommits(commitsUrl,commitName):
    commitHttp = urllib.request.urlopen(commitsUrl)
    commitJson = json.load(commitHttp)
    commitJudgment(commitJson[0],commitName)
    pass

# commit数据判断
def commitJudgment(commit,commitName):
    baseDir = os.path.dirname(__file__)
    filePath = os.path.join(baseDir, 'data','githubLastup', commitName)
    name = commit['commit']['author']['name']
    commitTime = commit['commit']['author']['date']
    message = commit['commit']['message']
    commitList = [commitName,name,commitTime,message]
    writeJudgment(filePath,commitList)
    pass

# 读写判断
def writeJudgment(filePath,commitList):
    commitName = commitList[0]
    name = commitList[1]
    commitTime = commitList[2]
    message = commitList[3]
    commit = "repo:" + commitName + ",author:" + name + ",date:" + commitTime + ",message:" + message
    if os.path.exists(filePath) and os.path.isfile(filePath):
        file = open(filePath,'r')
        line = file.readlines()
        file.close()
        line = list(line)
        judgment = "repo:" + commitName + ",author:" + name + ",date:" + commitTime
        while str(line).find(judgment) == -1:
            githubName = "仓库:" + commitName
            pushPeople = "提交人:" + name
            pushTime = "提交时间:" + commitTime
            remarks = "备注信息:" + message
            overMessage = "同步完成，请留意"
            messagePush = "心智模型001号通信ing \n 正在为您同步commits记录:" + "\n" +\
                           githubName + "\n" +\
                           pushPeople + "\n" +\
                           pushTime + "\n" +\
                           remarks + "\n" +\
                           overMessage
            CacheHandle.nowMassageId = 'Github'
            MessagePush.messagePush(messagePush)
            writeGithubLastup(commit,filePath)
            break
    else:
        CacheHandle.nowMassageId = 'Github'
        messagePush = "心智模型001号通信ing \n github仓库[" + commitName + "]信息同步ing \n 同步完成,请留意"
        MessagePush.messagePush(messagePush)
        writeGithubLastup(commit, filePath)
    pass

# 写入git同步记录
def writeGithubLastup(commit,filePath):
    file = open(filePath, 'w', encoding='utf-8')
    file.write(commit)
    file.close()
    pass
