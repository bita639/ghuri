from django.db import models

MALE = 'Male'
FEMALE = 'Female'

GENDER_CHOICE = [
  (MALE, MALE),
  (FEMALE, FEMALE),
]
class Person(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICE)
    age = models.IntegerField(default=5)
