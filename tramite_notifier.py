#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 23:50:09 2019

@author: alanzhao
"""

import os
import telepot
import textwrap

class TelegramNotifier:
    def __init__(self):
        self.telegram_bot = telepot.Bot(os.environ["BOT_TOKEN"])
        self.user_chat_id = os.environ["CHAT_ID"]
    
    def notify_tramite_movement(self, movement):
        message = """
        ¡Nuevo movimiento del trámite!
        Id: {}
        Fecha: {}
        Comentario: {}
        """.format(movement.external_id, movement.datetime, movement.comment)
        self.telegram_bot.sendMessage(chat_id = self.user_chat_id,
                                      text = textwrap.dedent(message))