from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Question)
admin.site.register(Mcq)
admin.site.register(Paper)
