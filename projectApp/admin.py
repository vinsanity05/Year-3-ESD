from django.contrib import admin
from .models import *


# Register your models here.
class StudentClubAdmin(admin.ModelAdmin):
    list_display = [field.name for field in StudentClub._meta.fields if field.name != "id"]
    list_filter = [field.name for field in StudentClub._meta.fields if field.name != "id"]


class ClubRepresentativeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ClubRepresentative._meta.fields if field.name != "id"]
    list_filter = [field.name for field in ClubRepresentative._meta.fields if field.name != "id"]


class FilmAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Film._meta.fields if field.name != "id"]
    list_filter = [field.name for field in Film._meta.fields if field.name != "id"]


class ScreenAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Screen._meta.fields if field.name != "id"]
    list_filter = [field.name for field in Screen._meta.fields if field.name != "id"]


class ShowAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Show._meta.fields if field.name != "id"]
    list_filter = [field.name for field in Show._meta.fields if field.name != "id"]


class AccountAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Account._meta.fields if field.name != "id"]
    list_filter = [field.name for field in Account._meta.fields if field.name != "id"]


from django.contrib.auth.admin import UserAdmin
from .models import User

fields = list(UserAdmin.fieldsets)
fields[0] = (None, {'fields': ('username', 'password', 'user_type')})
UserAdmin.fieldsets = tuple(fields)

admin.site.register(User, UserAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(StudentClub, StudentClubAdmin)
admin.site.register(Film, FilmAdmin)
admin.site.register(Show, ShowAdmin)
admin.site.register(Screen, ScreenAdmin)
admin.site.register(ClubRepresentative, ClubRepresentativeAdmin)
