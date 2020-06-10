from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from core.models import Event
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse

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
    user = request.user
    current_date = datetime.now() - timedelta(hours=1)
    event = Event.objects.filter(user=user,
                                 date_event__gt=current_date)
    # __gt é maior e __lt para menor
    data = {'events': event}
    return render(request, 'agenda.html', data)


@login_required(login_url='/login/')
def events(request):
    id_event = request.GET.get('id')
    data = {}
    if id_event:
        data['event'] = Event.objects.get(id=id_event)
    return render(request, 'evento.html', data)


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
                Event.objects.filter(id=id_event).update(title=title,
                                                         date_event=date_event,
                                                         description=description,
                                                         user=user)
        else:
            Event.objects.create(title=title,
                                 date_event=date_event,
                                 description=description,
                                 user=user)
    return redirect('/')


@login_required(login_url='/login/')
def delete_event(request, id_event):
    user = request.user
    try:
        event = Event.objects.get(id=id_event)
    except Exception:
        raise Http404()
    if user == event.user:
        event.delete()
    else:
        raise Http404()
    return redirect('/')


@login_required(login_url='/login/')
def json_list_event(request):
    user = request.user
    event = Event.objects.filter(user=user).values('id', 'title')
    return JsonResponse(list(event), safe=False)


@login_required(login_url='/login/')
def historic(request):
    user = request.user
    current_date = datetime.now()
    event = Event.objects.filter(user=user,
                                 date_event__lt=current_date)
    data = {'events': event}
    return render(request, 'historico.html', data)
