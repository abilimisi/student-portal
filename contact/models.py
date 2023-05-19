from django.db import models

# Create your models here.

class Cancer(models.Model):
    username=models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    calender = models.CharField(max_length=50)
    dateofbirth = models.CharField(max_length=50)
    dateoftime = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    pass1 = models.CharField(max_length=50)
    pass2 = models.CharField(max_length=50)

    def __str__(self):
        return (self.username)



