from django.contrib import admin
from .models import User,Post,Like,Comment,follower_count

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(follower_count)

# Register your models here.
