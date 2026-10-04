import os
import re
import unicodedata

# Master Density Database (grams per 1 mL of the ingredient)
# Expanded Master Density Database (grams per 1 mL of the ingredient)
# Derived from USDA FDC, King Arthur Baking, and standard packaging conversions
INGREDIENT_DENSITIES = {
    # --- Flours, Grains, Baking & Mixes ---
    "white whole wheat flour": 0.507,      # ~120g per cup
    "box cake mix": 0.570,                # ~135g per cup
    "potato flour": 0.676,                # ~160g per cup
    "chick pea flour": 0.389,             # Garbanzo flour: ~92g per cup
    "corn flour": 0.507,                  # ~120g per cup
    "nutritional yeast": 0.211,           # Light flakes: ~50g per cup
    "phyllo dough": 0.350,                # Variable (usually measured in sheets/g)
    "potato bread": 0.250,                # Volumetric fallback for cubes/crumbs

    # --- Liquids, Vinegars, Brews & Syrups ---
    "liquid smoke": 1.010,                # Slightly denser than water
    "lemon juice": 1.030,                 # ~244g per cup
    "balsamic vinegar": 1.010,            # ~240g per cup
    "molasses": 1.437,                    # Dense syrup: ~340g per cup
    "blackstrap molasses": 1.450,         # Extra thick: ~343g per cup
    "soy sauce": 1.150,                   # Salty/dense: ~272g per cup
    "barbecue sauce": 1.180,              # Thick sauce: ~280g per cup
    "lager beer": 1.005,                  # ~238g per cup
    "stout beer": 1.012,                  # Slightly heavier residue
    "pilsner beer": 1.005,
    "cashew cheese sauce": 1.040,         # Creamy blend: ~246g per cup
    "bechamel sauce": 1.050,              # White roux sauce: ~248g per cup

    # --- Cereals, Oats & Pasta (Dry) ---
    "pearl barley": 0.845,                # ~200g per cup
    "quick grits": 0.676,                 # Corn grits: ~160g per cup
    "cream of wheat": 0.718,              # Farina cereal: ~170g per cup
    "old fashion rolled oats": 0.418,     # ~99g per cup
    "steel cut irish oats": 0.718,        # Denser than rolled: ~170g per cup
    "linguine noodles": 0.400,            # Dry packed shape volumetric fallback
    "penne noodles": 0.380,               # Loose hollow shape volumetric fallback
    "spaghetti noodles": 0.420,
    "macaroni noodles": 0.400,

    # --- Legumes, Beans & Dal (Dry vs. Cooked) ---
    "black eyed peas": 0.761,             # Dry: ~180g per cup
    "dry pinto beans": 0.795,             # Dry: ~188g per cup
    "cooked pinto beans": 0.740,          # Wet, packed: ~175g per cup
    "dry navy beans": 0.803,              # Dry: ~190g per cup
    "cooked navy beans": 0.740,           # Wet, packed: ~175g per cup
    "dry black beans": 0.782,             # Dry: ~185g per cup
    "cooked black beans": 0.740,          # Wet, packed: ~175g per cup
    "dried red beans": 0.782,             # Dry: ~185g per cup
    "cooked red beans": 0.740,            # Wet, packed: ~175g per cup
    "dried great northern beans": 0.761,  # Dry: ~180g per cup
    "cooked great northern beans": 0.740, # Wet, packed: ~175g per cup
    "dried cannellini beans": 0.761,      # Dry: ~180g per cup
    "cooked cannellini beans": 0.740,     # Wet, packed: ~175g per cup
    "mung dal": 0.845,                    # Split/skinned mung: ~200g per cup
    "split yellow lentils dal": 0.845,    # ~200g per cup
    "brown lentils": 0.811,               # Dry whole: ~192g per cup
    "spilt red lentils": 0.803,           # Dry split: ~190g per cup
    "green split peas": 0.809,            # Dry split: ~191g per cup

    # --- Nuts, Roots & Alliums ---
    "walnuts": 0.423,                     # Chopped: ~100g per cup
    "almonds": 0.592,                     # Whole/chopped average: ~140g per cup
    "cashews": 0.550,                     # Whole/halves average: ~130g per cup
    "fresh garlic": 0.570,                # Minced/crushed: ~135g per cup
    "fresh shallots": 0.550,              # Chopped: ~130g per cup
    "fresh turmeric root": 0.600,         # Minced root
    "ground turmeric": 0.444,             # Dried powder: ~105g per cup

    # --- Fresh, Canned & Frozen Vegetables ---
    "fresh carrots": 0.530,               # Chopped/diced: ~125g per cup
    "canned carrots": 0.617,              # Sliced in liquid: ~146g per cup
    "red yams": 0.634,                    # Cubed raw: ~150g per cup
    "sweet potatoes": 0.634,              # Cubed raw: ~150g per cup
    "sweet potato leaves": 0.080,         # Very light leafy green packed loose
    "russet potato": 0.634,               # Diced raw
    "red potato": 0.655,                  # Slightly denser wax potato
    "golden potato": 0.655,
    "green cabbage": 0.317,               # Shredded loose: ~75g per cup
    "red cabbage": 0.317,                 # Shredded loose: ~75g per cup
    "bok choy": 0.296,                    # Shredded/chopped: ~70g per cup
    "napa cabbage": 0.296,                # Shredded/chopped: ~70g per cup
    "fresh spinach": 0.127,               # Raw packed loose: ~30g per cup
    "baby spinach": 0.127,                # Raw packed loose: ~30g per cup
    "canned spinach": 0.824,              # Wet, heavily compressed: ~195g per cup
    "frozen spinach": 0.655,              # Thawed/chopped compressed: ~155g per cup
    "canned corn": 0.700,                 # Drained kernels: ~165g per cup
    "frozen corn": 0.655,                 # Whole kernels: ~155g per cup
    "frozen peas": 0.613,                 # Whole peas: ~145g per cup
    "frozen mixed veggies": 0.634,        # Standard mix: ~150g per cup
    "broccoli": 0.300,                    # Cut florets loose: ~71g per cup
    "frozen broccoli": 0.380,             # Slightly more compact ice/florets
    "red bell pepper": 0.380,             # Chopped: ~90g per cup
    "yellow bell pepper": 0.380,          # Chopped: ~90g per cup
    "green bell pepper": 0.380,           # Chopped: ~90g per cup
    "crushed tomatoes": 1.020,            # Dense puree: ~241g per cup
    "stewed tomatoes": 0.930,             # Pieces with juice: ~220g per cup
    "diced tomatoes": 0.950,              # Pieces with juice: ~225g per cup
    "marinara sauce": 1.030,              # Cooked tomato sauce: ~244g per cup

    # --- Berries & Fruits (Fresh & Frozen) ---
    "fresh blueberries": 0.625,           # Whole: ~148g per cup
    "frozen blueberries": 0.655,          # Slightly heavier with ice frost: ~155g per cup
    "frozen wild blueberries": 0.592,     # Smaller berries pack tighter but less water ice
    "fresh strawberries": 0.608,          # Sliced: ~144g per cup
    "frozen strawberries": 0.634,          # Sliced frozen: ~150g per cup

    # --- Teas, Herbs & Powders ---
    "kashaya powder": 0.450,              # Herbal spiced powder base estimate
    "indian chai": 0.450,                 # Loose leaf tea blend base estimate
    "black tea": 0.360,                   # Loose leaves: ~85g per cup
    "green tea": 0.360,                   # Loose leaves: ~85g per cup
    "dried hibiscus leaves": 0.170,       # Whole dried petals (very light)
    "herbal fruit tea": 0.400,            # Chunky dried fruit tea blend pieces
    "fresh rosemary": 0.180,              # Stripped leaves loose
    "dried rosemary": 0.110,              # Dried needles: ~26g per cup
    "fresh marjoram": 0.120,              # Fresh loose leaves
    "dried marjoram": 0.084,              # Rubbed herb: ~20g per cup
    "fresh oregano": 0.120,               # Fresh loose leaves
    "dried oregano": 0.105,               # Rubbed herb: ~25g per cup
    "fresh basil": 0.105,                 # Chopped fresh leaves: ~25g per cup
    "fresh sage leaves": 0.080,           # Whole leaves loose
    "dried sage": 0.084,                  # Rubbed herb: ~20g per cup
    "dried dill": 0.118,                  # Weed: ~28g per cup

    # --- Tofu & Analogs ---
    "firm tofu": 0.960,                   # Packed blocks (usually mass, but 1g/mL equivalent)
    "super firm high protein tofu": 1.020, # Compressed, lower water content

    # --- Spices ---
    "smoked paprika": 0.6,
}


