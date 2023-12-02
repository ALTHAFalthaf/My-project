from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(Appointment)




from django.contrib import admin
from .models import Record, Schedule, Vaccine, Immunogen



class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('vaccine_type',)


admin.site.register(Schedule, ScheduleAdmin)


class VaccineAdmin(admin.ModelAdmin):
    list_display = ('timing',)

admin.site.register(Vaccine, VaccineAdmin)
admin.site.register(Immunogen)