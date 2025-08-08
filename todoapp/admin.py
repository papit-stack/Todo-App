from django.contrib import admin
from .models import Todo,Category
# Register your models here.
admin.site.register(Category)
admin.site.register(Todo)
