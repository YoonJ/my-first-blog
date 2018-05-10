from konlpy.tag import Twitter
from app.NLP.Models import When, Action, Where, Whom, What
from app.Google import upcoming
import time


def understand(sentence):
    print(sentence)
    sentence = sentence.strip()
    twitter = Twitter().pos(sentence, norm=True, stem=True)

    check_list = [False for i in range(len(twitter))]
    when = When.get_when(twitter, check_list)
    whom = Whom.get_whom(twitter, check_list)
    where = Where.get_where(twitter,check_list)
    _, action, action_command = Action.get_action(twitter, check_list)
    what, what_str = What.get_what(twitter, check_list)
    #isSchedule= 1 # 스케줄 일정인가 보안 정보인가

    if action_command is 1:
        print(when.to_string(), what_str)
        startAt = when.to_string()
        when.Oclock += 1
        endAt = when.to_string()
        event = {
            'summary': what_str,  # 일정 이름
            'location': '',  # 일정 장소
            'description': '',  # 일정 설명
            'start': {  # 시작 시간
                'dateTime': startAt,  # '2015-05-28T09:00:00-07:00' 이런 format으로
                'timeZone': 'Asia/Seoul',
            },
            'end': {  # 끝나는 시간
                'dateTime': endAt,
                'timeZone': 'Asia/Seoul',
            },
            'attendees': [  # 만약에 grouping을 사용할 때 구성원들의 이메일을 적어주면 좋을 듯
                {'email': 'lpage@example.com'},
                {'email': 'sbrin@example.com'},
            ],
            'reminders': {  # reminder, 이메일로 일정 전날에 알려줄지 + 팝업으로 몇 분 전에 알려줄지
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        upcoming.register_event2(event)
        # upcoming.get_upcoming_event()

    return when, where, whom, what, action


s = time.time()

data = open('data2.txt','r',encoding='utf8')
query=data.readline().strip()
entity=('When : ', 'Where : ' ,'Whom : ', 'What : ', 'Action : ' )
while (query):
    #print(query)
    [print(entity[i], result)  for i, result in enumerate (understand(query)) ]
    print("#---------------------------------#")
    query = data.readline().strip()



e=time.time()
print(e-s , '초')
