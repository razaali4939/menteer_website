from django.contrib import admin
from .models import Mentee_Profile
# Register your models here.

admin.site.register(Mentee_Profile)
# class menteeAdmin(admin.ModelAdmin):
#     list_display=('pt_id','name', 'name', 'gender', 'age', 'phone', 'address', 'city', 'country')
