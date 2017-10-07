from django import forms
from django.utils import timezone

from .models import TimePhase, FirstPhase


def time_choice():
    time_list = []
    now = timezone.localtime(timezone.now())
    for hour in range(now.hour, 24):
        time_list.append((hour, hour))
    choices = tuple(time_list)
    return choices


class TimePhaseForm(forms.ModelForm):
    first = forms.IntegerField(min_value=1, initial=1, label='Длительность первой фазы')
    second = forms.IntegerField(min_value=1, initial=1, label='Длительность второй фазы')

    class Meta:
        model = TimePhase
        fields = ['first', 'second']


class FirstPhaseForm(forms.ModelForm):
    time = forms.ChoiceField(choices=time_choice, label='Время')

    class Meta:
        model = FirstPhase
        fields = ['time', 'event']
