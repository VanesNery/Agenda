from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=100, verbose_name='Titulo')
    description = models.TextField(blank=True, null=True, verbose_name='Descrição')
    date_event = models.DateTimeField(verbose_name='Data do Evento')
    date_create = models.DateTimeField(auto_now=True, verbose_name='Data de Criação')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')

    class Meta:
        db_table = 'event'

    def __str__(self):
        return self.title
        
    def get_date_event(self):
        return self.date_event.strftime('%d/%m/%Y - %H:%M Hrs')

    def get_date_input_event(self):
        return self.date_event.strftime('%Y-%m-%dT%H:%M')
    
    def get_date_event_late(self):
        if self.date_event < datetime.now():
            return True
        else:
            return False
