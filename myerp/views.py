from django.contrib.auth import login, authenticate
from django.http import HttpResponse


def easy_login(request):
    username = request.GET['username']
    password = request.GET['password']
    user = authenticate(
        request, username=username, password=password
    )
    login(request, user)
    return HttpResponse('login success')
