from django.db import models
from wagtail.api import APIField
from wagtail import blocks
from wagtail.models import Page, Orderable
from wagtail.fields import StreamField, RichTextField
from wagtail.images.models import Image
from wagtail.admin.panels import FieldPanel, MultipleChooserPanel, MultiFieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from wagtail.snippets.models import register_snippet
from wagtail.snippets.widgets import AdminSnippetChooser
from wagtail.search import index
from modelcluster.models import ClusterableModel

UNIT_CHOICES = [
    # Volume
    ('ml', 'Milliliters (ml)'),
    ('l', 'Liters (l)'),
    ('tsp', 'Teaspoons (tsp)'),
    ('tbsp', 'Tablespoons (tbsp)'),
    ('cup', 'Cups'),
    ('fl_oz', 'Fluid Ounces (fl oz)'),
    # Weight
    ('g', 'Grams (g)'),
    ('mg','Milligrams (mg)'),
    ('mcg','Micrograms (mcg)'),
    ('kg', 'Kilograms (kg)'),
    ('oz', 'Ounces (oz)'),
    ('lb', 'Pounds (lb)'),
    # Abstract Counts
    ('piece', 'Piece(s)'),
    ('can', 'Can(s)'),
    ('pinch', 'Pinch(es)'),
    ('clove', 'Clove(s)'),
    ('head', 'Head(s)'),
]
CATEGORIES = [
    ('Breakfast', 'Breakfast'),
    ('Lunch', 'Lunch'),
    ('Dinner', 'Dinner'),
    ('Dessert', 'Dessert'),
    ('snacks_sides', 'Snacks & Sides'),
    ('sauce', 'Sauces & Spreads'),
    ('dutch_oven' 'Dutch Oven & One Pot'),
    ('five_ingredients_or_less', 'Five Ingredients or Less'),
    ('quick_meals', 'Under 30 Minutes'),
    ('high_protein', 'High Protein'),
]
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
# Category Snippet
# ----------------------------
@register_snippet
class Category(index.Indexed, models.Model):
    name = models.CharField(max_length=100)

    search_fields = [
	index.SearchField('name'),
	index.AutocompleteField('name')
    ]
    
    def __str__(self):
        return f"{self.name}"

#-------------------------------
class RecipeCategory(models.Model): 
    page = ParentalKey(
        "recipes.RecipePage",
        related_name="recipe_category",
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
    	'recipes.Category',
	blank=True,
	null=True,
	related_name='+',
	on_delete=models.CASCADE
    )
    
    panels = [
        FieldPanel('category'),
    ]

# ----------------------------
# Nutrient Snippet
# ----------------------------
@register_snippet
class Nutrient(index.Indexed, models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField( 
        max_length=20,
        choices=UNIT_CHOICES,
        blank=True,
        null=True,
        help_text="Standardized unit of measurement"
    )

    search_fields = [
        index.SearchField('name'),
        index.AutocompleteField('name'),
    ]

    def __str__(self):
        return f"{self.name} ({self.unit})"

# ---------------------------------
# Ingredient Nutrient Relationship
# ---------------------------------
class IngredientNutrientRelationship(Orderable):
    # ParentalKey points upward to the Ingredient Snippet
    ingredient = ParentalKey(
        'Ingredient', 
        related_name='ingredient_nutrients', 
        on_delete=models.CASCADE
    )
    # ForeignKey links to your master Nutrient snippet
    nutrient = models.ForeignKey(
        'Nutrient', 
        on_delete=models.CASCADE, 
        related_name='+'
    )
    # The unique numeric weight for this specific ingredient
    amount = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        default=0.00
    )

    serving_size = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        default=0.00
    )
    panels = [
        # Explicit widget declaration forces the search box to always be visible
        FieldPanel('nutrient', widget=AdminSnippetChooser(Nutrient)),
        FieldPanel('amount'),
	FieldPanel('serving_size'),
    ]


# ----------------------------
# Ingredient Snippet
# ----------------------------

