BASE_URL = "https://api.nal.usda.gov/fdc"

def fetch_ingredient_nutrients(api_key, fdcId, ingredient_name, target_nutrients):
    endpoint = f"{BASE_URL}/v1/food/{fdcId}"
    params = {"api_key": api_key}

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()

        print(f"Processing: {data}")
        if not data:
            print(f"❌ No matches found for: {ingredient_name}")
            return None

        extracted_nutrients = {
            "ingredient": ingredient_name,
            "fdcId": data.get("fdcId"),
            "description": data.get("description"),
            "nutrients": {},
        }

        # Filter out only your allowed list of nutrients
        for nutrient in data.get("foodNutrients", []):
            # USDA returns nutrientId as an int or string depending on schema version
            n_id = str(nutrient.get("nutrientNumber"))
            if n_id in target_nutrients:
                label = target_nutrients[n_id]
                extracted_nutrients["nutrients"][label] = nutrient.get("value")

        return extracted_nutrients

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error fetching {ingredient_name}: {e}")
        return None