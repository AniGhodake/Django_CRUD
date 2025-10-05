from django.db import models

# Create your models here.
class Student(models.Model):
    Gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    name = models.CharField(max_length = 100)
    email = models.EmailField()
    course = models.CharField(max_length = 100)

    gender = models.CharField(max_length = 1, choices = Gender_choices, default = 'M' )


    hobbies = models.CharField(max_length = 255, blank = True)

    is_active = models.BooleanField(default= True)



    def get_hobby_list(self):
        """ Return hobbies as Python list for display/edit. """
        return self.hobbies.split(',') if self.hobbies else []
    

    def __str__(self):
        return self.name