@register_snippet
class Ingredient(index.Indexed, ClusterableModel):
    name = models.CharField(max_length=100)
    
    search_fields = [
        index.SearchField('name'),
        index.AutocompleteField('name'),
    ]

    panels = [
        FieldPanel("name"),
	# The hybrid approach: Bulk choice panel mapped to an inline relationship
        MultipleChooserPanel(
            'ingredient_nutrients',        # Matches the related_name on the bridge model
            chooser_field_name='nutrient', # Matches the ForeignKey target field
            label="Nutritional Breakdown",
        ),
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
	null=True,
	blank=True,
        on_delete=models.CASCADE,
        related_name="+"
    )
    quantity = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
        blank=True,
        null=True,
        help_text="Standardized unit of measurement"
    )
    note = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        help_text="e.g. chopped, sifted, divided, or 'to taste' if qty is empty"
    )
    panels = [
        FieldPanel("ingredient"),
        FieldPanel("quantity"),
	FieldPanel("unit"),
	FieldPanel("note"),
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
    #category = models.CharField(max_length=50, default="Dinner")
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
            #FieldPanel("category"),
            FieldPanel("difficulty"),
        ], heading="Classification"),
	
        MultipleChooserPanel(
            "recipe_category",
            label="Category",
            chooser_field_name="category",
        ),

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

        MultipleChooserPanel(
            "recipe_ingredients",
            label="Ingredients",
            chooser_field_name="ingredient",
            min_num=1
        ),
        
        InlinePanel(
            "steps",
            label="Instructions",
            min_num=1
        ),
    ]

    #api_fields = [
    #    APIField('ingredients'),           # Full JSON for your main Astro component
    #    APIField('schema_ingredients'),    # Clean strings for your SEO Schema logic
    #]

    # ---------- Helpers ----------

    def get_seo_title(self):
        return self.seo_title or self.title


    def get_meta_description(self):
        return self.meta_description or self.description[:155]


    def get_total_time_iso(self):
        return f"PT{self.total_time}M"
    
    def get_schema_ingredients(self):
        data = []
    
        for i in self.recipe_ingredients.all():
            if not i.ingredient:
                continue
            
        # Safely capture your clean numeric quantity
        recipe_qty = float(i.quantity) if i.quantity is not None else 0.0
            
        ingredient_data = {
            "name": i.ingredient.name,
            "quantity": recipe_qty,
            "unit": i.get_unit_display() if i.unit else "", # Returns human-friendly text like "Fluid Ounces (fl oz)"
            "unit_code": i.unit or "",                       # Returns the raw database string like "fl_oz"
            "note": i.note or "",
            "nutrients": []
        }
        
        nutrients_list = i.ingredient.ingredient_nutrients.values(
            'nutrient__name', 
            'amount', 
            'nutrient__unit',
            'serving_size'
        )
        
        for n in nutrients_list:
            serving_size_float = float(n['serving_size']) if n['serving_size'] is not None else 0.0
            base_amount_float = float(n['amount']) if n['amount'] is not None else 0.0
            
            # Straightforward, bulletproof math scaling
            if serving_size_float > 0 and recipe_qty > 0:
                scale_factor = recipe_qty / serving_size_float
                scaled_amount = round(base_amount_float * scale_factor, 2)
            else:
                scale_factor = 1.0
                scaled_amount = base_amount_float
            
            ingredient_data["nutrients"].append({
                "name": n['nutrient__name'],
                "unit": n['nutrient__unit'],
                "base_serving_size": serving_size_float,
                "base_nutrient_amount": base_amount_float,
                "scaled_nutrient_amount": scaled_amount,
                "scale_factor_applied": round(scale_factor, 2)
            })
            
        data.append(ingredient_data)
        
        return data
    
    def get_recipe_total_nutrition(self):
        totals = {}
        ingredients_payload = self.get_schema_ingredients()
    
        # Loop over the calculated payload we made in the previous step
        for ingredient in ingredients_payload:
            for nutrient in ingredient["nutrients"]:
                name = nutrient["name"]
                unit = nutrient["unit"]
                amount = nutrient["scaled_nutrient_amount"]
            
                # Initialize the dict key if it doesn't exist yet
                if name not in totals:
                    totals[name] = {"amount": 0.0, "unit": unit}
                
                totals[name]["amount"] = round(totals[name]["amount"] + amount, 2)
            
        return totals

    def get_schema_instructions(self):
        return [
            {
                "@type": "HowToStep",
                "text": step.instruction
            }
            for step in self.steps.all()
        ]

