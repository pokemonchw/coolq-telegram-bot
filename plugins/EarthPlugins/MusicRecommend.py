#!/usr/bin/python3
import os

search_api = "http://music.163.com/api/search/pc"

def searchSong(key):

    pass

def getMusicRecommend():
    baseDir = os.path.dirname(__file__)
    recomsongPath = os.path.join(baseDir, 'data/recommendsong', 'recomsong')
    recomnamePath = os.path.join(baseDir, 'data/recommendsong', 'recomname')
    recomnameN = open(recomnamePath).read()
    recomsongN = open(recomsongPath).read()
    searchSong(recomsongN)
    pass