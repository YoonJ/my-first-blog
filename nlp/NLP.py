from konlpy.tag import Twitter
from konlpy.tag import Komoran
from konlpy.tag import Kkma
import sys
import time
import datetime
s = time.time()

if  0:

    for tag in [ Twitter, Kkma] : #Komoran
        nlp = tag()
        for sentence in list1:

           # nlp = Twitter()  # Twitter 라이브러리 사용
            if tag == Twitter:
                result = nlp.pos(sentence, norm=True, stem=1)
            else:
                result = nlp.pos(sentence, flatten=1)

            for phrase in result:
                if 'J' in phrase[-1]:
                    print(phrase[0], '(', phrase[1],')' , end = ' \t')
                else:
                    print(phrase[0] ,'(', phrase[1],')',  end  = ' ')

            print()
        print( '\n')


class When():
    timeinfo= datetime.datetime.now()
    Year = int(timeinfo.year)
    Month = int(timeinfo.month)
    Day = int(timeinfo.day)
    Day_original = int(timeinfo.day)
    Weekday = datetime.datetime.today().weekday() # int Monday=0 ~
    Oclock = int(timeinfo.hour)
    Min = int(timeinfo.minute)

    From_Day = None

    To_Year = None # ~ 까지
    To_Month = None
    To_Day = None
    To_Weekday = None
    To_Oclock = None
    To_Min = None

    isNextweek = 0
    isThisweek = False
    detected = False


    def update(self,time,unit):
        if unit == '월':
            self.Month = time
            self.detected = True
        elif unit == '일':
            self.Day = time
            self.detected = True
        elif unit == '시':
            self.Oclock = time
            self.detected = True
        elif unit == '분':
            self.Min = time
            self.detected = True


    def next_week_detected(self):
        self.isNextweek = 7
        self.isThisweek = False
        self.From_Day = self.Day - self.Weekday +7
        self.To_Day = self.Day + 6 - self.Weekday +7

    def this_week_detected(self):
        self.isNextweek = 0
        self.isThisweek = True
        self.From_Day = self.Day - self.Weekday
        self.To_Day = self.Day + 6 - self.Weekday


    def update_by_weekday(self, weekday):
        weeklist = ['월', '화', '수', '목', '금', '토', '일']
        try:
            input_Weekday = weeklist.index(weekday) + self.isNextweek
            offset = input_Weekday - self.Weekday
            self.update(self.Day_original + offset, '일')

        except ValueError as V:
            return False

    def __str__(self):
        if self.detected:
            return "%2d월 %2d일 %2d시 %2d분"% (self.Month ,self.Day, self.Oclock , self.Min)

        elif self.isNextweek or self.isThisweek:
            return "%2d월 %2d일 %2d시 %2d분"% (self.Month ,self.From_Day, self.Oclock , self.Min) + " ~ " + "%2d월 %2d일 %2d시 %2d분"% (self.Month ,self.To_Day, self.Oclock , self.Min)
        else:
            return "보안 관련 정보로 추정됨"

