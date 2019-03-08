#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 23:50:09 2019

@author: alanzhao
"""

from os import environ
import telepot
import textwrap

class TelegramNotifier:
    def __init__(self):
        self.telegram_bot = telepot.Bot(environ["BOT_TOKEN"])
        self.user_chat_id = environ["CHAT_ID"]
        self.mute_available = environ["MUTE"].upper() == "TRUE"

    def notify(self, message, muteable = False):
        if not muteable or not self.mute_available:
            self.telegram_bot.sendMessage(chat_id = self.user_chat_id,
                                          text = message)

    def notify_tramite_movement(self, movement):
        message = """
        ¡Nuevo movimiento del trámite!
        Id: {}
        Fecha: {}
        Comentario: {}
        """.format(movement.external_id, movement.datetime, movement.comment)
        self.notify(textwrap.dedent(message))
