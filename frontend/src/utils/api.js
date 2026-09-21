export async function getDevData(type) {
    const devMap = {
        home:         () => import('../data/homepage.json'),
        recipes:      () => import('../data/recipes.json'),
        recipeDetail: () => import('../data/recipe.json'),
        blogIndex:    () => import('../data/blog.json'),
        blogPost:     () => import('../data/blog-post.json'),
        measurements: () => import('../data/measurements.json'),
    }

    const loader = devMap[type];
    if (!loader) throw new Error(`No dev data for type: ${type}`);
    return loader();
}