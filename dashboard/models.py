from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

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
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    yearbook = models.ForeignKey(Yearbook, default=1, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, null=True, blank=True, help_text='Do you have a nickname? (Optional)')
    birthdate = models.DateField()
    gown_photo = models.ImageField(upload_to=gown_photo_path, default='/upload/no_photo.jpg')
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
        return reverse(url='dashboard:student-yearbook-detail', kwargs={'pk': str(self.pk)})


# class YearbookQuestion(models.Model):
#     yearbook = models.ForeignKey(Yearbook, on_delete=models.CASCADE)
#     question_text = models.CharField(max_length=100)
#     hint = models.CharField(max_length=200, blank=True, null=True, help_text='Give a hint on how to answer the question. (Optional)')
#     publish = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['publish', 'question_text',]
#         permissions = (
#                 ('can create yearbook question', 'Create a yearbook question'),
#             )

#     def __str__(self):
#         return self.question_text

#     def get_absolute_url(self):
#         return reverse(url='dashboard:yearbook-question-detail', kwargs={'pk': str(self.pk)})

# class YearbookAnswer(models.Model):
#     yearbook_question = models.ForeignKey(YearbookQuestion, on_delete=models.CASCADE)
#     answer = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name = 'Student\'s Yearbook Answer'
#         verbose_name_plural = 'Student\'s Yearbook Answers'
#         ordering = ['yearbook_question', 'updated_at',]

#     def __str__(self):
#         return self.answer

class Poll(models.Model):
    poll_text = models.CharField(max_length=255, help_text='Poll question to display')
    description = models.TextField(null=True, blank=True, help_text='Description of the purpose of the poll (Optional)')
    active = models.BooleanField('Open for Vote', default=False, help_text='Weather or not the poll is currently open for voting.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    end_at = models.DateField('Deadline for voting')

    class Meta:
        ordering = ['active', '-end_at',]

    def __str__(self):
        return self.poll_text

    def get_absolute_url(self):
        return reverse(url='dashboard:poll-detail', kwargs={'pk': str(self.pk)})

class PollChoice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)

    class Meta:
        ordering = ['poll']

    def __str__(self):
        return self.choice_text

class PollResult(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(PollChoice, on_delete=models.CASCADE)
    submitted_date = models.DateTimeField(auto_now_add=True, help_text='Date where the student voted on the poll')

    class Meta:
        ordering = ['poll', '-submitted_date',]

    def __str__(self):
        return '{}, {}'.format(self.poll, self.choice)

class Event(models.Model):
    title = models.CharField(max_length=100)
    description =  models.TextField(help_text='Summary of the event')
    dress_code = models.TextField(null=True, blank=True, help_text='Are there any dress codes to follow? (Optional)')
    venue = models.CharField(max_length=100, help_text='Where the event is taking place')
    start_at = models.DateTimeField(help_text='Starting date and time of the event')
    end_at = models.DateTimeField(help_text='Ending date and time of the event')
    fee = models.DecimalField(decimal_places=2, max_digits=12, default=0.00, help_text='Entrance Fee for the event. (Enter 0.00 if event is free)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=False, help_text='Publish to make event visible to all students')

    class Meta:
        ordering = ['-start_at', 'title',]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(url='dashboard:event-detail', kwargs={'pk', str(self.pk)})

class Program(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description =  models.TextField(help_text='Short description of the program')
    start_at = models.TimeField(help_text='Starting time of the program')
    end_at = models.TimeField(help_text='Ending time of the program')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['event', '-start_at', 'title',]

    def __str__(self):
        return '{} - ({} Event)'.format(self.title, self.event)


