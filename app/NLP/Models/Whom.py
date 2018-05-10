def getFriends(ID): # depends on database....
    return {'진호', '영희', '철수','건희','승주'}


def getGroup(ID):
    return{'종설프', '인공지능세미나', '독서동아리'}


def get_whom(twit, checklist):
    friends = getFriends(1234)
    result = []
    for i in range(len(twit)):
        word, pos = twit[i] #
        if word in friends:
            result.append(word)
            checklist[i] = 3
        elif pos == 'Josa' and (word == '랑' or word == '이랑' or word == '와' or word == '이와'):
            result.append(twit[i-1][0])
            checklist[i-1] = 3
            checklist[i] = 3
    return list(set(result))