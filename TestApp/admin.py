from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Recipe, Ingredient, Instruction
# Register your models here.

admin.site.register(Recipe)
admin.site.register(Ingredient)

admin.site.register(Instruction)