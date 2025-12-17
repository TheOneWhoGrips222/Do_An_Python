
from django.contrib import admin
from .models import Question, Answer, Tags, TagItem, Report



admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tags)
admin.site.register(TagItem)
admin.site.register(Report)


