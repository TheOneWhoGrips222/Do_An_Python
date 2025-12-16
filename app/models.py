from django.db import models


# 1. Bảng User (Thông tin người dùng)
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    Displayname = models.CharField(max_length=100)
    CreationDate = models.DateField()
    Repution = models.IntegerField()
    Llike = models.IntegerField()
    DisLike = models.IntegerField()



# 2. Bảng Question (Câu hỏi)
class Question(models.Model):
    id = models.IntegerField(primary_key=True)
    Title = models.CharField(max_length=100)
    Body = models.TextField()
    CreationDate = models.DateField()
    score = models.DecimalField(max_digits=10, decimal_places=2)
    AnswerCount = models.IntegerField()
    FavoriteCount = models.IntegerField()
    AcceptAnswer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    Closedate = models.DateField(null=True, blank=True)
    OwnUser = models.ForeignKey('User', on_delete=models.CASCADE)






# 3. Bảng Answer (Câu trả lời)
class Answer(models.Model):
    id = models.IntegerField(primary_key=True)
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE)
    AnswerDate = models.DateField()
    AnswerScore = models.DecimalField(max_digits=5, decimal_places=2)
    AnswerBodt = models.TextField()
    OwnUser = models.ForeignKey('User', on_delete=models.CASCADE)

class Tags(models.Model):
    id = models.IntegerField(primary_key=True)


class TagItem(models.Model):
    Tag_id = models.ForeignKey('Tags', on_delete=models.CASCADE)
    Question_id = models.ForeignKey('Question', on_delete=models.CASCADE)
    class Meta:
        unique_together = (('Tag_id', 'Question_id'),)

class Report(models.Model):
    id = models.IntegerField(primary_key=True)
    Question_id = models.ForeignKey('Question', on_delete=models.CASCADE)
    Title =models.TextField()



