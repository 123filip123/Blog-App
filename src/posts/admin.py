from django.contrib import admin


from .models import Post, Profile

class PostAdmin(admin.ModelAdmin):
    search_fields=['title','body']
    list_display=['title','slug','created_at']
    prepopulated_fields= {'slug':('title',)}

class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileInline,)




admin.site.register(Post,PostAdmin)

admin.site.register(Profile)
