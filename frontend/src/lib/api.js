import { appendMetaData, getDevData } from '../utils/api';
const isDev = import.meta.env.DEV;
const API_BASE = import.meta.env.WAGTAIL_API_BASE;

const MAP = {
    home: {
        meta: `${API_BASE}/pages/?type=home.HomePage&fields=*`,
        data: `${API_BASE}/api/homepage/`,
    },
    recipes: {
        meta: `${API_BASE}/pages/?type=recipes.RecipeIndexPage&fields=*`,
        data: `${API_BASE}/api/recipes/`,
    },
    recipeDetail: {
        meta: `${API_BASE}/pages/?type=recipes.RecipePage&fields=*`,
        data: `${API_BASE}/api/recipes/`,  // ← needs slug appended at call time
    },
    blogIndex: {
        meta: `${API_BASE}/pages/?type=blog.BlogIndexPage&fields=*`,
        data: `${API_BASE}/api/blog/`,
    },
    blogPost: {
        meta: `${API_BASE}/pages/?type=blog.BlogPost&fields=*`,
        data: `${API_BASE}/api/blog/`,  // ← needs slug appended at call time
    },
    measurements: {
        data: `${API_BASE}/api/measurements/`,
    }
}

export async function getPageData(type, slug = null) {
    if (isDev) {
        const data = await getDevData(type);
        return data.default;
    }

    const entry = MAP[type];
    if (!entry) throw new Error(`Unknown page type: ${type}`);

    // Build data URL
    const dataUrl = slug ? `${entry.data}${slug}/` : entry.data;
    const dataRes = await fetch(dataUrl);

    if (!dataRes.ok) {
        throw new Error(`API error ${dataRes.status} for ${dataUrl}`);
    }

    const dataJson = await dataRes.json();

    // Fetch and append Wagtail page meta if available
    if (entry.meta) {
        try {
            const metaRes = await fetch(entry.meta);
            if (metaRes.ok) {
                const metaJson = await metaRes.json();
                const page = metaJson?.items?.[0];
                if (page) {
                    return appendMetaData({
                        data: dataJson,
                        meta: page.meta,
                        title: page.title
                    });
                }
            }
        } catch (e) {
            // Meta fetch failed — return data without meta
            console.warn(`Meta fetch failed for ${type}:`, e.message);
        }
    }

    return dataJson;
}