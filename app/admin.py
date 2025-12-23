
from django.contrib import admin
from .models import Question, Answer, Tag, TagItem, Report, Users

admin.site.register(Users)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(TagItem)
admin.site.register(Report)


