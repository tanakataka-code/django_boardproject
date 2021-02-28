from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .models import BoardModel
from django.contrib.auth.decorators import login_required

# Create your views here.

def signupfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.create_user(username, '', password )
        except IntegrityError:
            return render(request, 'signup.html', {'error': 'このユーザーはすでに登録されています。'})

    return render(request, 'signup.html')


def loginfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            return render(request, 'login.html', {})

    return render(request, 'login.html', { })


@login_required
def listfunc(request):
    object_list = BoardModel.objects.all()
    return render(request, 'list.html', {'object_list': object_list})


def logoutfunc(request):
    logout(request)
    return redirect('login')


@login_required
def detailfunc(request, pk):
    obj = get_object_or_404(BoardModel, pk=pk)
    return render(request, 'detail.html', {'obj': obj})


def goodfunc(request, pk):
    obj = BoardModel.objects.get(pk=pk)
    obj.good += 1
    obj.save()
    return redirect('list')


def readfunc(request, pk):
    obj = BoardModel.objects.get(pk=pk)
    username = request.user.get_username()

    if username in obj.readtext:
        return redirect('list')
    else:
        obj.read += 1
        obj.readtext = obj.readtext + ' ' + username
        obj.save()
        return redirect('list')