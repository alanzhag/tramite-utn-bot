#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 17:36:11 2019

@author: alanzhao
"""

import requests
import json
import tramite_notifier as tn
from os import environ, path
from operator import attrgetter
from lxml import html

import datetime

DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"

def convert_string_to_datetime(date_time_str):
    return datetime.datetime.strptime(date_time_str, DATETIME_FORMAT)

def convert_datetime_to_string(datetime):
    return datetime.strftime(DATETIME_FORMAT)

def sublist_in_even_chunks(list_to_sublist, chunk_lenght):
    return [list_to_sublist[i:i + chunk_lenght] for i in range(0, len(list_to_sublist), chunk_lenght)]

def transform_movement(movement):
    raw_date = movement[1].replace("- ", "").strip()
    return TramiteMovement(external_id = int(movement[0].replace("# ", "")), 
                           datetime = convert_string_to_datetime(raw_date),
                           comment = movement[2].encode("utf-8"),
                           raw_datetime = raw_date)

class TramiteMovement:
    DATETIME = "datetime"
    
    def __init__(self, external_id, datetime, comment, raw_datetime):
        self.external_id = external_id
        self.datetime = datetime
        self.comment = comment
        self.raw_datetime = raw_datetime
    
    def __str__(self):
        pretty = "external_id: {}, datetime: {}, comment: {}"
        return pretty.format(self.external_id, self.datetime, self.comment)

class TramiteChecker:
    
    LAST_MOVEMENT_DATETIME = "last_movement_datetime"
    
    def __init__(self, xt_code, xt_key):
        self.xt_code = str(xt_code)
        self.xt_key = str(xt_key)
        self.persistence_file_path = self.buid_current_path("persistence.json")
        self.session = requests.Session()
        self.persistence = self.load_persistence()
        self.notifier = tn.TelegramNotifier()
        self.authenticate()
        
    def authenticate(self):
        data = {
                'form_email': '',
                'form_pwd': '',
                'form_cod': self.xt_code,
                'form_key': self.xt_key,
                'form_submit': '2'
                }
        self.session.post('http://xt.frba.utn.edu.ar/pub/login.do', data=data)
    
    def get_movements(self):
        data = {
                'form_idtr': self.xt_code
                }
        response = self.session.post('http://xt.frba.utn.edu.ar/pub/tramite.do', 
                                 data=data)
        tree = html.fromstring(response.content)
        movement_columns = tree.xpath("//div[@class='app-cita']/span/text()")
        chunked_movements = sublist_in_even_chunks(movement_columns, 3)
        return [transform_movement(movement) for movement in chunked_movements]
    
    def check_for_new_movements(self):
        movements = self.get_movements()
        if self.has_new_movement(movements):
            last_movement = self.get_last_movement(movements)
            self.notify_user_of_new_movement(last_movement)
            self.update_last_known_movement_id(last_movement.datetime)
        else:
            self.notifier.notify("No updates", muteable = True)
            
    def update_last_known_movement_id(self, new_id):
        self.persistence[self.LAST_MOVEMENT_DATETIME] = convert_datetime_to_string(new_id)
        self.save_persistence()
    
    def notify_user_of_new_movement(self, movement):
        self.notifier.notify_tramite_movement(movement)
            
    def get_last_movement(self, movements):
        return max(movements, key=attrgetter(TramiteMovement.DATETIME))
    
    def has_new_movement(self, movements):
        last_known_movement_id = self.last_known_movement_id()
        return any(movement.datetime > last_known_movement_id
                               for movement in movements)
    def load_persistence(self):
        with open(self.persistence_file_path,"r") as persistence:
            return json.load(persistence)
        
    def save_persistence(self):
        with open(self.persistence_file_path, "w") as persistence:
            json.dump(self.persistence, persistence)
        
    def last_known_movement_id(self):
        raw_date = self.persistence[self.LAST_MOVEMENT_DATETIME]
        return convert_string_to_datetime(raw_date)
    
    def buid_current_path(self, filename):
        return path.join(path.dirname(__file__), filename)

if __name__ == "__main__":
    xt_code = environ["XT_CODE"]
    xt_key = environ["XT_KEY"]
    tramite_checker = TramiteChecker(xt_code, xt_key)
    tramite_checker.check_for_new_movements()
