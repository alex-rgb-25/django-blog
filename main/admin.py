from django.contrib import admin
from .models import Blog, Comments, Likers
# Register your models here.

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "user","title","text", "url", "date","get_tags", "likes")
#show tags in admin interface
    def get_tags(self, obj):
        return ", ".join(o for o in obj.tags.names())
class CommentsAdmin(admin.ModelAdmin):
    list_display = ("id", "user","text", "blog")

@admin.register(Likers)
class LikersAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "blog")



admin.site.register(Comments, CommentsAdmin)