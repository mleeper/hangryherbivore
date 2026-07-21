from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.models import Page
from wagtail.api import APIField
from wagtail.fields import RichTextField
from wagtail.snippets.models import register_snippet
from recipes.models import Category

# import MultiFieldPanel:
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, MultipleChooserPanel

class CTA(models.Model):
    text = models.CharField(
        null=True,
        blank=True,
        verbose_name="Call to action text",
        max_length=255,
        help_text="Text to display on Call to Action",
    )
    link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Hero Primary CTA link",
        help_text="Choose a page to link to for the Call to Action",
    )

    panels = [
        FieldPanel("text"),
        FieldPanel("link")
    ]

class HeroCTA(CTA):
    page = ParentalKey(
        "home.HomePage",
        related_name="hero_cta",
        on_delete=models.CASCADE
    )

class HowItWorksCTA(CTA):
    page = ParentalKey(
        "home.HomePage",
        related_name="how_it_works_cta",
        on_delete=models.CASCADE
    )

class AboutCTA(CTA):
    page = ParentalKey(
        "home.HomePage",
        related_name="about_cta",
        on_delete=models.CASCADE
    )

@register_snippet
class ValueBarItem(models.Model):
    icon = models.CharField(max_length=10)
    text = models.CharField(max_length=100)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return self.text

    panels = [
        FieldPanel('icon'),
        FieldPanel('text'),
        FieldPanel('sort_order'),
    ]

class HomePageValueBarItem(models.Model):
    page = ParentalKey(
        "home.HomePage",
        related_name="homepage_value_bar",
        on_delete=models.CASCADE
    )
    value_bar_item = models.ForeignKey(
        "home.ValueBarItem",
	    null=True,
	    blank=True,
        on_delete=models.CASCADE,
        related_name="+"
    )
    panels = [
        FieldPanel('value_bar_item')
    ]

@register_snippet
class HowItWorksItem(models.Model):
    icon = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=100)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
    
    def __str__(self):
        return self.title

    panels = [
        FieldPanel('title'),
        FieldPanel('icon'),
        FieldPanel('text'),
        FieldPanel('sort_order'),
    ]

class HomePageHowItWorksItem(models.Model):
    page = ParentalKey(
        "home.HomePage",
        related_name="how_it_works_list",
        on_delete=models.CASCADE
    )

    how_it_works_item = models.ForeignKey(
        "home.HowItWorksItem",
	    null=True,
	    blank=True,
        on_delete=models.CASCADE,
        related_name="+"
    )

    panels = [
        FieldPanel('how_it_works_item')
    ]

class HomePage(Page):
    # add the Hero section of HomePage:
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Hero image",
    )
    hero_title = models.CharField(
        blank=True,
        null=True,
        max_length=255, help_text="Write a header for the hero section"
    )
    hero_subtitle = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text="Write a short blurb for the hero section"
    )
    how_it_works_title = models.CharField(
        null=True,
        blank=True,
        verbose_name="How it works title",
        max_length=255,
        help_text="Title text for how it works",
    )
    how_it_works_text = models.CharField(
        null=True,
        blank=True,
        verbose_name="How it works description",
        max_length=255,
        help_text="Short description for how it works",
    )
    about_title = models.CharField(
        null=True,
        blank=True,
        verbose_name="About Title",
        max_length=255,
        help_text="Write a title for the about section",
    )
    about_content = RichTextField(blank=True)
    
    email_signup_title = models.CharField(
        null=True,
        blank=True,
        verbose_name="Email Signup Title",
        max_length=255,
        help_text="Write a title for the email signup",
    )   
    email_signup_content = RichTextField(blank=True)
    email_signup_button_text = models.CharField(
        null=True,
        blank=True,
        help_text="Button text for email signup"
    )

    # modify your content_panels:
    content_panels = Page.content_panels + [
        FieldPanel("hero_image"),
        FieldPanel("hero_title"),
        FieldPanel("hero_subtitle"),
        InlinePanel(
            "hero_cta",
            label="Hero CTA",
            max_num=2
        ),
        MultipleChooserPanel(
            "homepage_value_bar",
            label="Value Bar",
            chooser_field_name="value_bar_item",
            min_num=1,
            max_num=5
        ),
        FieldPanel('how_it_works_title'),
        FieldPanel('how_it_works_text'),
        InlinePanel(
            "how_it_works_cta",
            label="How It Works CTA",
            max_num=2
        ),
        MultipleChooserPanel(
            "how_it_works_list",
            label="How it works list",
            chooser_field_name="how_it_works_item",
            min_num=1,
            max_num=6
        ),
        FieldPanel("about_title"),
        FieldPanel("about_content"),
        InlinePanel(
            "about_cta",
            label="About CTA",
            max_num=1
        ),
       FieldPanel("email_signup_title"),
       FieldPanel("email_signup_content"),
	   FieldPanel("email_signup_button_text"),
    ]

    # ---------- Helpers ----------
    def get_schema_value_bar(self):
        return [
            {
                "icon": item.icon,
                "text": item.text,
            }
            for item in self.homepage_value_bar.all()
        ]
    
    def get_schema_hero_cta(self):
        return [
            {
                "text": cta.text,
                "link": cta.link,
            }
            for cta in self.hero_cta.all()
        ]

    def get_schema_about_cta(self):
        return [
            {
                "text": cta.text,
                "link": cta.link,
            }
            for cta in self.about_cta.all()
        ]
    
    def get_schema_how_it_works_cta(self):
        return [
            {
                "text": cta.text,
                "link": cta.link,
            }
            for cta in self.how_it_works_cta.all()
        ]
    
    def get_schema_how_it_works_list(self):
        return [
            {
                "icon": item.icon,
                "title": item.title,
                "text": item.text,
            }
            for item in self.how_it_works_list.all()
        ]

    def get_schema_categories(self):
        return [
            {
                "name": category.name,
                "icon": category.icon,
                "description": category.description,
            }
            for category in Category.objects.all()
        ]