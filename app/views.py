from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.

def keyboard(request):

    return JsonResponse(
        {
            'type':'buttons',
            'buttons':['key one','key two','key three']
        }
    )