# Separate density reference for cooked/wet items
COOKED_LEGUME_DENSITY = 0.74  # Average for cooked/canned beans/lentils (~175g per cup)

# Standard US volume to Milliliters (mL) conversion map
VOLUME_TO_ML = {
    "cup": 236.588,
    "cups": 236.588,
    "tbsp": 14.787,
    "tablespoon": 14.787,
    "tablespoons": 14.787,
    "tsp": 4.929,
    "teaspoon": 4.929,
    "teaspoons": 4.929
}

FRACTION_TO_UNIT = {
    "1/2": "half",
    "1/4": "quarter",
    "1/8": "eigth",
    "1/3": "third",
    "2/3": "two third",
}

def normalize_string(text):
    """Cleans up punctuation, parentheses, and extra spaces for more reliable matching."""
    text = text.lower()
    text = re.sub(r'\(.*?\)', '', text)  # Remove anything inside parenthetical notes like "(sifted)"
    text = re.sub(r'[^a-z0-9\s]', '', text)  # Remove punctuation like dashes or commas
    return " ".join(text.split())  # Clean up trailing or double spaces

def find_density(ingredient_name):
    """Finds density by checking normalized names and accounting for cooked vs dry states."""
    clean_name = normalize_string(ingredient_name)
    
    # 1. State check: Is this a cooked/canned legume?
    is_cooked = "cooked" in clean_name or "canned" in clean_name
    
    # 2. Check for common legumes in the name
    legumes = ["lentil", "bean", "chickpea", "split pea", "garbanzo"]
    has_legume = any(legume in clean_name for legume in legumes)
    
    # 3. Handle the cooked state switch dynamically
    if is_cooked and has_legume:
        return COOKED_LEGUME_DENSITY

    # 4. Standard Direct match check (defaults to your dry dictionary values)
    if clean_name in INGREDIENT_DENSITIES:
        return INGREDIENT_DENSITIES[clean_name]
        
    # 5. Keyword fallback check
    for key, density in INGREDIENT_DENSITIES.items():
        if key in clean_name:
            return density
            
    return None

