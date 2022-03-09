from django.contrib import messages
from django.shortcuts import redirect, render
from wagtail.contrib.routable_page.models import route
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
    subpage_types = []
    parent_page_types = ['ProjectsPage']

    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return type(parent) == ProjectsPage

    @property
    def get_tags(self):
        """
        Similar to the authors function above we're returning all the tags that
        are related to the blog post into a list we can access on the template.
        We're additionally adding a URL to access BlogPage objects with that tag
        """
        tags = self.tags.all()
        for tag in tags:
            tag.url = '/' + '/'.join(s.strip('/') for s in [
                self.get_parent().url,
                'tags',
                tag.slug
            ])
        return tags

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


class ProjectsPage(Page):
    """
    ProjectsPage model
    """
    # define custom template file
    template = "main/projects_page.html"
    projectPages = ProjectPage.objects.all().filter(live=True).order_by('-date')
    subpage_types = ['ProjectPage']

    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return super(ProjectsPage, cls).can_create_at(parent) \
               and not cls.objects.exists()

    def children(self):
        return self.get_children().specific().live()

    def get_context(self, request):
        context = super(ProjectsPage, self).get_context(request)
        context['posts'] = ProjectPage.objects.descendant_of(
            self).live().order_by(
            '-date')
        return context

    @route(r'^tags/$', name='tag_archive')
    @route(r'^tags/([\w-]+)/$', name='tag_archive')
    def tag_archive(self, request, tag=None):

        try:
            tag = Tag.objects.get(slug=tag)
        except Tag.DoesNotExist:
            if tag:
                msg = 'There are no projects tagged with "{}"'.format(tag)
                messages.add_message(request, messages.INFO, msg)
            return redirect(self.url)

        posts = self.get_posts(tag=tag)
        context = {
            'tag': tag,
            'posts': posts
        }
        return render(request, 'main/projects_page.html', context)

    def serve_preview(self, request, mode_name):
        # Needed for previews to work
        return self.serve(request)

    # Returns the child BlogPage objects for this BlogPageIndex.
    # If a tag is used then it will filter the posts by tag.
    def get_posts(self, tag=None):
        posts = ProjectPage.objects.live().descendant_of(self)
        if tag:
            posts = posts.filter(tags=tag)
        return posts

    # Returns the list of Tags for all child posts of this BlogPage.
    def get_child_tags(self):
        tags = []
        for post in self.get_posts():
            # Not tags.append() because we don't want a list of lists
            tags += post.get_tags
        tags = sorted(set(tags))
        return tags


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
