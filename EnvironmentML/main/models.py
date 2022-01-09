from django.db import models


# Create your models here.


class Project(models.Model):
    project_name = models.CharField(max_length=200)
    project_date = models.DateTimeField('Date Completed')
    project_summary = models.TextField()
    project_article = models.TextField()
    project_image = models.ImageField(upload_to='project_images/')
    project_authors = models
    def __str__(self):
        return self.project_name