def conver_to_int(char):
    numlist = ['zero', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구']
    try:
        time = numlist.index(char)
        return time
    except ValueError as V :

        try:
            numlist = ['zero', '한', '두', '세', '네', '다섯', '여섯', '일곱', '여덟', '아홉', '열', '열한', '열두']
            time = numlist.index(char)
            return time
        except ValueError as V:
            return False


    ''' 
        
    for i in numlist:
        if i == char:
            time = numlist.index(i)
            return time

    numlist = ['zero', '한', '두', '세', '네', '다섯', '여섯', '일곱', '여덟', '아홉', '열', '열한', '열두']
    for i in numlist:
        if i == char:
            time = numlist.index(i)
            return time
    '''

def extract_time(word):
    try:
        unit = word[-1]
        time = word[:-1]
        if (unit == '월' or unit == '일' or unit =='분') and len(word) > 1:  # 월, 일 ,분
            temp = time.split('십')
            if len(temp) == 1: # == 1 ~ 9
                time = conver_to_int(temp[0])
                return time, unit

            elif temp[0] == '' and temp[0] == '': # == 10
                return 10, unit

            else: # == 11 ~ 99
                ten = conver_to_int(temp[0])
                one = conver_to_int(temp[1])
                return ten*10 + one, unit


        elif unit =='시' and len(word) >1 : # 시
            time = conver_to_int(time)
            return time, '시'

        else:
            return 0,0

    except:
        e = sys.exc_info()[0]
        print(e)
        return 0,0



def getWhen(twit): # 3일 뒤 1주일 후 / 요일의 경우 '요일'꼭 붙여야 함 / 내일.모레 구현완료 / 이번주, 다음주 시간범위 측정가능 / 월을 넘어갈 때 기능 구현(3월34일 = 4월 3일)

    #print(twit)
    timeclass = When()
    for i in range(len(twit)):
        corpus = twit[i]
        word = corpus[0]
        pos = corpus[1]
        if word == '다음주' or (word=='다음' and twit[i+1][0] == '주'): # 다음주
            timeclass.next_week_detected()

        elif word == '이번주' or (word=='이번' and twit[i+1][0] == '주'): # 이번주
            timeclass.this_week_detected()

        elif word[1:] == '요일': # 요일 디텍션
            weekday = word[0]
            timeclass.update_by_weekday(weekday)

        elif word == '오늘':
            timeclass.update(timeclass.Day_original, '일')
        elif word == '내일':
            timeclass.update(timeclass.Day_original+1, '일')
        elif word == '모레':
            timeclass.update(timeclass.Day_original + 2, '일')
        elif pos == 'Number':
            time = word
            unit = twit[i+1][0]
            timeclass.update(int(time), unit[0]) # '시밥' 이 출력되는 경우도 있어 맨 앞글자만 추가

        else:
            time , unit = extract_time(word)
            if time:
                timeclass.update(int(time), unit[0])

    return timeclass


def Action(twit): # 진행중
    action = [ ]
    for corpus in twit:
        word = corpus[0]
        if word in {'추가', '등록', '있다' }:
            action.append( ('일정등록', word) )
        elif word in {'변경', '수정', '바꾸다'}:
            action.append( ('일정변경', word))
        elif word in {'삭제', '지우다'}:
            action.append(('일정삭제', word))
        elif word in  {'?', '확인', '알다', '가능하다'}:
            action.append ( ('정보확인', word) )
    return action

def getWhere(twit):
    result = [ ]
    for t in range(len(twit)):
        word, pos =  twit[t]
        if  pos == 'Josa' and ( word =='에서' or word =='서'):
            result.append(twit[t-1][0])

    return result


def getFriends(ID): # depends on database....
    return {'진호', '영희', '철수'}

def getWhom(twit):
    friends = getFriends(1234)
    result = []
    for i in range(len(twit)):
        word, pos = twit[i] #
        if word in friends:
            result.append(word)
        elif pos == 'Josa' and (word =='랑' or word =='이랑' or word =='와' or word =='이와'):
            result.append(twit[i-1][0])
    return result

class TwitterClass: # sublcass로 when... 등 만들어서 infodetected가 0 인 곳만 고려해서 뽑기. 나머지는 기타로 빼서 출력
    def __init__(self, twit):
        self.twit = twit
        self.is_info_detected = [0 for t in twit] # [0,0,0,0,0] 으로 초기화, 각 twit의 인덱스가 시간,엑션 등등으로 판명되었으면 1

def understand(sentence):
    #print("\n", sentence)
    sentence = sentence.strip()
    twitter = Twitter().pos(sentence, norm=True, stem=True)
    #twitter = TwitterClass(twitter)
    when = getWhen(twitter)
    action = Action(twitter)
    whom = getWhom(twitter)
    where = getWhere(twitter)
    what = [ ]
    #isSchedule= 1 # 스케줄 일정인가 보안 정보인가

    return when, where, whom, what, action




def getWhen_oldver(sentence):
    sentence = sentence.replace(' ','') # 띄어쓰기 없이 다 붙임
    twit = Twitter().pos(sentence, norm=True, stem=1) #트윗으로 분석하면 어찌됐건 시간은 잘 나눠짐
    print(twit)
    timelist=[ ]
    for i in range(len(twit)):
        corpus = twit[i]
        word = corpus[0]
        pos = corpus[1]

        if pos == 'Number':
            time = word
            unit = twit[i+1][0]
            timelist.append((time, unit[0])) # '시밥' 이 출력되는 경우도 있어 맨 앞글자만 추가

        else:
            time , unit = extract_time(word)
            if time:
                timelist.append((time, unit[0]))

    return timelist
def Action_oldver(twit): # 진행중
    action = [ ]
    for corpus in twit:
        word = corpus[0]
        if word in  {'?', '확인', '알다', '가능하다'}:
            action.append ( ('정보확인', word) )
            return action

    return('정보수정')
