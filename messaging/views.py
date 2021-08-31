import sqlite3

from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def index(request):
    if request.user:
        return redirect(f'/messaging/{request.user.username}')

    return render(request, 'login.html')

@login_required
def user(request, user_name):
    try:
        user = User.objects.get(username=user_name)
        users = User.objects.exclude(pk=user.id)
        messages = Message.objects.filter(to=user)

        return render(request, 'user.html', {
            'user_name': user_name,
            'messages': messages,
            'users': users,
        })
    except:
        return HttpResponse('something is wrong')

@login_required
def message(request):
    to = User.objects.get(pk=request.POST.get('to'))
    message = request.POST.get('message')
    m = Message(to=to, sender=request.user)
    m.save()

    conn = sqlite3.connect('./db.sqlite3')
    curr = conn.cursor()
    sql = f'UPDATE messaging_message SET message="{message}" WHERE id={m.id}'
    curr.executescript(sql)
    curr.close()
    conn.commit()

    return redirect('/')
