from django.contrib import admin
from .models import *
from django.contrib.sites.models import Site
from . import models

admin.site.unregister(Site)

class SiteAdmin(admin.ModelAdmin):
    fields = ('id', 'name', 'domain')
    readonly_fields = ('id',)
    list_display = ('id', 'name', 'domain')
    list_display_links = ('name',)
    search_fields = ('name', 'domain')


admin.site.register(Site, SiteAdmin)
admin.site.register(Profile)
admin.site.register(Self_info)
admin.site.register(Interest)
admin.site.register(Friend_request)
admin.site.register(Friend_response)
admin.site.register(Letter_network)
admin.site.register(Letter)

@admin.register(School_img)
class School_imgAdmin(admin.ModelAdmin):
    list_display = ['image','confirm','user']
    list_display_links = ['image', 'user']
    list_editable = ['confirm']
    list_per_page = 50
    ordering = ['confirm']


admin.site.register(Agree)
admin.site.register(Phone)





