"""
Shows basic usage of the Google Calendar API. Creates a Google Calendar API
service object and outputs a list of the next 10 events on the user's calendar.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
import calendar

# 필요한 파일: credentials.json, client_secret.json


def get_upcoming_event():
    # Setup the Calendar API
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    #print(now) # format 2018-04-20T11:56:43.

    #print('Getting the upcoming event')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=1, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
     #   print(start)
     #   print(event['summary'])

    year = start[:4]
    month = start[5:7]
    day = start[8:10]
    time = start[12:16]
    msg = "다가오는 최근 일정은 "
    msg += year + "년 " + month + "월 " + day + "일 " + time + "에 " + event['summary'] + "입니다."
    #print(msg)

    return msg


def get_event(time):
    # Setup the Calendar API
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    #print(now) # format 2018-04-20T11:56:43.

    #print('Getting the upcoming event')
    events_result = service.events().list(calendarId='primary', timeMin=time,
                                          maxResults=1, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
     #   print(start)
     #   print(event['summary'])

    year = start[:4]
    month = start[5:7]
    day = start[8:10]
    time = start[12:16]
    msg = "다가오는 최근 일정은 "
    msg += year + "년 " + month + "월 " + day + "일 " + time + "에 " + event['summary'] + "입니다."
    #print(msg)

    return msg


def register_event(name, time):
    # Setup the Calendar API
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    # 여기에서 받은 parameter에 대해서 event를 알아서 조정해주면 된다.

    event = {
        'summary': name, # 일정 이름
        'location': '', # 일정 장소
        'description': '', # 일정 설명
        'start': { # 시작 시간
            'dateTime': time, # '2015-05-28T09:00:00-07:00' 이런 format으로
            'timeZone': 'Asia/Seoul',
        },
        'end': { # 끝나는 시간
            'dateTime': time,
            'timeZone': 'Asia/Seoul',
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=2'
        ],
        'attendees': [ # 만약에 grouping을 사용할 때 구성원들의 이메일을 적어주면 좋을 듯
            {'email': 'lpage@example.com'},
            {'email': 'sbrin@example.com'},
        ],
        'reminders': { # reminder, 이메일로 일정 전날에 알려줄지 + 팝업으로 몇 분 전에 알려줄지
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print ('Event created: %s' % (event.get('htmlLink')))


    return





msg = get_upcoming_event()
name = 'test'
datetime = '2018-05-01T09:00:00+09:00'
register_event(name=name, time='2018-05-01T09:00:00+09:00')

print(msg)



