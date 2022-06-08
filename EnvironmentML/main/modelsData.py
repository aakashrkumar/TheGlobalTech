from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db.models import Q


class Project(models.Model):
    project_name = models.CharField(max_length=200)
    project_date = models.DateTimeField('Date Completed')
    project_summary = models.TextField()
    project_article = models.TextField()
    project_image = models.ImageField(upload_to='project_images/')
    project_authors = models.ManyToManyField(User, related_name='project_authors')
    slug = models.CharField(max_length=300)

    def get_project_authors(self):
        return ",".join([str(p) for p in self.project_authors.all()])

    def __str__(self):
        return self.project_name


class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name='User', on_delete=models.CASCADE)
    profile = models.ImageField(upload_to="profiles")  # or whatever
    role = models.CharField(max_length=200, default="")
    info = models.TextField(default="")
    url = models.CharField(max_length=300)

    def save(self, *args, **kwargs):
        base_url = self.user.first_name.lower() + "-" + self.user.last_name.lower()
        counter = 1
        url = base_url
        while UserProfile.objects.filter(url=url).filter(~Q(user__id=self.user.id)).exists():
            counter += 1
            url = f"{base_url}-{counter}"
        self.url = url
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Volunteers(models.Model):
    verified = models.BooleanField(default=False)
    joined_on = models.DateTimeField('Date Joined')
    user = models.OneToOneField(User, verbose_name='User', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    # plural name of the model
    class Meta:
        verbose_name_plural = "Volunteers"
