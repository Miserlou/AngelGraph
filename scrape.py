#!/usr/bin/env python

from peewee import *
from model import AngelEvent
import datetime
import urllib2
import json
import pprint

DATABASE = 'angels.db'
database = SqliteDatabase(DATABASE)
API = 'http://api.angel.co/1/feed'

def p_print(data):
    pprint.pprint(data)

def setup_db():
    database.connect()
    try:
        AngelEvent.create_table() #only needed once
    except Exception, e:
        return

def scrape():
    data = json.load(urllib2.urlopen(API))

    for event in data['feed']:
        try:
            if event['actor']['type'] != 'User':
                continue

            if event['item']['type'] not in ['Comment', 'StartupIntro', 'Follow']:
                continue

            if event_in_db(event['id']):
                continue
        except Exception, e:
            continue

        add_event(event)

def event_in_db(id):
    try:
        AngelEvent.get(AngelEvent.al_id == id)
        return True
    except Exception, e:
        return False

def add_event(event):
    if event['target']:
        target = event['target']['angellist_url']
    else:
        target = "No target"

    e = AngelEvent.create(  al_id   = event['id'],
                        event_type  = event['item']['type'], 
                        username    = event['actor']['angellist_url'],
                        target      = target,
                        datetime    = event['timestamp']
                    )
    return e

def get_all_events():
    for event in AngelEvent.select():
        print event.username[17:] + " " + event.event_type.lower() + "ed " + event.target[17:] + "at " + event.datetime

setup_db()
scrape()
get_all_events()
