from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

def keyboard(request):

    return JsonResponse(
        {
            'type':'text'
        }
    )

@csrf_exempt
def message(request):
    #request를 한글호환이 되는 'utf-8'로 바뚜어 json_str변수에 저장
    json_str = ((request.body).decode('utf-8'))
    #JSON문자열로 되어 있는 것을 Python 타입으로 변경시켜 received_json변수에 저장
    if(json_str == ''):

        return JsonResponse(
            {
                'message': {
                    'text': 'None'
                },
                'keyboard': {
                    'type': 'text'
                }
            })

    json_data = json.loads(json_str)
    #사용자가 보낸 명령어에서 필드명이 content인 변수에 저장
    data = json_data['content']

    #request_mode = data.encode('utf-8')

    if data == '일정':
        return JsonResponse(
        {
            'message':{
                'text': '일정을 말했습니다.'
            },
            'keyboard':{
                'type':'text'
            }
        }
    )
    elif data == '공유':
        return JsonResponse(
        {
            'message':{
                'text': '공유를 말했습니다.'
            },
            'keyboard':{
                'type':'text'
            }
        }
    )
    else:
        return JsonResponse(
            {
                'message': {
                    'text': 'Nothing'
                },
                'keyboard': {
                    'type': 'text'
                }
            }
        )