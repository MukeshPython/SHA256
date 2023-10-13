from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100, blank=True, null=True)
    salt = models.CharField(max_length=100, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'user'
