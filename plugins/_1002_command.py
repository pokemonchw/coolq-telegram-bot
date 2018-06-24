import logging

import plugins.textHandle
import global_vars
import telegram
from main.command import command_listener
from telegram.ext import MessageHandler, Filters
from telegram.ext.dispatcher import DispatcherHandlerStop

from main.utils import get_forward_index, get_plugin_priority

logger = logging.getLogger("CTB." + __name__)
logger.debug(__name__ + " loading")

# Commands are only available in group and discuss
# For private chat, another plugin will take over


def tg_command(bot: telegram.Bot,
               update: telegram.Update):
    if update.edited_message:  # handle edit
        message: telegram.Message = update.edited_message
    else:
        message: telegram.Message = update.message

    if not message.text.startswith(global_vars.commandSwitch):  # no command indicator
        return
    textJudge = message.text
    textJudge = plugins.textHandle.fanZhuanJian(textJudge)
    if textJudge == message.text:
        global_vars.fanJian = 'jian'
    else:
        global_vars.fanJian = 'fan'
    textJudge = plugins.textHandle.quanZhuanBan(textJudge)
    message.text = textJudge
    tg_group_id = message.chat_id  # telegram group id
    tg_reply_to = message.reply_to_message

    logger.debug('Command indicator met: ' + message.text)
    text = message.text

    for command in global_vars.command_list:  # process all non-forward commands
        if command.tg_only and (text.find(global_vars.commandSwitch + str(command.command)) > -1):
            logger.debug(f'Matched Telegram only command: {command.command}')
            global_vars.tgMessage = message.text
            command.handler(tg_group_id=tg_group_id,
                            tg_user=message.from_user,
                            tg_message_id=message.message_id,
                            tg_reply_to=tg_reply_to)

            raise DispatcherHandlerStop()

    forward_index = get_forward_index(tg_group_id=tg_group_id)
    if forward_index == -1:
        logger.warning('Forward not found, please check your forward settings.')
        raise DispatcherHandlerStop()

    for command in global_vars.command_list:  # process all forward commands
        if not command.tg_only and not command.qq_only and (text.find(global_vars.commandSwitch + str(command.command)) > -1):
            logger.debug(f'Matched general command: {command.command}')
            global_vars.tgMessage = message.text
            command.handler(forward_index,
                            tg_user=message.from_user,
                            tg_group_id=tg_group_id,
                            tg_message_id=message.message_id,
                            tg_reply_to=tg_reply_to)
            raise DispatcherHandlerStop()


global_vars.dp.add_handler(MessageHandler(Filters.text & Filters.group,
                                          tg_command),
                           get_plugin_priority(__name__))


# decorator 'message_type', 'message_type', ..., group=number
@global_vars.qq_bot.on_message('group', 'discuss', group=get_plugin_priority(__name__))
def qq_command(context):
    if len(context['message']) > 1:  # rich text can not be commands
        return {'pass': True}

    if context['message'][0]['type'] != 'text':  # commands can only be pure text
        return {'pass': True}

    qq_group_id = context.get('group_id')
    qq_discuss_id = context.get('discuss_id')

    textJudge = context['message'][0]['data']['text']
    textJudge = plugins.textHandle.fanZhuanJian(textJudge)
    if textJudge == context['message'][0]['data']['text']:
        global_vars.fanJian = 'jian'
    else:
        global_vars.fanJian = 'fan'
    textJudge = plugins.textHandle.quanZhuanBan(textJudge)
    context['message'][0]['data']['text'] = textJudge

    text = context['message'][0]['data']['text']  # get message text

    if not text.startswith(global_vars.commandSwitch):  # no command indicator
        return {'pass': True}

    logger.debug('Command indicator met: ' + text)
    text = text[2:]

    for command in global_vars.command_list:  # process all non-forward commands
        if command.qq_only and (text.find(global_vars.commandSwitch + str(command.command)) > -1):
            logger.debug(f'Matched QQ only command: {command.command}')
            global_vars.qqMessage = context['message'][0]['data']['text']
            return command.handler(qq_group_id,
                                   qq_discuss_id,
                                   int(context['user_id']))

    forward_index = get_forward_index(qq_group_id=qq_group_id,
                                      qq_discuss_id=qq_discuss_id)
    if forward_index == -1:
        logger.warning('Forward not found, please check your forward settings.')
        return ''

    for command in global_vars.command_list:  # process all forward commands
        if not command.tg_only and not command.qq_only and (text == command.command or text == command.short_command):
            logger.debug(f'Matched general command: {command.command}')
            global_vars.qqMessage = context['message'][0]['data']['text']
            return command.handler(forward_index,
                                   qq_group_id=qq_group_id,
                                   qq_discuss_id=qq_discuss_id,
                                   qq_user=int(context['user_id']))

    return {'pass': True}


@command_listener('cmd', qq_only=True, description='查看命令列表')
def command_qq(qq_group_id: int,
               qq_discuss_id:int,
               qq_user: int):
    result = '\n'
    for command in global_vars.command_list:
        if not command.tg_only:
            result += f'{command.command}({command.short_command}): \n  {command.description}\n'
    return {'reply': result}


@command_listener('cmd', tg_only=True, description='查看命令列表')
def command_tg(tg_group_id: int,
               tg_user: telegram.User,
               tg_message_id: int,
               tg_reply_to: telegram.Message):
    result = ''
    for command in global_vars.command_list:
        if not command.qq_only:
            result += f'{command.command}({command.short_command}): \n  {command.description}\n'
    global_vars.tg_bot.sendMessage(chat_id=tg_group_id,
                                   text=result,
                                   reply_to_message_id=tg_message_id)


@command_listener('帮助', qq_only=True, description='获取帮助信息')
def command_qq(qq_group_id: int,
               qq_discuss_id:int,
               qq_user: int):
    cmdText = global_vars.commandSwitch
    result = '''链接正常\n心智模型002号正常启动，多端消息正常链接中\n请使用'''+ cmdText + '''cmd查询命令菜单'''
    return {'reply': result}

@command_listener('帮助', tg_only=True, description='获取帮助信息')
def command_tg(tg_group_id: int,
               tg_user: telegram.User,
               tg_message_id: int,
               tg_reply_to: telegram.Message = None):
    cmdText = global_vars.commandSwitch
    result = '链接正常\n心智模型002号正常启动，多端消息正常链接中\n请使用' + cmdText + 'cmd查询命令菜单'
    global_vars.tg_bot.sendMessage(chat_id=tg_group_id,
                                   text=result,
                                   reply_to_message_id=tg_message_id,
                                   parse_mode='HTML')