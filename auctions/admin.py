from django.contrib import admin


# Register your models here.
from .models import MenuListings
admin.site.register(MenuListings)


from .models import Comment
admin.site.register(Comment)
