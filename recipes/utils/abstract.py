ABSTRACT_UNIT_TO_GRAMS = {
    # Garlic
    ('clove', 'Fresh Garlic'):        4.0,
    ('clove', 'Garlic'):              4.0,

    # Onion
    ('whole', 'Onion'):               150.0,
    ('half',  'Onion'):               75.0,
    ('slice', 'Onion'):               15.0,

    # Cabbage
    ('head',  'Red Cabbage'):         900.0,
    ('head',  'Green Cabbage'):       900.0,
    ('head',  'Napa Cabbage'):        700.0,
    ('half',  'Red Cabbage'):         450.0,
    ('half',  'Green Cabbage'):       450.0,
    ('half',  'Napa Cabbage'):        350.0,


    # Celery
    ('stalk', 'Potatoes'):            40.0,

    # Lemon / Lime
    ('whole', 'Lemon'):               58.0,
    ('slice', 'Lemon'):               6.0,
    ('whole', 'Lime'):                44.0,

    # Bell peppers
    ('whole', 'Red Bell Pepper'):     119.0,
    ('whole', 'Yellow Bell Pepper'):  119.0,
    ('whole', 'Green Bell Pepper'):   119.0,
    ('slice', 'Red Bell Pepper'):     15.0,
    ('slice', 'Yellowll Pepper'):     15.0,
    ('slice', 'Green Bell Pepper'):     15.0,

    # Tomatoes
    ('whole', 'Stewed Tomatoes'):     123.0,
    ('slice', 'Stewed Tomatoes'):     20.0,

    # Ginger
    ('slice', 'Fresh Ginger'):        3.0,

    # Herbs
    ('sprig', 'Fresh Rosemary'):      2.0,
    ('sprig', 'Fresh Marjoram'):      2.0,
    ('sprig', 'Fresh Basil'):         2.0,
    ('leaf',  'Sage Leaves'):         1.5,
    ('stalk', 'Fresh Rosemary'):      5.0,

    # Potatoes
    ('whole', 'Potatoes'):            150.0,
    ('whole', 'Red Potatoes'):        150.0,
    ('whole', 'Golden Potatoes'):     150.0,
    ('whole', 'Russet Potatoes'):     213.0,

    # Coconut Milk/Cream
    ('can', 'Coconut Milk'):          90.0,
    ('can', 'Coconut Cream'):         90.0,

    # Tomatoes
    ('can', 'Diced Tomatoes'):        90.0,
    ('can', 'Stewed Tomatoes'):       90.0,
    ('can', 'Crushed Tomatoes'):      90.0,
    
    # Corn
    ('can', 'Canned Corn'):           90.0,

    # Carrots,
    ('can', 'Canned Carrots'):        90.0,
    ('whole', 'Carrots'):             90.0,
    ('half', 'Fresh Carrots'):        90.0,

    # Other
    ('whole', 'Avocado'):             150.0,
    ('half',  'Avocado'):             75.0,
}

def abstract_to_grams(unit, ingredient_name, quantity=1.0):
    """
    Convert abstract unit to grams for nutrition calculation.
    Returns None if no conversion exists.
    """
    key = (unit.lower(), ingredient_name)
    grams_per_unit = ABSTRACT_UNIT_TO_GRAMS.get(key)

    if grams_per_unit is None:
        return None

    return grams_per_unit * quantity