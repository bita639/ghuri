from django.db import models
from accounts.models import MyUser

# Create your models here.

class Recipe(models.Model):
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='recipe_owner_id')
    title = models.CharField(max_length=255)
    description = models.TextField()


class Ingredient(models.Model):
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='ingredient_owner_id')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredient_recipe_id')
    description = models.CharField(max_length=255)


class Instruction(models.Model):
    recipee = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='instruction_owner_id')
    number = models.PositiveSmallIntegerField()
    description = models.TextField()