from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from core.models import Event

# Create your views here.

# def index(request):
#     return redirect('/agenda/')


def login_user(request):
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/')


def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou senha inválida")

    return redirect('/')


@login_required(login_url='/login/')
def list_event(request):
    usuario = request.user
    evento = Event.objects.filter(user=usuario)
    dados = {'eventos': evento}
    return render(request, 'agenda.html', dados)


@login_required(login_url='/login/')
def events(request):
    return render(request, 'evento.html')


@login_required(login_url='/login/')
def submit_event(request):
    if request.POST:
        title = request.POST.get('title')
        date_event = request.POST.get('date_event')
        description = request.POST.get('description')
        user = request.user
        Event.objects.create(title=title,
                             date_event=date_event,
                             description=description,
                             user=user)
    return redirect('/')
