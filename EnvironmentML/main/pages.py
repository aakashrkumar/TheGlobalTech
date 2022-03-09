from wagtail.core.blocks import CharBlock, RichTextBlock, StructBlock

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.images.blocks import ImageChooserBlock

from wagtail_content_import.models import ContentImportMixin
from wagtailcodeblock.blocks import CodeBlock

from .modelsData import *
from .mapper import MyMapper, BaseStreamBlock
from wagtail.contrib.table_block.blocks import TableBlock
from taggit.models import Tag, TaggedItemBase

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager


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


class ProjectPageTag(TaggedItemBase):
    """
    This model allows us to create a many-to-many relationship between
    the BlogPage object and tags. There's a longer guide on using it at
    https://docs.wagtail.org/en/stable/reference/pages/model_recipes.html#tagging
    """
    content_object = ParentalKey('ProjectPage', related_name='tagged_items', on_delete=models.CASCADE)


class ProjectPage(Page, ContentImportMixin):
    # Database fields
    mapper_class = MyMapper

    date = models.DateField("Post date")

    subtitle = models.CharField(blank=True, max_length=255)
    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=False
    )

    body = StreamField([
        ('code', CodeBlock(label='Any code', default_language='python')),
        ('heading', CharBlock()),
        ('table', TableBlock()),
        ('paragraph', RichTextBlock())
    ])

    project_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    # Search index configuration

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('date'),
    ]

    # Editor panels configuration
    tags = ClusterTaggableManager(through=ProjectPageTag, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle', classname="full"),
        FieldPanel('introduction', classname="full"),
        FieldPanel('date'),
        InlinePanel('authors', label="Authors"),
        ImageChooserPanel('project_image'),
        StreamFieldPanel('body', classname="full"),
        InlinePanel('related_links', label="Related links"),
        FieldPanel('tags'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]

    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return type(parent) == ProjectsPage


class ProjectsPage(Page):
    """
    ProjectsPage model
    """
    # define custom template file
    template = "main/projects.html"
    projectPages = ProjectPage.objects.all().filter(live=True).order_by('-date')

    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return super(ProjectsPage, cls).can_create_at(parent) \
               and not cls.objects.exists()


class Authors(Orderable):
    page = ParentalKey(ProjectPage, on_delete=models.SET_NULL, related_name='authors', null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    panels = [
        FieldPanel('user'),
    ]


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


class InfoBlock(StructBlock):
    title = CharBlock()
    body = RichTextBlock()

    class Meta:
        icon = 'title'

    def get_context(self, value, parent_context=None):
        ctx = super().get_context(value, parent_context=parent_context)
        ctx['title'] = value['title']
        ctx['body'] = value['body']
        return ctx


class HomePage(Page):
    """
    Homepage model
    """
    # define custom template file
    template = "main/home.html"
    projectPages = ProjectPage.objects.filter(live=True).order_by('-date')

    info_structs = StreamField([
        ('info_block', InfoBlock())
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('info_structs'),
    ]

    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return super(HomePage, cls).can_create_at(parent) \
               and not cls.objects.exists()
