from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
from .forms import IngredientForm, InstructionForm, RecipeForm


def add_new_value(request):
    rform = RecipeForm(request.POST or None)
    iform = IngredientForm(request.POST or None)
    cform = InstructionForm(request.POST or None)
    if rform.is_valid() and iform.is_valid() and cform.is_valid():
        rinstance = rform.save(commit=False)
        iinstance = iform.save(commit=False)
        cinstance = cform.save(commit=False)
        user = request.user
        rinstance.owner = user
        rinstance.save()
        iinstance.owner = user
        cinstance.owner = user
        iinstance.recipe_id = rinstance.id
        cinstance.recipe_id = rinstance.id
        iinstance.save()
        cinstance.save()
        return HttpResponseRedirect('/package/add/')
    context = {
        'rform' : rform,
        'iform' : iform,
        'cform' : cform,
    }
    return render(request, "add_new_recipe.html", context)