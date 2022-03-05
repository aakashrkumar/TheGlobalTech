from django.db import models
from django.contrib.auth.models import User

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index


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

    def __str__(self):
        return self.user.username

    # plural name of the model
    class Meta:
        verbose_name_plural = "Volunteers"


class ArticlePage(Page):
    # Database fields
    body = RichTextField()
    date = models.DateField("Post date")
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    # Search index configuration

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('date'),
    ]

    # Editor panels configuration

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('body', classname="full"),
        InlinePanel('related_links', label="Related links"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        FieldPanel('feed_image'),
    ]

    # Parent page / subpage type rules
    parent_page_types = ['blog.BlogIndex']
    subpage_types = []
