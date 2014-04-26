from django.contrib import admin
from ticket_backend.models import Catagory, User, Author, Ticketrequest, Media, Activity

# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    """docstring for AuthorAdmin"""
    list_display = ('name',)
    search_fields = ('name',)

class UserAdmin(admin.ModelAdmin):
    """docstring for AuthorAdmin"""
    list_display = ('name', 'card_id',)
    search_fields = ('card_id',)

class ActivityAdmin(admin.ModelAdmin):
    """docstring for BlogAdmin"""
    list_diaplay = ('id', 'caption', 'author', 'destruction', 'posters', 'catagories','ticket_number', 'ticket_requests', 'publish_time', 'request_begin_time', 'request_deadline',)
    list_filter = ('publish_time',)
    date_hierarchy = 'publish_time'
    ordering = ('-publish_time',)
    filter_horizontal = ('catagories',)
    # raw_id_field = ('author',)

class CatagoryAdmin(admin.ModelAdmin):
    """docstring for TagAdmin"""
    list_display = ('catagory_name',)
    search_fields = ('catagory_name',)

class MediaAdmin(admin.ModelAdmin):
    """docstring for MediaAdmin"""
    readonly_fields = ('thumb',)
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
           return self.readonly_fields
        return self.readonly_fields

class TicketrequestAdmin(admin.ModelAdmin):
    """docstring for CommentAdmin"""
    list_display = ('target', 'person', 'request_time',)
    search_fields = ('person',)

admin.site.register(Author, AuthorAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Catagory, CatagoryAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Ticketrequest, TicketrequestAdmin)