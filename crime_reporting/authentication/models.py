from django.db import models

from django.contrib.auth.models import AbstractUser

import uuid

# Create your models here.

class BaseClass(models.Model):

    uuid = models.SlugField(default=uuid.uuid4,unique=True)

    active_status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        abstract = True




# Create your models here.

class RoleChoices(models.TextChoices):

    USER = 'User','User'

    ADMIN = 'Admin','Admin'

class Profile(AbstractUser):

    photo = models.FileField(upload_to='profile pictures/')

    role = models.CharField(max_length=25,choices=RoleChoices.choices)
    
    def __str__(self):

        return f'{self.username}'
    
    class Meta:

        verbose_name = 'Profile'

        verbose_name_plural = 'Profile'      
