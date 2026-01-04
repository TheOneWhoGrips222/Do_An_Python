
from django.contrib import admin
from .models import User, Tag, Question, Answer, Comment, TagItem, Vote,Report

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Comment)
admin.site.register(TagItem)
admin.site.register(Vote)
admin.site.register(Report)


