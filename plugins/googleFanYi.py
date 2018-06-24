import re
from main.command import command_listener
import telegram
import global_vars
from googletrans import Translator
import socks
import socket

translator = Translator()

LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'ar': 'arabic',
    'be': 'belarusian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'zh-CN': 'chinese_simplified',
    'zh-TW': 'chinese_traditional',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'gl': 'galician',
    'de': 'german',
    'el': 'greek',
    'iw': 'hebrew',
    'hi': 'hindi',
    'hu': 'hungarian',
    'is': 'icelandic',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'ko': 'korean',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'mk': 'macedonian',
    'ms': 'malay',
    'mt': 'maltese',
    'no': 'norwegian',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'ro': 'romanian',
    'ru': 'russian',
    'sr': 'serbian',
    'sk': 'slovak',
    'sl': 'slovenian',
    'es': 'spanish',
    'sw': 'swahili',
    'sv': 'swedish',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'yi': 'yiddish',
  }

@command_listener('翻译',tg_only=True,description="谷歌翻译，格式:\翻译 <目标语言> xxxx\n   简中:zh-CN,繁中:zh-TW,英语:en,日语:ja,德语:de,法语:fr,韩语:ko,俄语:ru")
def googleFanYiTg(tg_group_id: int=None,
                   tg_user: telegram.User=None,
                   tg_message_id: int=None,
                   tg_reply_to: telegram.Message=None):
    commandText = global_vars.tgMessage
    text = commandText.strip(global_vars.commandSwitch + '翻译')
    message = googleFanYi(commandText,'翻译')
    if message == 'Null':
        return {'reply': '输入错误，请重试'}
    else:
        message = message[0]
    message = text + '\n>>\n' + message
    global_vars.tg_bot.send_message(chat_id=tg_group_id,
                                    text=message,
                                    reply_to_message_id=tg_message_id)

@command_listener('翻译',qq_only=True,description="谷歌翻译，格式:\翻译 <目标语言> xxxx\n   简中:zh-CN,繁中:zh-TW,英语:en,日语:ja,德语:de,法语:fr,韩语:ko,俄语:ru")
def googleFanYiQq(qq_group_id: int=None,
                  qq_discuss_id: int=None,
                  qq_user: int=None):
    commandText = global_vars.qqMessage
    text = commandText.strip(global_vars.commandSwitch + '翻译')
    message = googleFanYi(commandText, '翻译')
    if message == 'Null':
        return {'reply': '输入错误，请重试'}
    else:
        message = message[0]
    message = text + '\n>>\n' + message
    return {'reply': message}

def googleFanYi(text,command):
    yuanYuZhong = re.findall(global_vars.commandSwitch + command + " <(.*)> - <",text)
    yuanYuZhong = listToStr(yuanYuZhong)
    socksDefault = socks.get_default_proxy()
    socketDefault = socket.socket
    socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 1080)
    socket.socket = socks.socksocket
    if yuanYuZhong == '':
        muBiaoYuZhong = re.findall(global_vars.commandSwitch + command + " <(.*)>",text)
        muBiaoYuZhong = listToStr(muBiaoYuZhong)
    else:
        muBiaoYuZhong = re.findall(global_vars.commandSwitch + command + " <" + yuanYuZhong + "> - <(.*)>",text)
        muBiaoYuZhong = listToStr(muBiaoYuZhong)
    if muBiaoYuZhong == '':
        message = text.strip(global_vars.commandSwitch + command + ' ')
        result = translator.translate(message,dest='zh-CN')
        if result.text == message:
            result = translator.translate(message,dest='en')
        else:
            pass
    else:
        try:
            if yuanYuZhong == '':
                message = text.strip(global_vars.commandSwitch + command + ' <' + muBiaoYuZhong + '> ')
                result = translator.translate(message,dest=muBiaoYuZhong)
            else:
                message = text.strip(global_vars.commandSwitch + command + ' <' + yuanYuZhong + '> - <' + muBiaoYuZhong + '> ')
                result = translator.translate(message,dest=muBiaoYuZhong,src=yuanYuZhong)
        except ValueError:
            message = text.strip(global_vars.commandSwitch + command)
            result = translator.translate(message,dest='zh-CN')
            if result.text == message:
                result = translator.translate(message,dest='en')
            else:
                pass
    socks.setdefaultproxy(socksDefault)
    socket.socket = socketDefault
    message = [result.text]
    return message

def listToStr(list):
    string = ''
    for i in list:
        string = string + i
    return string
