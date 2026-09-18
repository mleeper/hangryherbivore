from django.db import models
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.api import APIField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index


# ----------------------------
# Blog Category Snippet
# ----------------------------
@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text="URL friendly version of the name"
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Short description of this category"
    )
    icon = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Emoji icon for this category"
    )
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('description'),
        FieldPanel('icon'),
        FieldPanel('sort_order'),
    ]


# ----------------------------
# Blog Post Tag
# ----------------------------
class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPost',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


# ----------------------------
# Blog Index Page
# ----------------------------
class BlogIndexPage(Page):
    subtitle = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Short description shown under the title"
    )
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Hero image for the blog index"
    )

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("hero_image"),
    ]

    subpage_types = ['blog.BlogPost']

    def get_posts(self, category=None, tag=None):
        posts = BlogPost.objects.live().descendant_of(self).order_by(
            '-first_published_at'
        )
        if category:
            posts = posts.filter(categories__slug=category)
        if tag:
            posts = posts.filter(tags__slug=tag)
        return posts

    def get_context(self, request):
        context = super().get_context(request)
        category = request.GET.get('category')
        tag = request.GET.get('tag')
        context['posts'] = self.get_posts(category=category, tag=tag)
        context['categories'] = BlogCategory.objects.all()
        return context

    api_fields = [
        APIField('subtitle'),
        APIField('hero_image'),
    ]

    class Meta:
        verbose_name = "Blog Index Page"


# ----------------------------
# Blog Post
# ----------------------------
class BlogPost(Page):
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Hero image for this post"
    )
    excerpt = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Short summary shown on the blog index"
    )
    content = RichTextField(
        blank=True,
        help_text="Main content of the blog post"
    )

    # Tags via taggit
    tags = ClusterTaggableManager(
        through=BlogPostTag,
        blank=True
    )

    # Categories via snippet
    categories = ParentalManyToManyField(
        'blog.BlogCategory',
        blank=True,
        related_name='posts'
    )

    search_fields = Page.search_fields + [
        index.SearchField('content'),
        index.SearchField('excerpt'),
        index.FilterField('categories'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("hero_image"),
        FieldPanel("excerpt"),
        FieldPanel("content"),
        MultiFieldPanel([
            FieldPanel("categories"),
            FieldPanel("tags"),
        ], heading="Categorization"),
    ]

    parent_page_types = ['blog.BlogIndexPage']
    subpage_types = []

    api_fields = [
        APIField('hero_image'),
        APIField('excerpt'),
        APIField('content'),
        APIField('tags'),
        APIField('categories'),
    ]

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"