def get_fallback_density(ing_clean):
    """Provides a realistic density approximation based on ingredient keywords."""
    # 1. Liquids (Water-based: milk, juice, vinegar, water, sauce)
    if any(k in ing_clean for k in ['water', 'milk', 'juice', 'vinegar', 'sauce', 'broth', 'wine', 'honey', 'syrup']):
        return 1.0  # ~1.0 g/mL
        
    # 2. Fats & Oils (Olive oil, butter, coconut oil)
    if any(k in ing_clean for k in ['oil', 'butter', 'margarine', 'shortening']):
        return 0.9  # ~0.9 g/mL
        
    # 3. Flours, Powders, & Starches (Flour, cocoa, baking soda, cornstarch)
    if any(k in ing_clean for k in ['flour', 'powder', 'soda', 'starch', 'sugar', 'salt', 'spice', 'cinnamon', 'cumin']):
        return 0.6  # ~0.5 - 0.6 g/mL
        
    # 4. Global fallback for anything completely unknown
    return 0.75  # Safe middle-ground for mixed recipe items

def parse_fraction(fraction_str):
    """Converts string fractions like '1 1/2' or '3/4' into floats."""
    if not fraction_str:
        return 0.0
    parts = fraction_str.strip().split()
    total = 0.0
    for part in parts:
        if '/' in part:
            num, denom = part.split('/')
            total += float(num) / float(denom)
        else:
            total += float(part)
    return total

def convert_raw_line(line):
    """Parses a messy string line, extracts components, and converts units if possible."""
    # 1. Clean the line of invisible control characters, standard whitespace, and uniform slashes
    clean_line = line.strip().lstrip('\ufeff\u200b')  # Strip BOM and zero-width spaces
    clean_line = clean_line.replace('∕', '/')        # Replace curly mathematical slashes with standard slashes

    # 2. Use a slightly modified pattern that explicitly allows any unicode space (\s)
    pattern = r'^([\d\s\./]+)\s*(cups?|tbsps?|tablespoons?|tsps?|teaspoons?|cans?|sprigs?|slices?|cloves?|pieces?|stalks?|bunches|bunch)?\s+(.+)$'

    match = re.match(pattern, clean_line, re.IGNORECASE)

    if match:
        raw_amount, unit, ing_name = match.groups()
        clean_raw_amount = raw_amount.strip()
        amount = parse_fraction(clean_raw_amount)
        
        # Handle case where unit is None
        unit_lower = unit.lower() if unit else None
        ing_clean = ing_name.lower().strip()
        
        line_dict = {"ingredient": ing_clean, "amount": amount}
        
        # Look for the closest match in our density database
        density = None
        for key in INGREDIENT_DENSITIES:
            if key in ing_clean:
                density = INGREDIENT_DENSITIES[key]
                break
                
        if density is None:
            density = get_fallback_density(ing_clean)
            
        line_dict = {"ingredient": ing_clean}
        
        # Calculate weight using either exact or fallback density
        if unit_lower in VOLUME_TO_ML:
            volume_ml = amount * VOLUME_TO_ML[unit_lower]
            weight_grams = round(volume_ml * density)
            line_dict["unit"] = 'g'
            line_dict["amount"] = weight_grams
            line_dict["ingredient"] = ing_clean
            return line_dict
        else:
            line_dict["unit"] = "whole" if amount >= 1 else FRACTION_TO_UNIT.get(clean_raw_amount)
            line_dict["amount"] = clean_raw_amount
            line_dict["ingredient"] = ing_clean
            return line_dict
    
    key_value_match = re.search(r'^\s*(.+?)\s*:\s*(.+?)\s*$', line.strip())

    if(key_value_match):
        key, value = key_value_match.groups()
        line_dict = {}
        line_dict[key] = value
        return line_dict

    # Return original line if it doesn't match standard volume patterns (e.g., "salt to taste")
    return line.strip()

