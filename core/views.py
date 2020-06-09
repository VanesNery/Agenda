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
    id_event = request.GET.get('id')
    dados = {}
    if id_event:
        dados['event'] = Event.objects.get(id=id_event)
    return render(request, 'evento.html')


@login_required(login_url='/login/')
def submit_event(request):
    if request.POST:
        title = request.POST.get('title')
        date_event = request.POST.get('date_event')
        description = request.POST.get('description')
        user = request.user
        id_event = request.POST.get('id_event')
        if id_event:
            event = Event.objects.get(id=id_event)
            if event.user == user:
                Event.objects.filter(id=id_event.update(title=title,
                                                        date_event=date_event,
                                                        description=description,
                                                        user=user))
        else:
            Event.objects.create(title=title,
                                 date_event=date_event,
                                 description=description,
                                 user=user)
    return redirect('/')


@login_required(login_url='/login/')
def delete_event(request, id_event):
    user = request.user
    event = Event.objects.get(id=id_event)
    if user == event.user:
        event.delete()
    return redirect('/')
