from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Callable for naming student profile photo
def profile_photo_path(instance, filename):
    return 'profile_photos/{}/{}'.format(instance.user.id, 'profile_photo.jpg')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_committee = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to=profile_photo_path, default='defaults/default_profile_photo.jpg')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Yearbook(models.Model):
    title = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=False)
    end_date = models.DateField()

    def __str__(self):
        return self.title

# Callable for naming student photo path
def gown_photo_path(instance, filename):
    return 'uploads/students/{}/{}'.format(instance.student.id, 'gown.jpg')

def suit_photo_path(instance, filename):
    return 'uploads/students/{}/{}'.format(instance.student.id, 'suit.jpg')

def baby_photo_path(instance, filename):
    return 'uploads/students/{}/{}'.format(instance.student.id, 'baby.jpg')

class StudentYearbook(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    yearbook = models.ForeignKey(Yearbook, default=1, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, null=True, blank=True, help_text='Do you have a nickname? (Optional)')
    birthdate = models.DateField(help_text='Use YYYY-MM-DD format. Example: 1999-09-26')
    gown_photo = models.ImageField('Gown Photo (Academic Dress)', upload_to=gown_photo_path, default='/upload/no_photo.jpg')
    suit_photo = models.ImageField('Suit/Dress photo', upload_to=suit_photo_path, default='/upload/no_photo.jpg')
    baby_photo = models.ImageField('Baby photo', upload_to=baby_photo_path, default='/upload/no_photo.jpg')
    bio = models.TextField('About yourself?', help_text='Tell the world about yourself in less than 300 characters.')
    quote = models.TextField('Your favorite quote or motto?')
    thank_you_message = models.TextField('Who would you like to thank?', help_text='Take this opportunity to thank those who are special to you.')
    submit = models.BooleanField(default=False)
    submitted_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['submit', '-submitted_date', 'student',]

    def __str__(self):
        return '{}, {}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('dashboard:student-yearbook-detail', kwargs={'pk': str(self.pk)})

class Poll(models.Model):
    poll_text = models.CharField(max_length=255, help_text='Poll question to display')
    description = models.TextField(null=True, blank=True, help_text='Description of the purpose of the poll (Optional)')
    active = models.BooleanField('Open for Vote', default=False, help_text='Whether or not the poll is currently open for voting.')
    end_at = models.DateField('Deadline for voting')
    publish = models.BooleanField(default=False, help_text='Published polls can be viewed by all students')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['publish', 'active', 'end_at',]

    def __str__(self):
        return self.poll_text

    def get_absolute_url(self):
        return reverse('dashboard:poll-detail', kwargs={'pk': str(self.pk)})

class PollChoice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)

    class Meta:
        ordering = ['poll']

    def __str__(self):
        return self.choice_text

class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(PollChoice, on_delete=models.CASCADE)
    submitted_date = models.DateTimeField(auto_now_add=True, help_text='Date where the student voted on the poll')

    class Meta:
        ordering = ['poll', '-submitted_date',]

    def __str__(self):
        return '{}, {}'.format(self.poll, self.choice)

# Callable for naming student photo path
def event_photo_path(instance, filename):
    sluged_title = instance.title.replace(' ', '-').lower()
    return 'uploads/events/{}/{}'.format(sluged_title, 'event_photo.jpg')

class Event(models.Model):
    title = models.CharField(max_length=100)
    description =  models.TextField(help_text='Summary of the event')
    dress_code = models.TextField(null=True, blank=True, help_text='Are there any dress codes to follow? (Optional)')
    venue = models.CharField(max_length=100, help_text='Where the event is taking place')
    event_datetime = models.DateTimeField(help_text='Date and time of the event')
    event_photo = models.ImageField(upload_to=event_photo_path, null=True, blank=True)
    fee = models.DecimalField(decimal_places=2, max_digits=12, default=0.00, help_text='Entrance Fee for the event. (Enter 0.00 if event is free)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=False, help_text='Publish to make event visible to all students')

    class Meta:
        ordering = ['-event_datetime', 'title',]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('dashboard:event-detail', kwargs={'pk': str(self.pk)})

class Program(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description =  models.TextField(null=True, blank=True, help_text='Short description of the program')
    start_at = models.TimeField(help_text='Starting time of the program')
    end_at = models.TimeField(help_text='Ending time of the program')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['event', '-start_at', 'title',]

    def __str__(self):
        return '{} - ({} Event)'.format(self.title, self.event)
        
class EventSubscription(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['event',]

    def __str__(self):
        return '{} going to {}'.format(self.event, self.student)

class Payment(models.Model):
    title = models.CharField('Payment Title', max_length=100)
    description = models.TextField(null=True, blank=True, help_text='Describe why this particular payment is needed')
    amount = models.DecimalField('Payment Amount', max_digits=12, decimal_places=2)
    due_date = models.DateField('Due date of the payment')
    publish = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['publish', 'due_date', 'amount',]

    def __str__(self):
        return self.title 

    def get_absolute_url(self):
        return reverse('dashboard:payment-detail', kwargs={'pk': str(self.pk)})

class StudentPayment(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateField('Date of payment')

    class Meta:
        ordering = ['payment', 'payment_date',]

    def __str__(self):
        return 'Paym: {}, Student: {}'.format(self.payment, self.student)

