from django.db import models
import random
import string

# Create your models here.

class user_detail(models.Model):
    objects =None
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    password = models.TextField(null=True, blank=True)
    referral_code = models.CharField(max_length=10,null=True, blank=True
                                     )
    points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "User_info"


