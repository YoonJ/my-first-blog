def get_action(twit, checklist): # 진행중
    # 보안이든 일정이든 추가,삭제,수정,조회하는 건 똑같으니
    # 첫 단계에서 < 정보조회/수정> 을 나누고 그 후 <보안/일정> 을 파악하는 게 어떤지

    action_list = []
    add = False
    security = '일정정보'
    action_command = -1

    for i in range(len(twit)):
        word, pos = twit[i]

        # 정보확인에 관한 문장인 경우
        if word in {'확인', '알다', '가능하다', '되다', '돼다', '야','언제','시간', '?'}:
            checklist[i] = 'check'
            if pos == 'Noun' and i + 1 < len(twit):
                checklist[i + 1] = 2
            add = True
            action_list.append(('정보확인', word))
            break

        # 정보수정에 문장인 경우
        else:
            if word in {'추가', '등록'}: # 있다 제거 함
                checklist[i] = 'edit'
                if pos == 'Noun' and i + 1 < len(twit):
                    checklist[i + 1] = 2
                add = True
                action_list.append(('정보추가', word))
                action_command = 1
                break

            elif word in {'변경', '수정', '바꾸다'}:
                checklist[i] = 'edit'
                if pos == 'Noun' and i + 1 < len(twit):
                    checklist[i + 1] = 'edit'
                add = True
                action_list.append( ('정보수정', word))
                break

            elif word in {'삭제', '지우다', '없애다', '없다', '취소'}:
                checklist[i] = 'edit'
                if pos == 'Noun' and i+1 < len(twit):
                    checklist[i+1] = 'edit'
                add = True
                action_list.append(('정보삭제', word))
                break
    # 보안에 관한 문장
    for i in range(len(twit)):
        word, pos = twit[i]
        if word in {'친구', '친한친구', '그룹', '친한'}:
            checklist[i] = 'security'
            security = '보안정보'
            break

    # 디폴트로  정보추가
    if add is False:
        action_list.append('정보추가')
        action_command = 1

    return security, action_list, action_command