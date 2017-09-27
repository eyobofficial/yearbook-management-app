from django.db import models
from django.urls import reverse

class Yearbook(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    end_date = models.DateField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class YearbookQuestion(models.Model):
    yearbook = models.ForeignKey(Yearbook, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=100)
    hint = models.CharField(max_length=200, blank=True, null=True, help_text='Give a hint on how to answer the question. (optional)')
    publish = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['publish', 'question_text',]
        permissions = (
                ('can create yearbook question', 'Create a yearbook question'),
            )

    def __str__(self):
        return self.question_text

    def get_absolute_url(self):
        return reverse(url='dashboard:yearbook-question-detail', kwargs={'pk': str(self.pk)})

class YearbookAnswer(models.Model):
    yearbook_question = models.ForeignKey(YearbookQuestion, on_delete=models.CASCADE)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Student\'s Yearbook Answer'
        verbose_name_plural = 'Student\'s Yearbook Answers'
        ordering = ['yearbook_question', 'updated_at',]

    def __str__(self):
        return self.answer

