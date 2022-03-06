from django.db import models
from django.contrib.auth.models import User
from modelcluster.fields import ParentalKey
from wagtail.core.blocks import CharBlock, RichTextBlock

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.images.blocks import ImageChooserBlock

from wagtail.core import blocks
from wagtail_content_import.models import ContentImportMixin
from wagtailcodeblock.blocks import CodeBlock

from .modelsData import *
from .mapper import MyMapper, BaseStreamBlock
from wagtail.contrib.table_block.blocks import TableBlock


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
    AboutUSPage model
    """
    # define custom template file
    template = "main/aboutus.html"
    team = User.objects.all().filter(is_staff=True)

    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return super(AboutUSPage, cls).can_create_at(parent) \
               and not cls.objects.exists()


class ProjectPage(Page, ContentImportMixin):
    # Database fields
    mapper_class = MyMapper
    project_authors = models.ManyToManyField(User, related_name='authors')
    date = models.DateField("Post date")

    body = StreamField([('code', CodeBlock(label='Any code', default_language='python')), ('heading', CharBlock()), ('table', TableBlock()), ('paragraph', RichTextBlock())])

    project_image = models.ForeignKey(
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
        ImageChooserPanel('project_image'),
        FieldPanel('body', classname="full"),
        InlinePanel('related_links', label="Related links"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]

    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return type(parent) == ProjectsPage


class ProjectPageRelatedLink(Orderable):
    page = ParentalKey(ProjectPage, on_delete=models.CASCADE, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]


class AuthorPage(Page):
    """
    AuthorPage model
    """
    # define custom template file
    template = "main/author.html"
    author = ""

    def save(self, *args, **kwargs):
        """
        Override the save method to set the author of the page to the current user.
        """
        # Set the author to the current user
        self.author = UserProfile.objects.get(slug=self.slug)
        super(AuthorPage, self).save(*args, **kwargs)

    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return type(parent) == AboutUSPage


class PrivacyPolicyPage(Page):
    """
    PrivacyPolicy model
    """

    template = "main/privacypolicy.html"

    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return super(PrivacyPolicyPage, cls).can_create_at(parent) \
               and not cls.objects.exists()


class TermsPage(Page):
    """
    Terms model
    """

    template = "main/terms.html"

    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return super(TermsPage, cls).can_create_at(parent) \
               and not cls.objects.exists()
