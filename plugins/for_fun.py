import logging

import telegram
from main.command import command_listener

from main.utils import get_forward_index, send_from_tg_to_qq

logger = logging.getLogger("CTB." + __name__)
logger.debug(__name__ + " loading")


@command_listener('dice', 'dice', tg_only=True, description='throw a dice')
def dice(tg_group_id: int,
         tg_user: telegram.User,
         tg_message_id: int,
         tg_reply_to: telegram.Message = None):
    forward_index = get_forward_index(tg_group_id=tg_group_id)
    if forward_index == -1:
        return

    reply_entity = list()
    reply_entity.append({
        'data': {'text': 'threw a dice'},
        'type': 'text'})
    reply_entity.append({
        'data': {'type': '1'},
        'type': 'dice'})

    send_from_tg_to_qq(forward_index,
                       reply_entity,
                       tg_group_id=tg_group_id,
                       tg_user=tg_user)


@command_listener('rps', 'rps', tg_only=True, description='rock paper stone')
def rps(tg_group_id: int,
        tg_user: telegram.User,
        tg_message_id: int,
        tg_reply_to: telegram.Message):
    forward_index = get_forward_index(tg_group_id=tg_group_id)
    if forward_index == -1:
            return

    reply_entity = list()
    reply_entity.append({
        'data': {'text': 'played rock–paper–scissors'},
        'type': 'text'})
    reply_entity.append({
        'data': {'type': '1'},
        'type': 'rps'})

    send_from_tg_to_qq(forward_index,
                       reply_entity,
                       tg_group_id=tg_group_id,
                       tg_user=tg_user)

