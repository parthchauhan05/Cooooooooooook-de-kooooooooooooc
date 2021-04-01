from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
class Recipe(models.Model):
    recipe_name = models.CharField(max_length=255)
    recipe_steps = models.CharField(max_length=255)
    recipe_prep_time = models.DurationField()
    recipe_cook_time = models.DurationField()
    recipe_servings = models.IntegerField()
    recipe_image = models.FileField(upload_to='images')
    recipe_ingredient = models.ManyToManyField('Ingredient')
    recipe_favourites = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    recipe_chef = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='creater')
    
    def __str__(self):
        return self.recipe_name

class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=255)
    def __str__(self):
        return self.ingredient_name


class Ratings(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField()
