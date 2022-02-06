from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Reviews)
