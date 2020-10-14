from django.forms import ModelForm
from .models import Recipe, Ingredient, Instruction


class RecipeForm(ModelForm):

    class Meta:
        model = Recipe
        exclude = ['owner',]

class IngredientForm(ModelForm):

    class Meta:
        model = Ingredient
        exclude = ['owner','recipe',]

class InstructionForm(ModelForm):

    class Meta:
        model = Instruction
        exclude = ['recipee',]