from main.command import command_listener
import telegram
import datetime
import os
import random
import global_vars

baseDir = os.path.dirname(__file__)
qian = ['大吉 今看两楹橂，当与梦时同',
        '大凶 田园寥落干戈后，骨肉流离道路中',
        '上吉 锦江春色来天地，玉垒浮云变古今',
        '上吉 星垂平野阔，月涌大江流',
        '下凶 欲祭疑君在，天涯哭此时',
        '下凶 恐非平生魂，路远不可测',
        '上平 沧海月明柱有泪，蓝田日暖玉生烟',
        '上平 葡萄美酒夜光杯，欲饮琵琶马上催',
        '上平 繁华事散逐香尘，流水无情草自春',
        '上平 莫愁前路无知己，天下谁人不识君',
        '下平 不才明主弃，多病故人疏',
        '下平 念天地之悠悠，独怆然而涕下',
        '下平 夕阳无限好，只是近黄昏',
        '下平 东风不与周郎便，铜雀春深锁二乔',
        '中平 今夜偏知春气暖，虫声新透绿窗纱',
        '中平 清时有味是无能，闲爱孤云静爱僧',
        '中平 雁声远过潇湘去，十二楼中月自明',
        '中平 沙平水息声影绝，一杯相属君当歌',
        '中平 白日不到处，青春恰自来',
        '中平 野旷天低树，江清月近人',
        '中平 相望试登高，心随雁飞灭',
        '中平 迷津欲有问，平海夕漫漫',
        '中平 旧时王榭堂前燕，飞入寻常百姓家',
        '中平 海日生残夜，江春入旧年']

@command_listener('求签',tg_only=True,description='求签')
def qiuQianTg(tg_group_id: int=None,
                   tg_user: telegram.User=None,
                   tg_message_id: int=None,
                   tg_reply_to: telegram.Message=None):
    if qiuQianLog('tg',tg_user.id) == 'True':
        message = random.choice(qian)
    else:
        message = '命由天定，事在人为，请明日再来'
    global_vars.tg_bot.send_message(chat_id=tg_group_id,
                                    text=message,
                                    reply_to_message_id=tg_message_id,
                                    parse_mode='HTML')

@command_listener('求签',qq_only=True,description='求签')
def qiuQianQq(qq_group_id: int=None,
                  qq_discuss_id: int=None,
                  qq_user: int=None):
    if qiuQianLog('qq',str(qq_user)) == 'True':
        message = random.choice(qian)
    else:
        message = '命由天定，事在人为，请明日再来'
    return {'reply': message}

def qiuQianLog(im = '',id = ''):
    id = int(id)
    qiuQianTime = datetime.datetime.now()
    year = qiuQianTime.year
    month = qiuQianTime.month
    day = qiuQianTime.day
    qiuQianTime = str(year) + str(month) + str(day)
    dateTimeLogData = os.path.join(baseDir,'data','qiuQian')
    if im == 'qq':
        dateTimeLog = os.path.join(dateTimeLogData,'qq',qiuQianTime)
    else:
        dateTimeLog = os.path.join(dateTimeLogData,'tg', qiuQianTime)
    if os.path.exists(dateTimeLog) and os.path.isfile(dateTimeLog):
        logList = []
        with open(dateTimeLog, 'r') as f:
            for line in f.readlines():
                linestr = line.strip()
                logList.append(linestr)
        if str(id) in logList:
            return 'Null'
        else:
            file = open(dateTimeLog, 'a', encoding='utf-8')
            file.write('\n')
            file.write(str(id))
            file.close()
            return 'True'
    else:
        os.mknod(dateTimeLog)
        file = open(dateTimeLog, 'w', encoding='utf-8')
        file.write(str(id))
        file.close()
        return 'True'
