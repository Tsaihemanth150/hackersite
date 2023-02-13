from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    email = models.EmailField(User)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=500)
    mobile = models.CharField(max_length=20, null=False)
    nationality = models.CharField(max_length=40, null=True)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.user.first_name



