from django.db import models

# Create your models here.
class Suscriber(models.Model):
    email = models.EmailField(unique=True)
    is_removed = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add = True,  blank = True)
    update_date = models.DateTimeField(auto_now = True, blank = True)
