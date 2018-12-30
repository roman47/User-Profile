from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.


class UserProfile(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dob = models.DateField()
    email = models.EmailField()
    confirm_email = models.EmailField()
    short_bio = models.TextField(validators=[MinLengthValidator(10)])
    avatar = models.ImageField(upload_to='documents/')

    def __str__(self):
        return self.first_name + " " + self.last_name
