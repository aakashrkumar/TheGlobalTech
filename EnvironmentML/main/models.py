from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Project(models.Model):
    project_name = models.CharField(max_length=200)
    project_date = models.DateTimeField('Date Completed')
    project_summary = models.TextField()
    project_article = models.TextField()
    project_image = models.ImageField(upload_to='project_images/')
    project_authors = models.ManyToManyField(User, related_name='Users')
    slug = models.CharField(max_length=300)

    def __str__(self):
        return self.project_name
