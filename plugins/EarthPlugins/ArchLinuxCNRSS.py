import urllib.request
import urllib.error
import xmltodict
import json
import os
from plugins.EarthPlugins import MessagePush
import time
import plugins.EarthPlugins.CacheHandle as CacheHandle

# 获取RSS信息
def getArchLinuxCNRSS():
    url = 'https://www.archlinuxcn.org/feed/'
    try:
        rss = urllib.request.urlopen(url)
        rssXML = rss.read()
        rssDict = xmltodict.parse(rssXML)
        rssJsonStr = json.dumps(rssDict, ensure_ascii=False)
        rssJson = json.loads(rssJsonStr)
        articleList = rssJson['rss']['channel']['item']
        judgeArticle(articleList)
    except urllib.error.HTTPError:
        time.sleep(10)
        getArchLinuxCNRSS()
    pass

# 文章信息判断
def judgeArticle(articleList):
    baseDir = os.path.dirname(__file__)
    filePath = os.path.join(baseDir, 'data','archLinuxCN', 'articleList.json')
    if os.path.exists(filePath) and os.path.isfile(filePath):
        writeArticle(articleList,'0')
    else:
        writeArticle(articleList,'1')
    pass

# 写入文章
def writeArticle(articleList,judge):
    baseDir = os.path.dirname(__file__)
    filePath = os.path.join(baseDir,'data', 'archLinuxCN', 'articleList.json')
    articleJson = _loadjson(filePath)
    if judge == '0':
        for i in range(0, len(articleList)):
            articleListKeys = articleList[i]
            writeJudge = judgeJsonKeys(articleListKeys,articleJson)
            if writeJudge == '1':
                articleJson.append(getArticleInfo(articleListKeys))
                message = '心智模型001号通信ing' + '\n' + 'ArchLinuxCN有新的变动日志，请留意' + '\n'
                message = message + articleListKeys['title'] + '\n' + articleListKeys['link'] + '\n' + articleListKeys['pubDate']
                CacheHandle.nowMassageId = 'ArchLinuxCNRSS'
                MessagePush.messagePush(message)
    else:
        for i in range(0,len(articleList)):
            articleJson.append(getArticleInfo(articleList[i]))
        message = "心智模型001号通信ing" + '\n' + "ArchLinuxCN变动日志已更新完成，请留意"
        CacheHandle.nowMassageId = 'ArchLinuxCNRSS'
        MessagePush.messagePush(message)
    articleJsonString = json.dumps(articleJson)
    articleFile = open(filePath, 'w', encoding='utf-8')
    articleFile.write(articleJsonString)
    articleFile.close()

# 文章信息获取
def getArticleInfo(keys):
    loadArticleJson = {}
    loadArticleJson['title'] = keys['title']
    loadArticleJson['link'] = keys['link']
    loadArticleJson['pubDate'] = keys['pubDate']
    return loadArticleJson

def judgeJsonKeys(mainKey,sonKeys):
    judge = '1'
    for i in range(0,len(sonKeys)):
        sonKey = sonKeys[i]
        if sonKey['title'] == mainKey['title']:
            judge = '0'
            break
    return judge

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
