def get_where(twit, checklist):
    result = []
    for t in range(len(twit)):
        if not checklist[t]:
            word, pos = twit[t]
            if pos == 'Josa' and (word == '에서' or word == '서'):
                result.append(twit[t - 1][0])
                checklist[t] = 4
                checklist[t - 1] = 4

    return result