from django.db import models

# Add these:
from wagtail.models import Page
from wagtail.fields import RichTextField

class RecipesIndexPage(Page):
	intro = RichTextField(blank=True)
	content_panels = Page.content_panels + ["intro"]

class RecipesPage(Page):
	intro = RichTextField(blank=True)
	main_image=models.ForeignKey(
		"wagtailimages.Image",
        	null=True,
        	blank=True,
        	on_delete=models.SET_NULL,
        	related_name="+",
        	help_text="Recipe Image",
	)
	secondary_image=models.ForeignKey(
		"wagtailimages.Image",
        	null=True,
        	blank=True,
        	on_delete=models.SET_NULL,
        	related_name="+",
        	help_text="Recipe Image",
	)
	category = models.CharField(
		blank=True,
		max_length=255,
		help_text="Recipe Category"
	)	
	cook_time=models.CharField(
		blank=True,
		max_length=255,
		help_text="Recipe Cook Time"
	)
	calories=models.CharField(
		blank=True,
		max_length=255,
		help_text="Recipe Calories"
	)
	servings=models.CharField(
		blank=True,
		max_length=255,
		help_text="Recipe Cook Time"
	)
	nutrition=RichTextField(blank=True)
	ingredients=RichTextField(blank=True)
	body=RichTextField(blank=True)
	notes=RichTextField(blank=True)
	content_panels = Page.content_panels + [
		"intro",
		"main_image",
		"secondary_image",
		"category",
		"cook_time",
		"calories",
		"servings",
		"nutrition",
		"ingredients",
		"body",
		"notes"
	]
