'''Google Module'''
import os.path
import time
import json
import requests
import httplib2
from googleapiclient.discovery import build
from oauth2client.client import AccessTokenCredentials
from datetime import datetime, timezone, timedelta

class GoogleAuthManager(object):
    '''Authentication Manager for Google OAuth2.0'''
    TOKEN_FILE = './google-token.json'

    def __init__(self):
        if not os.path.exists(self.TOKEN_FILE):
            with open('./client_id.json') as client_file:
                client_data = json.load(client_file)
            post_data = {'client_id':client_data['installed']['client_id'], 'scope':'https://www.googleapis.com/auth/calendar.readonly'}
            res = requests.post('https://accounts.google.com/o/oauth2/device/code', data=post_data)
            res = json.loads(res.text)
            print('You are not logged in to the device. Visit', end=' ')
            print(res['verification_url'])
            print('Enter', end=' ')
            print(res['user_code'], end=' ')
            print('to log in')
            interval = res['interval']
            time.sleep(interval)
            post_data = {'client_id':client_data['installed']['client_id'], 'client_secret':client_data['installed']['client_secret'], 'code':res['device_code'], 'grant_type':'http://oauth.net/grant_type/device/1.0'}
            res = requests.post('https://www.googleapis.com/oauth2/v4/token', data=post_data)
            while not res.status_code == requests.codes.ok:
                time.sleep(interval)
                res = requests.post('https://www.googleapis.com/oauth2/v4/token', data=post_data)
            print('signin success')
            with open(self.TOKEN_FILE, mode='w') as google_file:
                json.dump(json.loads(res.text), google_file)
        self.validate_token()
    
    def validate_token(self):
        with open(self.TOKEN_FILE, mode='r') as token_file:
            token = json.load(token_file)
        post_data = {'access_token':token['access_token']}
        res = requests.post('https://www.googleapis.com/oauth2/v3/tokeninfo', data=post_data)
        res_text = json.loads(res.text)
        if res.status_code == 400:
                self.refresh_token()

    def refresh_token(self):
        with open('./client_id.json') as client_file:
            client_data = json.load(client_file)
        with open(self.TOKEN_FILE, mode='r') as token_file:
            token = json.load(token_file)
        post_data = {'client_id':client_data['installed']['client_id'], 'client_secret':client_data['installed']['client_secret'], 'refresh_token':token['refresh_token'], 'grant_type':'refresh_token'}
        res = requests.post('https://www.googleapis.com/oauth2/v4/token', data=post_data)
        res = json.loads(res.text)
        token['access_token'] = res['access_token']
        token['expires_in'] = res['expires_in']
        token['token_type'] = res['token_type']
        with open(self.TOKEN_FILE, mode='w') as token_file:
            json.dump(token, token_file)

    def get_access_token(self):
        with open(self.TOKEN_FILE, mode='r') as token_file:
            token = json.load(token_file)
        return token['access_token']

class GoogleManager():
    '''Class to handle Google calendar'''

    def __init__(self):
        google_auth_manager = GoogleAuthManager()
        user_agent = 'python-recaller/1.0'
        credentials = AccessTokenCredentials(google_auth_manager.get_access_token(), user_agent)
        http = httplib2.Http()
        http = credentials.authorize(http)
        self.service = build('calendar', 'v3', http=http)

    def build_today_events(self):
        today_events = ''
        counter = 1
        page_token = None
        now = datetime.now()
        today = datetime(now.year, now.month, now.day, 0, 0, 0, 0).isoformat() + '+05:30'
        tomo = datetime(now.year, now.month, now.day+1, 0, 0, 0, 0).isoformat() + '+05:30'
        with open('./calendars.json') as calendars:
            calendar_list = json.load(calendars)
        for calendar in calendar_list:
            today_events = today_events + calendar['type'] + ' today\n'
            while True:
                events = self.service.events().list(calendarId=calendar['calendarId'], pageToken=page_token, timeMax=tomo, timeMin=today).execute()
                for event in events['items']:
                    today_events += str(counter)
                    today_events += '.'
                    counter += 1
                    today_events += event['summary']
                    today_events += '\n'
                    if 'description' in event:
                        today_events += event['description']
                        today_events += '\n'
                page_token = events.get('nextPageToken')
                if not page_token:
                    break
            page_token = None
        return today_events

    def build_tomo_events(self):
        tomo_events = ''
        counter = 1
        page_token = None
        now = datetime.now()
        today = datetime(now.year, now.month, now.day+1, 0, 0, 0, 0).isoformat() + '+05:30'
        tomo = datetime(now.year, now.month, now.day+2, 0, 0, 0, 0).isoformat() + '+05:30'
        with open('./calendars.json') as calendars:
            calendar_list = json.load(calendars)
        for calendar in calendar_list:
            tomo_events = tomo_events + calendar['type'] + ' tomorrow\n'
            while True:
                events = self.service.events().list(calendarId=calendar['calendarId'], pageToken=page_token, timeMax=tomo, timeMin=today).execute()
                for event in events['items']:
                    tomo_events += str(counter)
                    tomo_events += '.'
                    counter += 1
                    tomo_events += event['summary']
                    tomo_events += '\n'
                    if 'description' in event:
                        tomo_events += event['description']
                        tomo_events += '\n'
                page_token = events.get('nextPageToken')
                if not page_token:
                    break
            page_token = None
        return tomo_events