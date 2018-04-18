from konlpy.tag import Twitter
from konlpy.tag import Komoran
from konlpy.tag import Kkma
from requests import put
import sys


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


def conver_to_int(char):
    numlist = ['zero', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구']
    for i in numlist:
        if i == char:
            time = numlist.index(i)
            return time

    numlist = ['zero', '한', '두', '세', '네', '다섯', '여섯', '일곱', '여덟', '아홉', '열', '열한', '열두']
    for i in numlist:
        if i == char:
            time = numlist.index(i)
            return time

    return False

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

class When():
    Month = None
    Day = None
    Oclock =None
    Min = None
    From = None
    To = None
    def update(self,time,unit):
        if unit == '월':
            self.Month = time
        elif unit == '일':
            self.Day = time
        elif unit == '일':
            self.Day = time


def getWhen(sentence):
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

def Action(twit): # 진행중
    action = []
    for corpus in twit:
        word = corpus[0]
        if word in  {'?', '확인', '알다', '가능하다'}:
            action.append ( ('정보확인', word) )
            return action

    return('정보수정')




def understand(sentence):
    when = getWhen(sentence) #내일. 모레, 3일 뒤 1주일 뒤, 요일 구현 X

    twit = Twitter().pos(sentence, norm=True, stem=1)
    action = Action(twit)


    if len(when) >0 : # 시간 정보가 있으면 일정관련명령
        pass

    else: # 시간 정보가 없으면 보안 관련 명령
        pass


    whom = [ ]
    where = [ ]
    what = [ ]

    #kkma = Kkma().pos(sentence, flatten=1)
    #print(kkma)

    print(when, action)

list1 = ['오월삼일열시오십이분친구와밥약속추가해줘',
         '1월 일일 열한시 밥약속 있어? ',
         '이월 삼일 세시 밥약속 추가',
         '구월 칠일 다섯시 11시 밥약속 추가',
         '삼일 정보통신세미나 약속',
         '10월 21일 7시 23분 건희와 밥약속 취소해줘',
         '9월 3일1시23분  오랑캐와 전쟁약속',
         '진호를 친한친구로 등록',
         '3일 7시 진호 시간되는지 알려줘']

for k in list1:
    understand(k)
    #print(getWhen(k))

    '''

        #whom
        if pos == "Josa" and ( ('랑' in value)  or ('와' in value ) ) and twit[k-1][1]=='Noun':  # 접속 조사 ~와 .. 사과와 배를 먹었다.
            #print(value)
            whom.add(twit[k - 1][0])

        #where
        if (pos == 'Josa') and  ('서' in value) :  # 부사격 조사
            #print(1)
            where.add(twit[k - 1][0])

        if action == 'Check':
            pass
        else:
            if value in {'?', '확인', '알다', '가능하다', '있다'}:
                action = 'Check'
            else: action = 'Edit'




    ### Kkma

    for  k in range ( len(kkma) ):
        value = kkma[k][0]
        pos = kkma[k][1]

        # when
        if pos == 'NNM': #단위 의존명사
            if kkma[k+1][1] == 'NNG ' and  (kkma[k+1][0] == '뒤' or kkma[k+1][0] == '후' ) :
                print(11111)
                plus = value
                when[value] = (when[value], plus)

            else:

                when[value] = kkma[k-1][0]

        #whom
        if pos == "JC" : #접속 조사 ~와 .. 사과와 배를 먹었다.
            whom.add (kkma[k-1][0])


    month = when.get('월',4)
    day = when.get('일', '오늘')
    hour = when.get('시', None)
    min = when.get('분', None)
    where = list(where)
    whom = list(whom)
    what = list(what)
    

    print(month,'월\t', day, '일 \t', hour,'시 \t', min, '분 \t', where, '에서 \t',  whom, '와 함께 \t', what,'이것을 \t' ,action, '수행할 것')
    #print(month , 'When :', when, ' \tWhom : ', whom, ' \tWhere : ' , where, ' \tAction : ' ,action)
    '''






