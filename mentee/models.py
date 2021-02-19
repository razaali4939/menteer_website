from django.db import models

# Create your models here.
class Mentee_Profile(models.Model):
    mentee_id=models.CharField(max_length=50)
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    gender=models.CharField(max_length=15)
    date_of_birth = models.DateField(auto_now_add=True, null = True)
    phone=models.CharField(max_length=20)
    State=models.CharField(max_length=100)
    country=models.CharField(max_length=100)

    class Meta:
        db_table='Mentee'