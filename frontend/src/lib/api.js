import { getDevData } from '../utils/api';

const isDev = import.meta.env.DEV;
const API_BASE = import.meta.env.WAGTAIL_API_BASE;
const MAP = {
    home:         { data: `${API_BASE}/api/homepage/` },
    recipes:      { data: `${API_BASE}/api/recipes/` },
    recipeDetail: { data: `${API_BASE}/api/recipes/` },
    blogIndex:    { data: `${API_BASE}/api/blog/` },
    blogPost:     { data: `${API_BASE}/api/blog/` },
    measurements: { data: `${API_BASE}/api/measurements/` },
}

export async function getPageData(type, slug = null) {
    if (isDev) {
        const data = await getDevData(type);
        return data.default;
    }

    const entry = MAP[type];
    if (!entry) throw new Error(`Unknown page type: ${type}`);

    const dataUrl = slug ? `${entry.data}${slug}/` : entry.data;
    const dataRes = await fetch(dataUrl);

    if (!dataRes.ok) throw new Error(`API error ${dataRes.status}`);

    return dataRes.json();
}