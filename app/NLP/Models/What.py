def get_what(twit, checklist):
    what_list = []
    ret_str = ''
    for i in range(len(twit)):
        if not checklist[i]:
            word, pos = twit[i]
            if pos == 'Noun':
                ret_str += twit[i][0]
                what_list.append(twit[i][0])

    return what_list, ret_str
