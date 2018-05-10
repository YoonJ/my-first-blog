import datetime
import sys


class When( ):
    timeInfo= datetime.datetime.now()
    Year = int(timeInfo.year)
    Month = int(timeInfo.month)
    Day = int(timeInfo.day)
    Day_original = int(timeInfo.day)
    Weekday = datetime.datetime.today().weekday()       # int Monday=0 ~
    Oclock = 0      # int(timeinfo.hour)
    Min = 0         # int(timeinfo.minute)
    PM= True

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
            if time < 12:
                self.Oclock += time +12
            else:
                self.Oclock += time
            self.detected = True
        elif unit == '분':
            self.Min = time
            self.detected = True

    def next_week_detected(self):
        self.isNextweek = 7
        self.isThisweek = False
        self.From_Day = self.Day - self.Weekday +7 # +8 ???
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

    def to_string(self):
        ret_string = str(self.Year) + '-'
        if self.Month < 10:
            ret_string += '0'
        ret_string += str(self.Month) + '-'
        if self.Day < 10:
            ret_string += '0'
        ret_string += str(self.Day) + 'T'
        if self.Oclock < 10:
            ret_string += '0'
        ret_string += str(self.Oclock) + ':'
        if self.Min < 10:
            ret_string += '0'
        ret_string += str(self.Min) + ':00'

        return ret_string

    def __str__(self):
        if self.detected:
            return "%2d월 %2d일 %2d시 %2d분"% (self.Month ,self.Day, self.Oclock , self.Min)

        elif self.isNextweek or self.isThisweek:
            return "%2d월 %2d일 %2d시 %2d분"% (self.Month ,self.From_Day, self.Oclock , self.Min) + " ~ " + "%2d월 %2d일 %2d시 %2d분"% (self.Month ,self.To_Day, self.Oclock , self.Min)
        else:
            return "시간 정보 없음"


def convert_to_int(char):
    kor_num_list = ['zero', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구']
    try:
        time = kor_num_list.index(char)
        return time
    except ValueError as V:
        try:
            kor_num_list = ['zero', '한', '두', '세', '네', '다섯', '여섯', '일곱', '여덟', '아홉', '열', '열한', '열두']
            time = kor_num_list.index(char)
            return time
        except ValueError as V:
            return False


def extract_time(word):
    try:
        unit = word[-1]
        time = word[:-1]
        if (unit == '월' or unit == '일' or unit == '분') and len(word) > 1:  # 월, 일 ,분
            temp = time.split('십')
            if len(temp) == 1:      # == 1 ~ 9
                time = convert_to_int(temp[0])
                return time, unit

            elif temp[0] == '' and temp[0] == '':    # == 10
                return 10, unit

            else:        # == 11 ~ 99
                ten = convert_to_int(temp[0])
                one = convert_to_int(temp[1])
                return ten*10 + one, unit

        elif unit == '시' and len(word) > 1:   # 시
            time = convert_to_int(time)
            return time, '시'

        else:
            return 0, 0

    except:
        e = sys.exc_info()[0]
        print(e)
        return 0, 0


def get_when(twit, checklist):
    # 3일 뒤 1주일 후 구현 안됨
    # 월을 넘어갈 때 기능 구현(3월34일 = 4월 3일) 구현 안됨
    # 오전 오후 구현 됨
    # 아침, 점심, 저녁 구현 됨

    #  요일의 경우 '요일'꼭 붙여야 함 / 내일.모레 구현완료 / 이번주, 다음주 시간범위 측정가능 /
    time_class = When()
    for i in range(len(twit)):
        if not checklist[i]:
            corpus = twit[i]
            word = corpus[0]
            pos = corpus[1]
            if word == '다음주':       # 다음주
                time_class.next_week_detected()
                checklist[i] = 1

            elif word=='다음' and twit[i+1][0] == '주':     # 다음주
                time_class.next_week_detected()
                checklist[i] = 1
                checklist[i+1] = 1

            elif word == '이번주': # 이번주
                time_class.this_week_detected()
                checklist[i] = 1

            elif word=='이번' and twit[i+1][0] == '주':    # 이번주
                time_class.this_week_detected()
                checklist[i] = 1
                checklist[i + 1] = 1

            elif word[1:] == '요일':      # 요일 디텍션
                weekday = word[0]
                time_class.update_by_weekday(weekday)
                checklist[i] = 1

            elif word == '오늘':
                time_class.update(time_class.Day_original, '일')
                checklist[i] = 1
            elif word == '내일':
                time_class.update(time_class.Day_original+1, '일')
                checklist[i] = 1
            elif word == '모레':
                time_class.update(time_class.Day_original + 2, '일')
                checklist[i] = 1
            elif pos == 'Number':
                time = word
                unit = twit[i+1][0]
                time_class.update(int(time), unit[0])     # '시밥' 이 출력되는 경우도 있어 맨 앞글자만 추가
                checklist[i] = 1
                checklist[i + 1] = 1

            elif word == '오전' or word == '아침'or word == '새벽':
                time_class.update(-12, '시')
                checklist[i] = 1

            elif word == '오후' or  word == '저녁':

                checklist[i] = 1


            else:
                time , unit = extract_time(word)
                if time:
                    time_class.update(int(time), unit[0])
                    checklist[i] = 1

    return time_class
