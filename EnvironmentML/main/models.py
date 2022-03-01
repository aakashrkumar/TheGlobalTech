from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Project(models.Model):
    project_name = models.CharField(max_length=200)
    project_date = models.DateTimeField('Date Completed')
    project_summary = models.TextField()
    project_article = models.TextField()
    project_image = models.ImageField(upload_to='project_images/')
    project_authors = models.ManyToManyField(User, related_name='authors')
    slug = models.CharField(max_length=300)

    def get_project_authors(self):
        return ",".join([str(p) for p in self.project_authors.all()])

    def __str__(self):
        return self.project_name


class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name='User', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="profiles")  # or whatever
    role = models.CharField(max_length=200, default="")
    bio = models.TextField(default="")

    def __str__(self):
        return self.user.username


class Volunteers(models.Model):
    verified = models.BooleanField(default=False)
    joined_on = models.DateTimeField('Date Joined')
    user = models.OneToOneField(User, verbose_name='User', on_delete=models.CASCADE)
