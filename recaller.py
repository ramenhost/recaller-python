#!/usr/local/bin/python3
import GoogleManager
import json
import way2sms

google_manager = GoogleManager.GoogleManager()
today_events = google_manager.build_today_events()
tomo_events = google_manager.build_tomo_events()
with open('./sms-config.json') as sms_config_file:
    sms_config = json.load(sms_config_file)
q = way2sms.sms(sms_config['username'], sms_config['password'])
with open('./contacts.txt') as contacts:
    for contact in contacts.readlines():
        q.send(contact, today_events)
        q.send(contact, tomo_events)
q.logout()
