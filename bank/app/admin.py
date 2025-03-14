from django.contrib import admin
from .models import Account,Gender,STATE
# Register your models here.
admin.site.register(Account)
admin.site.register(Gender)
admin.site.register(STATE)