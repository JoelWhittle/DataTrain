from django.contrib import admin
from .models import Post
from .models import Orders
# Register your models here.
admin.site.register(Post)
admin.site.register(Orders)