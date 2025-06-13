from django.contrib import admin
from core.models import *

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(PostTag)
admin.site.register(Comment)
admin.site.register(Like)



