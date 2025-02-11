from django.db import models

class User(models.Model):
    Full_name = models.CharField(max_length=100)  
    Student_Id = models.IntegerField(unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.Full_name 
