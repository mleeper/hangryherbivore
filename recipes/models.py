from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.images.models import Image
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from wagtail.snippets.models import register_snippet


# ----------------------------
# Recipe Index
# ----------------------------

class RecipeIndexPage(Page):
    intro = RichTextField(blank=True)

    subpage_types = ["recipes.RecipePage"]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]


# ----------------------------
# Ingredient Snippet
# ----------------------------

@register_snippet
class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    panels = [
        FieldPanel("name")
    ]

    def __str__(self):
        return self.name


# ----------------------------
# Recipe Ingredient Relation
# ----------------------------

class RecipeIngredient(models.Model):
    page = ParentalKey(
        "recipes.RecipePage",
        related_name="recipe_ingredients",
        on_delete=models.CASCADE
    )

    ingredient = models.ForeignKey(
        "recipes.Ingredient",
        on_delete=models.CASCADE
    )

    amount = models.CharField(
        max_length=50,
        help_text="e.g. 1 cup, 200g, 2 tbsp"
    )

    panels = [
        FieldPanel("amount"),
        FieldPanel("ingredient")
    ]


# ----------------------------
# Instruction Step
# ----------------------------

class RecipeStep(models.Model):
    page = ParentalKey(
        "recipes.RecipePage",
        related_name="steps",
        on_delete=models.CASCADE
    )

    step_number = models.IntegerField()
    instruction = models.TextField()

    panels = [
        FieldPanel("step_number"),
        FieldPanel("instruction")
    ]

    ordering = ["step_number"]


# ----------------------------
# Main Recipe Page
# ----------------------------

class RecipePage(Page):

    # ---------- SEO ----------
    #seo_title = models.CharField(
    #    max_length=60,
    #    help_text="Custom title for Google (60 chars max)",
    #    blank=True
    #)

    meta_description = models.CharField(
        max_length=160,
        help_text="Shown in Google results",
        blank=True
    )

    focus_keyword = models.CharField(
        max_length=100,
        blank=True,
        help_text="Primary SEO keyword"
    )


    # ---------- Core ----------
    description = models.TextField()
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )


    # ---------- Timing ----------
    prep_time = models.PositiveIntegerField(help_text="Minutes")
    cook_time = models.PositiveIntegerField(help_text="Minutes")
    total_time = models.PositiveIntegerField(
        help_text="Prep + Cook (minutes)"
    )


    # ---------- Servings ----------
    servings = models.PositiveIntegerField()
    cost_per_serving = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="USD cost per serving",
        null=True,
        blank=True
    )


    # ---------- Nutrition ----------
    calories = models.PositiveIntegerField(null=True, blank=True)
    protein = models.PositiveIntegerField(null=True, blank=True)
    carbs = models.PositiveIntegerField(null=True, blank=True)
    fat = models.PositiveIntegerField(null=True, blank=True)


    # ---------- Classification ----------
    cuisine = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=50, default="Dinner")
    difficulty = models.CharField(
        max_length=20,
        choices=[
            ("easy", "Easy"),
            ("medium", "Medium"),
            ("hard", "Hard")
        ],
        default="easy"
    )


    # ---------- Monetization ----------
    affiliate_product = models.URLField(
        blank=True,
        help_text="Primary affiliate link (tool/ingredient)"
    )

    sponsored = models.BooleanField(default=False)


    # ---------- Email Lead ----------
    lead_magnet_cta = models.CharField(
        max_length=100,
        blank=True,
        default="Get My Free Budget Meal Plan"
    )


    # ---------- Admin ----------
    content_panels = Page.content_panels + [

        MultiFieldPanel([
            FieldPanel("description"),
            FieldPanel("hero_image"),
        ], heading="Core Content"),


        MultiFieldPanel([
            FieldPanel("prep_time"),
            FieldPanel("cook_time"),
            FieldPanel("total_time"),
            FieldPanel("servings"),
            FieldPanel("cost_per_serving"),
        ], heading="Timing & Cost"),


        MultiFieldPanel([
            FieldPanel("calories"),
            FieldPanel("protein"),
            FieldPanel("carbs"),
            FieldPanel("fat"),
        ], heading="Nutrition"),


        MultiFieldPanel([
            FieldPanel("cuisine"),
            FieldPanel("category"),
            FieldPanel("difficulty"),
        ], heading="Classification"),


        MultiFieldPanel([
            FieldPanel("affiliate_product"),
            FieldPanel("sponsored"),
        ], heading="Monetization"),


        MultiFieldPanel([
            FieldPanel("seo_title"),
            FieldPanel("meta_description"),
            FieldPanel("focus_keyword"),
        ], heading="SEO"),


        MultiFieldPanel([
            FieldPanel("lead_magnet_cta"),
        ], heading="Email Growth"),


        InlinePanel(
            "recipe_ingredients",
            label="Ingredients",
            min_num=1
        ),

        InlinePanel(
            "steps",
            label="Instructions",
            min_num=1
        ),
    ]


    # ---------- Helpers ----------

    def get_seo_title(self):
        return self.seo_title or self.title


    def get_meta_description(self):
        return self.meta_description or self.description[:155]


    def get_total_time_iso(self):
        return f"PT{self.total_time}M"


    def get_schema_ingredients(self):
        return [
            f"{i.amount} {i.ingredient.name}"
            for i in self.recipe_ingredients.all()
        ]


    def get_schema_instructions(self):
        return [
            {
                "@type": "HowToStep",
                "text": step.instruction
            }
            for step in self.steps.all()
        ]

