from main.command import command_listener
import telegram
import random
import global_vars

@command_listener('prpr',tg_only=True,description='prpr')
def tg_prpr(tg_group_id: int=None,
                  tg_user: telegram.User=None,
                  tg_message_id: int=None,
                  tg_reply_to: telegram.Message=None):
    prprText = ['(￣口￣)!!','(￣^￣)','(＞ε＜)','~(￣▽￣)~','(￣ˇ￣)','(＞﹏＜)','(＞▽＜)','(＞ω＜)','(￣∀￣)','(*′∇`*)','(=′∇`=)']
    prprMax = len(prprText)
    prprIndex = random.randint(0,prprMax)
    message = prprText[prprIndex]
    global_vars.tg_bot.send_message(chat_id=tg_group_id,
                                   text=message,
                                   reply_to_message_id=tg_message_id,
                                   parse_mode='HTML')

@command_listener('prpr',qq_only=True,description='prpr')
def qq_prpr(qq_group_id: int=None,
                  qq_discuss_id: int=None,
                  qq_user: int=None):
    prprText = ['(￣口￣)!!','(￣^￣)','(＞ε＜)','~(￣▽￣)~','(￣ˇ￣)','(＞﹏＜)','(＞▽＜)','(＞ω＜)','(￣∀￣)','(*′∇`*)','(=′∇`=)']
    prprMax = len(prprText)
    prprIndex = random.randint(0,prprMax)
    message = prprText[prprIndex]
    return {'reply': message}