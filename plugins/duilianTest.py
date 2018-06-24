import urllib.request
import urllib.parse
import urllib.error
import json
from main.command import command_listener
import telegram
import global_vars
import plugins.textHandle

# 对联命令
@command_listener('对联 ',tg_only=True,description='对对联')
def getDuilian_tg(tg_group_id: int=None,
                   tg_user: telegram.User=None,
                   tg_message_id: int=None,
                   tg_reply_to: telegram.Message=None):
    commandText = global_vars.tgMessage
    message = getXiaLian(commandText,'对联 ')
    global_vars.tg_bot.send_message(chat_id=tg_group_id,
                                    text=message,
                                    reply_to_message_id=tg_message_id,
                                    parse_mode='HTML')

@command_listener('对联 ',qq_only=True,description='对对联')
def getDuilian_qq(qq_group_id: int=None,
                  qq_discuss_id: int=None,
                  qq_user: int=None):
    commandText = global_vars.qqMessage
    message = getXiaLian(commandText,'对联 ')
    return {'reply': message}

def getXiaLian(text,command):
    text = text.strip(global_vars.commandSwitch + command)
    text = plugins.textHandle.banZhuanQuan(text)
    textEncode = urllib.parse.quote(text)
    url = 'https://ai-backend.binwang.me/chat/couplet/' + textEncode
    http = urllib.request.urlopen(url)
    httpText = str(http.read(), 'UTF-8')
    httpJson = json.loads(httpText)
    output = httpJson['output']
    if global_vars.fanJian == 'fan':
        output = plugins.textHandle.jianZhuanFan(output)
    return output