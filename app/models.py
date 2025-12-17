
from django.db import models
from django.conf import settings




# --- Bảng Question (Câu hỏi) ---
class Question(models.Model):
    id = models.IntegerField(primary_key=True)
    Title = models.CharField(max_length=200)
    Body = models.TextField()
    CreationDate = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    AnswerCount = models.IntegerField(default=0)
    FavoriteCount = models.IntegerField(default=0)
    AcceptAnswer = models.ForeignKey('Answer', on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='accepted_by_question')
    Closedate = models.DateField(null=True, blank=True)
    OwnUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.Title


# --- Bảng Answer (Câu trả lời) ---
class Answer(models.Model):
    id = models.IntegerField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')  # Liên kết đến Question
    AnswerDate = models.DateTimeField(auto_now_add=True)
    AnswerScore = models.IntegerField(default=0)
    AnswerBody = models.TextField()
    OwnUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return f"Answer for: {self.question.Title[:20]}"

    class Meta:
        ordering = ['-AnswerScore', 'AnswerDate']


# --- Bảng Tags ---
class Tags(models.Model):
    name = models.CharField(max_length=50, unique=True)

class TagItem(models.Model):
    q_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='questions')
    tag_id = models.ForeignKey(Tags, on_delete=models.CASCADE, related_name='tags')
    class Meta:
        unique_together = (('q_id', 'tag_id'),)

    def __str__(self):
        return self.name
class Report(models.Model):
    id = models.IntegerField(primary_key=True)
    body = models.TextField()
    q_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='reports')