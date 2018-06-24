#!/usr/bin/python3
import subprocess
import time
import threading
from plugins.EarthPlugins import MessagePush, GithubRecord, SeismicInformation,ArchLinuxCNRSS,CacheHandle,TyphoonInformation

def start():
    tA = threading.Thread(target=seismicInformation,daemon=True)
    tB = threading.Thread(target=satelliteDesktop,daemon=True)
    tC = threading.Thread(target=synchronizationGithub,daemon=True)
    tD = threading.Thread(target=archLinuxCnRss,daemon=True)
    tE = threading.Thread(target=typhoonInformation,daemon=True)
    tF = threading.Thread(target=typhoonNews,daemon=True)
    tStart = threading.Thread(target=startInformation,daemon=True)
    tA.start()
    time.sleep(1)
    tB.start()
    time.sleep(1)
    tC.start()
    time.sleep(1)
    tD.start()
    time.sleep(1)
    tE.start()
    time.sleep(1)
    tF.start()
    time.sleep(1)
    tStart.start()
    pass

def archLinuxCnRss():
    print(1111)
    ArchLinuxCNRSS.getArchLinuxCNRSS()
    time.sleep(60)
    archLinuxCnRss()
    pass

def typhoonNews():
    print(2222)
    TyphoonInformation.pushNews()
    time.sleep(60)
    typhoonNews()
    pass

def seismicInformation():
    print(3333)
    SeismicInformation.getSeismicInformation()
    time.sleep(60)
    seismicInformation()
    pass

def satelliteDesktop():
    subprocess.call("himawaripy", shell=True)
    time.sleep(600)
    satelliteDesktop()
    pass

def synchronizationGithub():
    print(4444)
    try:
        GithubRecord.getGithubRecord()
        time.sleep(60)
        synchronizationGithub()
    except urllib.error.URLError:
        synchronizationGithub()
    pass

def typhoonInformation():
    print(5555)
    TyphoonInformation.pushTyphoonInfo()
    time.sleep(60)
    typhoonInformation()
    pass

def startInformation():
    message = "链接建立完成，通信开始，监测站正常工作中"
    CacheHandle.nowMassageId = 'start'
    MessagePush.messagePush(message)
    pass
