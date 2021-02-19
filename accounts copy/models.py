from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.dispatch import receiver

class Country(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

# Create your models here.
class Profile(models.Model):
    fname = models.CharField(max_length=255, null=True)
    lname = models.CharField(max_length=255, null=True)
    MALE= 1
    FEMALE = 2
    TRANS= 3
    GENDER_CHOICE=(
        (MALE,'Male'),
        (FEMALE,'Female'),
        (TRANS,'TRANS')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=False, unique=True)
    picture=models.ImageField(null=True, upload_to = 'courses/static/courses/images/users/', default = 'courses/static/courses/images/users/default_user.png')
    linkedin_url =  models.URLField(null=True, max_length=250)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICE, null=True, blank=True)

#Always create a user profile for anyone who signs up    
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)