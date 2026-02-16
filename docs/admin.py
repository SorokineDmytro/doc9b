from django.contrib import admin
from .models import Space, Page, UserCategory

class SpaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at',)

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'space', 'parent', 'order',)
    list_filter = ('space', 'categories',)
    search_fields = ('title',)

class UserCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)

admin.site.register(Space, SpaceAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserCategory, UserCategoryAdmin)