import json

from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from collections import Counter

from .forms import TimePhaseForm, FirstPhaseForm
from .models import FirstPhase, TimePhase


# Логин
class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'polls/login.html'

    def get_success_url(self):
        polls = TimePhase.objects.all().last()
        if polls and polls.active:
            return reverse_lazy('first')
        return reverse_lazy('main')

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

    def get_success_url(self):
        polls = TimePhase.objects.all().last()
        if polls and polls.active:
            return reverse_lazy('first')
        return reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super(FirstPhaseView, self).get_context_data(**kwargs)
        phase = TimePhase.objects.all().last()
        context['phase'] = phase
        user_vote = FirstPhase.objects.filter(user=self.request.user, polls=phase)
        if user_vote:
            context['user_vote'] = True
        now = timezone.localtime(timezone.now())
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
        context['phase'] = phase
        now = timezone.localtime(timezone.now())
        delta = (phase.first + phase.second) * 60 - (now - phase.start).seconds
        lst = []
        first = FirstPhase.objects.filter(polls=phase.id)
        for fir in first:
            if fir.time < 10:
                time = "0" + str(fir.time)
            else:
                time = str(fir.time)
            lst.append(time + str(fir.event))
        count = Counter(lst)
        max_value = max(count.values())
        max_keys = [k for k, v in count.items() if v == max_value]
        if len(max_keys) == 1:
            context['win_time'] = max_keys[0][:2]
            context['win_event'] = max_keys[0][2:]
            usr = []
            win_user = FirstPhase.objects.filter(polls=phase.id, time=max_keys[0][:2],
                                                 event=max_keys[0][2:]).values_list('user__username', flat=True)
            for win in win_user:
                usr.append(win)
            context['win_user'] = usr
        else:
            context['pat'] = True
            delta = -1
        if delta < 0:
            phase.active = False
            phase.save(update_fields=['active'])
        context['delta'] = delta
        context['dashboard'] = json.dumps(get_data_dashboard())
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


# Список вводившихся мероприятий
@login_required()
def get_event(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        events = FirstPhase.objects.filter(event__istartswith=q)
        results = []
        for ev in events:
            if ev.event not in results:
                results.append(ev.event)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


# Сброс голосования
@login_required()
def reset_polls(request):
    polls = TimePhase.objects.all().last()
    if polls.user == request.user and polls.active:
        polls.active = False
        polls.save()
        return HttpResponseRedirect(reverse_lazy('main'))
    return HttpResponseRedirect(reverse_lazy('first'))


# Сбор данных для графика
def get_data_dashboard():
    time = {}
    phases = TimePhase.objects.last()
    for i in range(0, 24):
        phase = FirstPhase.objects.filter(polls=phases, time=i)
        phase_event = phase.values_list('event', flat=True)
        if phase_event:
            time[str(i)] = list(phase_event)
        else:
            time[str(i)] = ['']
    return time
