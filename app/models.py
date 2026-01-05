from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator




class User(AbstractUser):
    reputation = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class Tag(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    view_count = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    own_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='questions')
    tags = models.ManyToManyField(Tag, through='TagItem', related_name='questions')
    accepted_answer = models.OneToOneField('Answer', on_delete=models.SET_NULL, null=True, blank=True,
                                           related_name='is_accepted_for')

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    body = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    own_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answers')

    class Meta:
        ordering = ['-score', 'creation_date']


class Comment(models.Model):
    body = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    own_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')


class TagItem(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('question', 'tag')


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_votes')
    value = models.SmallIntegerField(validators=[MinValueValidator(-1), MaxValueValidator(1)])

    class Meta:
        unique_together = ('user', 'question')

class Report(models.Model):
    body = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    own_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='reports')