#!/usr/bin/python3
import notify2
import subprocess
import global_vars
from bot_constant import *
import telegram
import plugins.EarthPlugins.PushMastodon as PushMastodon
import plugins.EarthPlugins.CacheHandle as CacheHandle

def messagePush(message):
    if CacheHandle.nowMassageId == 'start':
        pass
    else:
        systemMessage(message)
        shellMessage(message)
        tgQQMessage(message)
        if CacheHandle.nowMassageId == 'Seismic' or CacheHandle.nowMassageId == 'Typhoon':
            mastodonMessage(message)
    CacheHandle.nowMassageId = ''

def systemMessage(message):
    notify2.init("地球监测站")
    earthMonitorPush = notify2.Notification("地球监测站Past.1",message)
    earthMonitorPush.set_hint("x",10)
    earthMonitorPush.set_hint("y",10)
    earthMonitorPush.show()

def shellMessage(message):
    subprocess.call("echo '地球监测站Past.1 \n" + message + "'", shell=True)

def mastodonMessage(message):
    PushMastodon.pushMessage(message)

def tgQQMessage(message):
    try:
        tgMessage(message)
    except telegram.error.TimedOut:
        tgMessage(message)
    qqMessage(message)

def tgMessage(message):
    return global_vars.tg_bot.send_message(chat_id=FORWARD_LIST[0]['TG'],text=message)

def qqMessage(message):
    return  global_vars.qq_bot.send_group_msg(group_id=FORWARD_LIST[0]['QQ'],message=message,auto_escape=True)['message_id']
