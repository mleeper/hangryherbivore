from django.core.management.base import BaseCommand
from blog.models import BlogCategory


class Command(BaseCommand):
    help = 'Load initial blog categories'

    CATEGORIES = [
        {
            'name': 'Budget Tips',
            'slug': 'budget-tips',
            'icon': '💸',
            'description': 'Smart ways to stretch your grocery budget further.',
            'sort_order': 1,
        },
        {
            'name': 'Meal Planning',
            'slug': 'meal-planning',
            'icon': '📋',
            'description': 'Plan your week, reduce waste, and save time.',
            'sort_order': 2,
        },
        {
            'name': 'Grocery Guides',
            'slug': 'grocery-guides',
            'icon': '🛒',
            'description': 'What to buy, where to buy it, and how to store it.',
            'sort_order': 3,
        },
        {
            'name': 'Kitchen Skills',
            'slug': 'kitchen-skills',
            'icon': '🔪',
            'description': 'Techniques and tips to make cooking easier and faster.',
            'sort_order': 4,
        },
        {
            'name': 'Nutrition',
            'slug': 'nutrition',
            'icon': '🥦',
            'description': 'Understanding nutrients and eating well on a budget.',
            'sort_order': 5,
        },
        {
            'name': 'Recipe Roundups',
            'slug': 'recipe-roundups',
            'icon': '📖',
            'description': 'Curated collections of recipes around a theme.',
            'sort_order': 6,
        },
        {
            'name': 'Ingredient Spotlights',
            'slug': 'ingredient-spotlights',
            'icon': '🌿',
            'description': 'Deep dives into budget staple ingredients.',
            'sort_order': 7,
        },
        {
            'name': 'Seasonal Eating',
            'slug': 'seasonal-eating',
            'icon': '🍂',
            'description': 'Eating with the seasons to save money and eat fresher.',
            'sort_order': 8,
        },
    ]

    def handle(self, *args, **kwargs):
        created_count = 0
        updated_count = 0

        for cat in self.CATEGORIES:
            obj, created = BlogCategory.objects.update_or_create(
                slug=cat['slug'],
                defaults={
                    'name': cat['name'],
                    'icon': cat['icon'],
                    'description': cat['description'],
                    'sort_order': cat['sort_order'],
                }
            )

            if created:
                created_count += 1
                self.stdout.write(f'  ✓ Created: {obj.name}')
            else:
                updated_count += 1
                self.stdout.write(f'  ~ Updated: {obj.name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Done — {created_count} created, {updated_count} updated'
            )
        )