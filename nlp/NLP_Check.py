import NLP
import time

s=time.time()

data = open('data.txt','r',encoding='utf8')
query=data.readline().strip()
entity=('When : ', 'Where : ' ,'Whom : ', 'What : ', 'Action : ' )
while (query):
    #print(query)
    [print(entity[i], result)  for i, result in enumerate (NLP.understand(query)) ]
    print("#---------------------------------#")
    query = data.readline().strip()



e=time.time()
print(e-s , '초')
'''
list1 = ['오월삼일열시오십이분친구와밥약속추가해줘',
         '1월 일일 열한시 밥약속 있어? ',
         '이번 화요일 밥약속 추가',
         '이번주 목요일 다섯시 11시 밥약속 추가',
         '삼월칠일 목요일 열한시 밥약속 추가 ',
         '이번주 금요일 정보통신세미나 약속',
         '다음주 금요일 정보통신세미나 약속',
         '10월 21일 7시 이십구분 건희와 밥약속 취소해줘',
         '9월 3일1시23분  오랑캐와 전쟁약속',
         '진호를 친한친구로 등록',
         '내일 모레 7시 진호 시간되는지 알려줘',
         '이번주 일요일 밥약속 추가해줘',
         '다음주 월요일 시험 추가']






'''
