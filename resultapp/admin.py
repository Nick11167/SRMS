from django.contrib import admin
from .models import *

admin.site.register(Studentclass)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(SubjectCombination)
admin.site.register(Result)

