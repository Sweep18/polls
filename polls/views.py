import json

from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils import timezone

from .forms import TimePhaseForm, FirstPhaseForm
from .models import FirstPhase, TimePhase
from .utils import get_win_list, reset_polls, get_data_dashboard


# Логин
class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'polls/login.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super(LoginView, self).form_valid(form)


# Регистрация
class RegisterView(FormView):
    form_class = UserCreationForm
    template_name = 'polls/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super(RegisterView, self).form_valid(form)


# Старт голосования
class MainPageView(LoginRequiredMixin, FormView):
    form_class = TimePhaseForm
    template_name = 'polls/main.html'
    success_url = reverse_lazy('first')

    # Выбираем страницу входа, если голосование активно
    def dispatch(self, request, *args, **kwargs):
        polls = TimePhase.objects.all().last()
        now = timezone.localtime(timezone.now())

        if polls and polls.active:
            delta = polls.first * 60 - (now - polls.start).seconds
            if delta >= 0:
                return HttpResponseRedirect(reverse_lazy('first'))
            else:
                return HttpResponseRedirect(reverse_lazy('second'))
        return super(MainPageView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        phase = TimePhase.objects.all().last()
        if not phase or not phase.active:
            polls = form.save(commit=False)
            polls.user = self.request.user
            polls.save()
        return super(MainPageView, self).form_valid(form)


# Первая фаза
class FirstPhaseView(LoginRequiredMixin, FormView):
    form_class = FirstPhaseForm
    template_name = 'polls/first.html'
    success_url = reverse_lazy('first')

    def get_context_data(self, **kwargs):
        context = super(FirstPhaseView, self).get_context_data(**kwargs)
        now = timezone.localtime(timezone.now())
        phase = TimePhase.objects.all().last()
        user_vote = FirstPhase.objects.filter(user=self.request.user, polls=phase)

        if user_vote:
            context['user_vote'] = True
        context['phase'] = phase
        context['delta'] = phase.first * 60 - (now - phase.start).seconds
        return context

    def form_valid(self, form):
        polls = TimePhase.objects.all().last()
        if polls.active:
            polls.votes += 1
            polls.save(update_fields=['votes'])
            first = form.save(commit=False)
            first.polls = polls
            first.user = self.request.user
            first.save()
        return super(FirstPhaseView, self).form_valid(form)


# Вторая фаза
class SecondPhaseView(LoginRequiredMixin, FormView):
    form_class = FirstPhaseForm
    template_name = 'polls/second.html'
    success_url = reverse_lazy('second')

    def get_context_data(self, **kwargs):
        context = super(SecondPhaseView, self).get_context_data(**kwargs)
        phase = TimePhase.objects.all().last()

        # Если нет голосов, то отмена голосования
        if phase.votes == 0:
            reset_polls(phase)
            context['empty'] = True
            return context

        now = timezone.localtime(timezone.now())
        delta = (phase.first + phase.second) * 60 - (now - phase.start).seconds

        # Получаем список победителей
        context['win_time'], context['win_event'], context['win_user'] = get_win_list(phase)

        # Проверка завершения голосования
        if delta < 0 or not context['win_time']:
            reset_polls(phase)

        context['phase'] = phase
        context['delta'] = delta
        context['dashboard'] = json.dumps(get_data_dashboard())  # Получаем данные для графика
        return context

    def form_valid(self, form):
        polls = TimePhase.objects.all().last()
        if polls.active:
            polls.votes += 1
            polls.save(update_fields=['votes'])
            first, created = FirstPhase.objects.get_or_create(polls=polls, user=self.request.user,
                                                              defaults={'time': form.cleaned_data.get('time'),
                                                                        'event': form.cleaned_data.get('event')})
            if first:
                first.time = form.cleaned_data.get('time')
                first.event = form.cleaned_data.get('event')
                first.save(update_fields=['time', 'event'])
        return super(SecondPhaseView, self).form_valid(form)


# Сброс голосования
class ResetPollView(LoginRequiredMixin, TemplateView):
    template_name = 'polls/reset.html'

    def get_context_data(self, **kwargs):
        context = super(ResetPollView, self).get_context_data(**kwargs)
        polls = TimePhase.objects.all().last()
        if polls.user == self.request.user and polls.active:
            reset_polls(polls)
        return context
