const SITE = 'https://hangryherbivore.com';
const NAME = 'Hangry Herbivore';

const abs = (u) => (u ? (u.startsWith('http') ? u : `${SITE}${u}`) : undefined);
const iso = (m) => (m ? `PT${m}M` : undefined);
const clean = (o) => JSON.parse(JSON.stringify(o)); // drops undefined keys

export const publisher = { '@type': 'Organization', name: NAME, url: SITE };

export function websiteLd() {
    return clean({
        '@context': 'https://schema.org',
        '@graph': [
            { '@type': 'WebSite', name: NAME, url: SITE },
            { ...publisher },
        ],
    });
}

export function breadcrumbLd(crumbs) {
    // crumbs: [{ name, path }] in order, last one may omit path
    return clean({
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        itemListElement: crumbs.map((c, i) => ({
            '@type': 'ListItem',
            position: i + 1,
            name: c.name,
            item: c.path ? abs(c.path) : undefined,
        })),
    });
}

export function blogPostingLd(post, path) {
    return clean({
        '@context': 'https://schema.org',
        '@type': 'BlogPosting',
        headline: post.title.slice(0, 110),
        description: post.meta?.search_description || post.excerpt,
        image: post.hero_image ? [abs(post.hero_image)] : undefined,
        datePublished: post.first_published_at,
        dateModified: post.last_published_at,
        author: publisher,
        publisher,
        mainEntityOfPage: abs(path),
        keywords: post.tags?.map(t => t.name).join(', ') || undefined,
        articleSection: post.categories?.[0]?.name,
    });
}

export function recipeLd(r, path) {
    const hasCore = r.ingredients?.length > 0 && r.instructions?.length > 0;
    if (!hasCore) return null; // incomplete recipes produce invalid schema

    const cal = r.nutrition?.find(n => n.name === 'Calories')?.per_serving;

    return clean({
        '@context': 'https://schema.org',
        '@type': 'Recipe',
        name: r.title,
        description: r.meta?.search_description,
        image: r.image?.url ? [abs(r.image.url)] : undefined,
        datePublished: r.first_published_at,
        author: publisher,
        prepTime: iso(r.prep_time),
        cookTime: iso(r.cook_time),
        totalTime: iso(r.total_time),
        recipeYield: r.servings ? `${r.servings} servings` : undefined,
        recipeCategory: r.category?.[0]?.name,
        recipeIngredient: r.ingredients.map(i => `${i.display?.['1'] ?? ''} ${i.name}`.trim()),
        recipeInstructions: r.instructions.map(s => ({ '@type': 'HowToStep', text: s.text })),
        nutrition: cal != null
            ? { '@type': 'NutritionInformation', calories: `${cal} calories` }
            : undefined,
        mainEntityOfPage: abs(path),
    });
}