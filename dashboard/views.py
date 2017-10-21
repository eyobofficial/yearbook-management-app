from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

# Import user authentication modules
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

# Import Models
from .models import (Yearbook, 
                     StudentYearbook,
                     Poll,
                     PollChoice,
                     Vote,
                     Event,
                     Program,
                     EventSubscription, 
                     Payment,
                     StudentPayment,
                     )

# Import Forms
from dashboard.forms import (SignupForm, 
                             YearbookForm, 
                             YearbookSubmitForm,
                             PollForm,
                             UserAccountForm,
                             ProfilePhotoForm,
                             )

# Check if user is committee
def check_committee(user):
    return user.profile.is_committee

# Signup view
def signup(request):
    """
    Register a new student, login the new user and redirect to breakdowns:index page
    """

    # Check if user already logged
    if request.user.is_authenticated:
        return redirect('dashboard:index')
        
    form_class = SignupForm
    template_name = 'registration/signup.html'

    if request.method == 'POST':
        form = form_class(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.is_active = False
            # member_group = Group.objects.get(name='member')
            # user.groups.add(member_group,)
            user.save()
            login(request, user)
            return redirect('dashboard:index')
    else:
        form = form_class()
    return render(request, template_name, context={'form': form})

@login_required
def index(request):
    return render(request, 'dashboard/index.html', {
            'page_name': 'index',
        })

@login_required
def yearbook(request):
    try:
        yearbook_detail = StudentYearbook.objects.get(student=request.user)
    except:
        yearbook_detail = None

    if yearbook_detail is None:
        return redirect('dashboard:yearbook-create')
    else:
        if yearbook_detail.submit is not True:
            return redirect('dashboard:yearbook-submit')
        else:
            return render(request, 'dashboard/yearbook.html', {
                    'yearbook': yearbook_detail,
                    'page_name': 'yearbook',
                })

@login_required
def yearbook_create(request):
    try:
        yearbook_detail = StudentYearbook.objects.get(student=request.user)
    except:
        yearbook_detail = None

    if yearbook_detail is not None:
        if yearbook_detail.submit is True:
            return redirect('dashboard:yearbook')
        else:
            return redirect('dashboard:yearbook-update')
    else:
        form_class = YearbookForm

        if request.method == 'POST':
            # POST request
            form = form_class(request.POST, request.FILES)

            if form.is_valid():
                form.instance.student = request.user
                form.save()
                return redirect('dashboard:yearbook-submit')
        else:
            # GET Request
            form = form_class()
        return render(request, 'dashboard/yearbook_form.html', context={
                'form': form,
                'page_name': 'yearbook',
            })

@login_required
def yearbook_update(request):
    try:
        yearbook_detail = StudentYearbook.objects.get(student=request.user)
    except:
        yearbook_detail = None

    if yearbook_detail is None:
        return redirect('dashboard:yearbook-create')
    else:
        if yearbook_detail.submit is True:
            return redirect('dashboard:yearbook')
        else:
            form_class = YearbookForm

            if request.method == 'POST':
                form = form_class(request.POST, request.FILES, instance=yearbook_detail)

                if form.is_valid():
                    form.save()
                    return redirect('dashboard:yearbook-submit')
            else:
                form = form_class(instance=yearbook_detail)
            return render(request, 'dashboard/yearbook_form.html', {
                    'form': form,
                    'page_name': 'yearbook',
                }) 

@login_required
def yearbook_submit(request):
    try:
        yearbook_detail = StudentYearbook.objects.get(student=request.user)
    except:
        yearbook_detail = None

    if yearbook_detail is None:
        return redirect('dashboard:yearbook-create')
    else:
        form_class = YearbookSubmitForm

        if request.method == 'POST':
            # POST request
            form = form_class(request.POST)

            if form.is_valid():
                yearbook_detail.submit = True
                yearbook_detail.save()
                return redirect('dashboard:yearbook')
        else:
            # GET Request
            if yearbook_detail.submit is True:
                return redirect('dashboard:yearbook')
            form = form_class()
        return render(request, 'dashboard/yearbook_submit.html', context={
                'form': form,
                'yearbook': yearbook_detail,
                'page_name': 'yearbook',
            })

class PollList(LoginRequiredMixin, generic.ListView):
    model = Poll

    def get_queryset(self, *args, **kwargs):
        if self.request.user.profile.is_committee:
            return Poll.objects.all()
        return Poll.objects.filter(publish=True)

    def get_context_data(self, *args, **kwargs):
        context = super(PollList, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'polls'
        student_poll_list = []

        for student_poll in Vote.objects.filter(student_id=self.request.user.id):
            student_poll_list.append(student_poll.poll.id)

        context['student_poll_list'] = student_poll_list
        context['active_poll_count'] = len(Poll.objects.filter(active=True))
        return context

class PollDetail(UserPassesTestMixin, LoginRequiredMixin, generic.DetailView):
    model = Poll 

    def test_func(self, *args, **kwargs):
        return self.request.user.profile.is_committee

    def get_context_data(self, *args, **kwargs):
        context = super(PollList, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'polls'
        return context 

@login_required
def vote(request, pk):
    # Get a particular poll 
    try:
        poll = Poll.objects.get(pk=pk)
    except:
        poll = None
    
    # Get a Choice List for a specific poll 
    try:
        choice_list = PollChoice.objects.filter(poll_id=pk)
    except:
        choice_list = None

    if request.method == 'POST':
        # POST Request
        choice = request.POST.get('choice')
        if choice is not None:
            # Update Record
            user_vote = Vote(poll=poll, choice_id=choice, student=request.user)
            user_vote.save()
            return redirect('dashboard:poll-result', pk=poll.id)
    else:
        # GET Request
        try:
            vote = Vote.objects.get(student_id=request.user.id, poll_id=pk)
        except:
            vote = None

        if vote is not None:
            # i.e. User already voted
            return redirect('dashboard:poll-result', pk=poll.id)

        if poll is None:
            # No such poll is found
            return redirect('dashboard:poll-list')

        if poll.active is False:
            # Voting is closed
            return redirect('dashboard:poll-result', pk=poll.id)
    return render(request, 'dashboard/vote_form.html', {
            'poll': poll,
            'choice_list': choice_list, 
        })

class PollCreate(UserPassesTestMixin, CreateView):
    model = Poll
    fields = ('poll_text', 'description', 'end_at', 'publish',)
    template_name = 'dashboard/poll_create_form.html'

    def test_func(self):
        return self.request.user.profile.is_committee

    def get_context_data(self, *args, **kwargs):
        context = super(PollCreate, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'polls'
        context['subpage_name'] = 'add poll'
        return context

class PollUpdate(UserPassesTestMixin, UpdateView):
    model = Poll 
    fields = ('poll_text', 'description', 'end_at', 'publish',)
    template_name = 'dashboard/poll_update_form.html'

    def test_func(self):
        return self.request.user.profile.is_committee

    def get_context_data(self, *args, **kwargs):
        context = super(PollUpdate, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'polls'
        context['subpage_name'] = 'update poll'
        return context

class PollDelete(UserPassesTestMixin, DeleteView):
    model = Poll
    template_name = 'dashboard/poll_confirm_delete.html'
    success_url = '/dashboard/polls/'

    def test_func(self):
        return self.request.user.profile.is_committee

    def get_context_data(self, *args, **kwargs):
        context = super(PollDelete, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'polls'
        context['subpage_name'] = 'Delete poll'
        return context

@login_required
def poll_result(request, pk):
    # Get a particular poll 
    try:
        poll = Poll.objects.get(pk=pk)
    except:
        poll = None

    if poll is None:
        # i.e. The requested poll does not exist in the db
        return redirect('dashboard:poll-list')

    # Get current logged user's vote    
    try:
        user_vote = Vote.objects.get(poll_id=pk, student_id=request.user.id)
    except:
        user_vote = None

    if user_vote is None and poll.active:
        # i.e. User have not votted yet and poll is currently active (i.e. votting still ongoing)
        return redirect('dashboard:poll-vote', pk=poll.id)
    
    total_vote = Vote.objects.filter(poll_id=pk).count()
    choice_list = PollChoice.objects.filter(poll_id=pk)
    choice_polls = []

    for choice in choice_list:
        choice_poll = Vote.objects.filter(choice_id=choice.id)

        # Get percentage of votes for a particular choice
        try:
            percent = (choice_poll.count() / total_vote) * 100
        except ZeroDivisionError:
            percent = 0

        choice_dict = {
            'id': choice.id, 
            'text': choice.choice_text,
            'count': choice_poll.count(),
            'percent': percent,
        }
        choice_polls.append(choice_dict)
    
    return render(request, 'dashboard/poll_result.html', {
            'page_name': 'polls',
            'poll': poll,
            'user_vote': user_vote,
            'total_vote': total_vote,
            'choice_list': choice_list,
            'choice_polls': choice_polls,
        })

class PollDetail(UserPassesTestMixin, generic.DetailView):
    model = Poll 

    def test_func(self, *args, **kwargs):
        return self.request.user.profile.is_committee

    def get_context_data(self, *args, **kwargs):
        context = super(PollDetail, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'polls'
        context['choice_list'] = PollChoice.objects.filter(poll_id=self.kwargs['pk'])
        return context

class ChoiceCreate(UserPassesTestMixin, generic.CreateView):
    model = PollChoice
    fields = ('choice_text',)
    template_name = 'dashboard/choice_create_form.html'

    def test_func(self, *args, **kwargs):
        return self.request.user.profile.is_committee

    def get_success_url(self, *args, **kwargs):
        return '/dashboard/poll/{}'.format(self.kwargs['pk'])

    def form_valid(self, form, *args, **kwargs):
        form.instance.poll = Poll.objects.get(pk=self.kwargs['pk'])
        return super(ChoiceCreate, self).form_valid(form, *args, **kwargs)
        

    def get_context_data(self, *args, **kwargs):
        context = super(ChoiceCreate, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'polls'
        context['poll'] = Poll.objects.get(pk=self.kwargs['pk'])
        context['choice_list'] = PollChoice.objects.filter(poll_id=self.kwargs['pk'])
        return context

class ChoiceUpdate(UserPassesTestMixin, generic.UpdateView):
    model = PollChoice
    fields = ('choice_text',)
    template_name = 'dashboard/choice_update_form.html'

    def test_func(self, *args, **kwargs):
        return self.request.user.profile.is_committee

    def get_success_url(self, *args, **kwargs):
        choice = PollChoice.objects.get(pk=self.kwargs['pk'])
        return '/dashboard/poll/{}'.format(choice.poll.id)

    def get_context_data(self, *args, **kwargs):
        context = super(ChoiceUpdate, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'polls'
        targeted_choice = PollChoice.objects.get(pk=self.kwargs['pk'])
        poll = Poll.objects.get(pk=targeted_choice.poll.id)
        context['targeted_choice'] = targeted_choice
        context['poll'] = poll
        return context

class ChoiceDelete(UserPassesTestMixin, generic.DeleteView):
    model = PollChoice
    template_name = 'dashboard/choice_confirm_delete.html'

    def test_func(self, *args, **kwargs):
        return self.request.user.profile.is_committee

    def get_success_url(self, *args, **kwargs):
        choice = PollChoice.objects.get(pk=self.kwargs['pk'])
        return '/dashboard/poll/{}'.format(choice.poll.id)

    def get_context_data(self, *args, **kwargs):
        context = super(ChoiceDelete, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'polls'
        choice = PollChoice.objects.get(pk=self.kwargs['pk'])
        poll = Poll.objects.get(pk=choice.poll.id)
        context['choice'] = choice
        context['poll'] = poll
        return context


class EventList(LoginRequiredMixin, generic.ListView):
    model = Event

    def get_queryset(self, *args, **kwargs):
        return Event.objects.filter(publish=True)

    def get_context_data(self, *args, **kwargs):
        context = super(EventList, self).get_context_data(*args, **kwargs)
        subscription_list = []

        for event in Event.objects.filter(publish=True):
            subscription_count = EventSubscription.objects.filter(event_id=event.id).count()
            event_subscription = (event.id, subscription_count)
            subscription_list.append(event_subscription)
        
        context['subscription_list'] = subscription_list
        context['event_subscription'] = EventSubscription.objects.all()
        context['page_name'] = 'events'
        return context

class EventDetail(LoginRequiredMixin, generic.DetailView):
    model = Event

    def get_context_data(self, *args, **kwargs):
        context = super(EventDetail, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'events'
        try:
            event_subscription = EventSubscription.objects.get(event_id=self.kwargs['pk'], student_id=self.request.user.id)
        except:
            event_subscription = None

        context['event_subscription'] = event_subscription
        context['program_list'] = Program.objects.filter(event_id=self.kwargs['pk'])
        return context

class EventCreate(UserPassesTestMixin, CreateView):
    model = Event 
    fields = ('title', 'description', 'venue', 'event_datetime', 'dress_code', 'fee', 'event_photo', 'publish',)
    
    def test_func(self):
        return self.request.user.profile.is_committee
        
    def get_context_data(self, *args, **kwargs):
        context = super(EventCreate, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'events'
        context['subpage_name'] = 'add event'
        return context

class EventUpdate(UserPassesTestMixin, UpdateView):
    model = Event 
    fields = ('title', 'description', 'venue', 'event_datetime', 'dress_code', 'fee', 'event_photo', 'publish',)
    
    def test_func(self):
        return self.request.user.profile.is_committee

    # def get_success_url(self, *args, **kwargs):
    #     return '/dashboard/event/{}'.format(self.kwargs['pk'])

    def get_context_data(self, *args, **kwargs):
        context = super(EventUpdate, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'events'
        context['subpage_name'] = 'update event'
        return context

class EventDelete(UserPassesTestMixin, DeleteView):
    model = Event 
    template_name = 'dashboard/event_confirm_delete.html'
    success_url = '/dashboard/events/'

    def test_func(self):
        return self.request.user.profile.is_committee

    def get_context_data(self, *args, **kwargs):
        context = super(EventDelete, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'events'
        context['subpage_name'] = 'delete event'
        return context

@login_required
def subscribe_to_event(request):
    if request.method == 'GET':
        return redirect('dashboard:event-list')
    else:
        event_id = int(request.POST['event_id'])

        try:
            subscription_status = EventSubscription.objects.get(event_id=event_id, student_id=request.user.id)
        except:
            subscription_status = None

        if subscription_status is None:
            subscribe = EventSubscription(student_id=request.user.id, event_id=event_id)
            subscribe.save()
        else:
            subscription_status.delete()
        return redirect('dashboard:event-detail', pk=event_id)

class PaymentList(LoginRequiredMixin, generic.ListView):
    model = Payment
    queryset = Payment.objects.filter(publish=True)

    def post(self, *args, **kwargs):
        pass

    def get_context_data(self, *args, **kwargs):
        context = super(PaymentList, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'payments'
        student_payments = []
        for student_payment in StudentPayment.objects.filter(student_id=self.request.user.id):
            student_payments.append(student_payment.payment.id)

        context['student_payments'] = student_payments
        return context

class PaymentDetail(LoginRequiredMixin, generic.DetailView):
    model = Payment

    def get_context_data(self, *args, **kwargs):
        context = super(PaymentDetail, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'payments'

        try:
            student_payment = StudentPayment.objects.get(payment_id=self.kwargs['pk'], student_id=self.request.user.id)
        except:
            student_payment = None

        context['student_payment'] = student_payment
        return context

class PaymentCreate(UserPassesTestMixin, generic.CreateView):
    model = Payment 
    fields = ('title', 'description', 'amount', 'due_date', 'publish',)

    def test_func(self, *args, **kwargs):
        return self.request.user.profile.is_committee

    def get_context_data(self, *args, **kwargs):
        context = super(PaymentCreate, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'payments'
        context['subpage_name'] = 'add payment'
        return context

class PaymentUpdate(UserPassesTestMixin, generic.UpdateView):
    model = Payment 
    fields = ('title', 'description', 'amount', 'due_date', 'publish',)

    def test_func(self, *args, **kwargs):
        return self.request.user.profile.is_committee

    def get_context_data(self, *args, **kwargs):
        context = super(PaymentUpdate, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'payments'
        context['subpage_name'] = 'update payment'
        return context

class PaymentDelete(UserPassesTestMixin, DeleteView):
    model = Payment
    template_name = 'dashboard/payment_confirm_delete.html'
    success_url = '/dashboard/payments/'

    def test_func(self, *args, **kwargs):
        return self.request.user.profile.is_committee

    def get_context_data(self, *args, **kwargs):
        context = super(PaymentDelete, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'payments'
        context['subpage_name'] = 'delete payment'
        return context    

class AccountDetail(LoginRequiredMixin, generic.TemplateView):
    template_name = 'dashboard/account_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AccountDetail, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'account' 
        context['form'] = ProfilePhotoForm
        return context

@login_required
def change_profile_photo(request):
    form_class =  ProfilePhotoForm

    if request.method == 'POST':
        form =  form_class(request.POST, request.FILES, instance=request.user.profile)

        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('dashboard:account-detail')
    else:
        form = form_class(instance=request.user.profile)
    return render(request, 'dashboard/account_detail.html', {
            'form': form,
        })

@login_required
def account_update(request):
    account_form_class = UserAccountForm
    profile_form_class = ProfilePhotoForm
    template_name = 'dashboard/account_update.html'

    if request.method == 'POST':
        account_form = account_form_class(request.POST, instance=request.user)
        profile_form = profile_form_class(request.POST, request.FILES, instance=request.user.profile)

        if account_form.is_valid() and profile_form.is_valid():
            account_form.save()
            profile_form.save()
            return redirect('dashboard:account-detail')
    else:
        account_form = account_form_class(instance=request.user)
        profile_form = profile_form_class(instance=request.user)
    return render(request, template_name, {
            'page_name': 'account',
            'account_form': account_form,
            'profile_form': profile_form,
        })