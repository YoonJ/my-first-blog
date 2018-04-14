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
    json_str = (request.body).decode('uft-8')
    #JSON문자열로 되어 있는 것을 Python 타입으로 변경시켜 received_json변수에 저장
    received_json = json.loads(json_str)
    #사용자가 보낸 명령어에서 필드명이 content인 변수에 저장
    content_name = received_json['content']

    if content_name == '일정':
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
    elif content_name == '공유':
        return JsonResponse(
        {
            'message':{
                'text': '공유을 말했습니다.'
            },
            'keyboard':{
                'type':'text'
            }
        }
    )