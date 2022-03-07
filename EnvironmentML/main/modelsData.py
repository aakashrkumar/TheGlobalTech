from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name='User', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="profiles")  # or whatever
    role = models.CharField(max_length=200, default="")
    bio = models.TextField(default="")
    slug = models.CharField(max_length=300)

    def save(self, *args, **kwargs):
        base_slug = self.user.first_name + "-" + self.user.last_name
        counter = 1
        slug = base_slug
        while UserProfile.objects.filter(slug=slug).exists():
            counter += 1
            slug = f"{base_slug}-{counter}"
        self.slug = slug
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
