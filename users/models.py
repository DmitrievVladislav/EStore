from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"id: {self.id}, username: {self.username}, FIO: {self.first_name} {self.last_name}, superuser: {self.is_superuser}")




# Create your models here.
