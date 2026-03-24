from django.db import models

from wagtail.models import Page
from wagtail.api import APIField
from wagtail.fields import RichTextField

# import MultiFieldPanel:
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

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
        max_length=255, help_text="Write a header for the hero section"
    )
    hero_subtitle = models.CharField(
        blank=True,
        max_length=255,
        help_text="Write a short blurb for the hero section"
    )
    hero_primary_cta = models.CharField(
        blank=True,
        verbose_name="Hero Primary CTA",
        max_length=255,
        help_text="Text to display on Call to Action",
    )
    hero_primary_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Hero Primary CTA link",
        help_text="Choose a page to link to for the Call to Action",
    )
    hero_secondary_cta = models.CharField(
        blank=True,
        verbose_name="Hero Secondary CTA",
        max_length=255,
        help_text="Text to display on Call to Action",
    )
    hero_secondary_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Hero Secondary CTA link",
        help_text="Choose a page to link to for the Secondary Call to Action",
    )
    
    highlights_title = models.CharField(
        blank=True,
        verbose_name="Highlights section title",
        max_length=255,
        help_text="Text to display in the highlight section title",
    )
    highlights_intro = RichTextField(blank=True)
    highlights_first_feature_title = models.CharField(
        blank=True,
        verbose_name="First Feature Title",
        help_text="First feature title"
    )
    highlights_first_feature_content = RichTextField(blank=True)
    highlights_second_feature_title = models.CharField(
        blank=True,
        verbose_name="Second Feature Title",
        help_text="Second feature title"
    )
    highlights_second_feature_content = RichTextField(blank=True)
    highlights_third_feature_title = models.CharField(
        blank=True,
        verbose_name="Third Feature Title",
        help_text="Third feature title"
    )
    highlights_third_feature_content = RichTextField(blank=True)
    
    featured_recipes_title = models.CharField(
        blank=True,
        verbose_name="Featured Recipes title",
        max_length=255,
        help_text="Featured Recipes Title",
    )
    featured_recipes_intro = RichTextField(blank=True)

    philosophy_title = models.CharField(
        blank=True,
        verbose_name="Philosophy Title",
        max_length=255,
        help_text="Title to highlight our approach",
    )
    philosophy_content = RichTextField(blank=True)
    
    about_title = models.CharField(
        blank=True,
        verbose_name="About Title",
        max_length=255,
        help_text="Write a title for the about section",
    )
    about_content = RichTextField(blank=True)
    
    budget_meals_title = models.CharField(
        blank=True,
        verbose_name="Budget Meals Title",
        max_length=255,
        help_text="Budget Meals Title",
    )
    budget_meals_content = RichTextField(blank=True)
    budget_meals_cta_text = models.CharField(
        blank=True,
        help_text="Call to action link text"
    )
    email_signup_title = models.CharField(
        blank=True,
        verbose_name="Email Signup Title",
        max_length=255,
        help_text="Write a title for the email signup",
    )   
    email_signup_content = RichTextField(blank=True)
    email_signup_button_text=models.CharField(
        blank=True,
        help_text="Button text for email signup"
    )

    api_fields = [
        APIField("hero_image"),
    	APIField("hero_title"),
    	APIField("hero_subtitle"),
    	APIField("hero_primary_cta"),
    	APIField("hero_primary_cta_link"),
    	APIField("hero_secondary_cta"),
    	APIField("hero_secondary_cta_link"),
    	APIField("highlights_title"),
    	APIField("highlights_intro"),
    	APIField("highlights_first_feature_title"),
    	APIField("highlights_first_feature_content"),
    	APIField("highlights_second_feature_title"),
    	APIField("highlights_second_feature_content"),
    	APIField("highlights_third_feature_title"),
    	APIField("highlights_third_feature_content"),
    	APIField("featured_recipes_title"),
    	APIField("featured_recipes_intro"),
    	APIField("philosophy_title"),
    	APIField("philosophy_content"),  
    	APIField("about_title"),
    	APIField("about_content"),
    	APIField("budget_meals_title"),
    	APIField("budget_meals_content"),
    	APIField("budget_meals_cta_text"),
    	APIField("email_signup_title"),
    	APIField("email_signup_content"),
    	APIField("email_signup_button_text"),
    ]

    # modify your content_panels:
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_image"),
                FieldPanel("hero_title"),
                FieldPanel("hero_subtitle"),
                FieldPanel("hero_primary_cta"),
                FieldPanel("hero_primary_cta_link"),
                FieldPanel("hero_secondary_cta"),
                FieldPanel("hero_secondary_cta_link"),
            ],
            heading="Hero section",
        ),
        MultiFieldPanel(
	    [
		FieldPanel("highlights_title"),
		FieldPanel("highlights_intro"),
		FieldPanel("highlights_first_feature_title"),
		FieldPanel("highlights_first_feature_content"),
		FieldPanel("highlights_second_feature_title"),
		FieldPanel("highlights_second_feature_content"),
		FieldPanel("highlights_third_feature_title"),
		FieldPanel("highlights_third_feature_content"),
	    ],
	    heading="What You'll Find Here Section"
        ),
        MultiFieldPanel(
            [
                FieldPanel("featured_recipes_title"),
                FieldPanel("featured_recipes_intro"),
            ],
            heading="Featured Recipes Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("philosophy_title"),
                FieldPanel("philosophy_content"),
            ],
            heading="How This Works Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("about_title"),
                FieldPanel("about_content"),
            ],
            heading="About section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("budget_meals_title"),
                FieldPanel("budget_meals_content"),
                FieldPanel("budget_meals_cta_text"),
            ],
            heading="Budget Meals Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("email_signup_title"),
                FieldPanel("email_signup_content"),
		FieldPanel("email_signup_button_text"),
            ],
            heading="Email Signup section",
        ),
    ]

