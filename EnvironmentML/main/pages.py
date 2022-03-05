from django.db import models
from django.contrib.auth.models import User
from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from .modelsData import *


class HomePage(Page):
    """
    Homepage model
    """
    # define custom template file
    template = "main/home.html"
    projects = Project.objects.all()

    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return super(HomePage, cls).can_create_at(parent) \
               and not cls.objects.exists()


class ProjectsPage(Page):
    """
    ProjectsPage model
    """
    # define custom template file
    template = "main/projects.html"
    projects = Project.objects.all()

    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return super(ProjectsPage, cls).can_create_at(parent) \
               and not cls.objects.exists()


class AboutUSPage(Page):
    """
    ProjectsPage model
    """
    # define custom template file
    template = "main/aboutus.html"
    team = User.objects.all().filter(is_staff=True)

    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return super(AboutUSPage, cls).can_create_at(parent) \
               and not cls.objects.exists()


class ProjectPage(Page):
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
        ImageChooserPanel('feed_image'),
    ]

    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return type(parent) == ProjectsPage


class AuthorPage(Page):
    """
    AuthorPage model
    """
    # define custom template file
    template = "main/author.html"
    author = UserProfile.objects.get(username=Page.slug)

    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return super(AuthorPage, cls).can_create_at(parent) \
               and not cls.objects.exists()


class ProjectPageRelatedLink(Orderable):
    page = ParentalKey(ProjectPage, on_delete=models.CASCADE, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]


def load():
    pass
