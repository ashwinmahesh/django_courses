from __future__ import unicode_literals
from django.db import models

class CourseManager(models.Manager):
    def validate(self, postData):
        errors={}
        if(len(postData['name'])==0):
            errors['name']='Course name cannot be empty'
        if(len(postData['description'])==0):
            errors['description']='Course description cannot be empty'
        return errors

class Course(models.Model):
    name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    created_at_clean=models.CharField(max_length=255, default='FFFFFF')
    description=models.TextField()

    objects=CourseManager()

# Create your models here.
