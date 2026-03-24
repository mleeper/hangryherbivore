from django.db import models

# Create your models here.

# Add these:
from wagtail.models import Page
from wagtail.fields import RichTextField

class BlogIndexPage(Page):
	intro=RichTextField(blank=True)
	content_panels = Page.content_panels + ["intro"]

class BlogPage(Page):
	intro=RichTextField(blank=True)
	blog_image=models.ForeignKey(
        	"wagtailimages.Image",
        	null=True,
        	blank=True,
        	on_delete=models.SET_NULL,
        	related_name="+",
        	help_text="Blog image",
	)
	body=RichTextField(blank=True)
	content_panels = Page.content_panels + ["intro", "blog_image", "body"]
    
