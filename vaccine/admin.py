from django.contrib import admin
from .models import Usertable

class UserAdmin(admin.ModelAdmin):
    list_display=('fname','lname','email','phone','dob','role','password')
admin.site.register(Usertable,UserAdmin)