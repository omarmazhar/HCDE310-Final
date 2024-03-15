import requests
import json

def get_nutrition_data(food_item):
    """
    Fetches nutrition data for a given food item using the Edamam API.
    """
    api_url = "https://api.edamam.com/api/nutrition-data?app_id=6a2f5f46&app_key=f647292ef28b5d08914370df89454e82"
    params = {"ingr": food_item}
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for: {food_item}")
        return None

def calculate_intake_percentages(user_weight, nutrition_data):
    calories_needed = user_weight * 15
    protein_needed = user_weight * 0.75
    carbs_needed = (user_weight / 2.2) * 7
    total_calories = total_protein = total_carbs = 0

    for item in nutrition_data.values():
        total_calories += item['totalNutrients'].get('ENERC_KCAL', {}).get('quantity', 0)
        total_protein += item['totalNutrients'].get('PROCNT', {}).get('quantity', 0)
        total_carbs += item['totalNutrients'].get('CHOCDF', {}).get('quantity', 0)

    calories_percent = (total_calories / calories_needed) * 100
    protein_percent = (total_protein / protein_needed) * 100
    carbs_percent = (total_carbs / carbs_needed) * 100

    return calories_percent, protein_percent, carbs_percent

def main():
    all_nutrition_data = {}
    while True:
        food_item = input("Enter a food item (or type 'quit' to exit): ").strip()
        if food_item.lower() == 'quit':
            break
        nutrition_data = get_nutrition_data(food_item)
        if nutrition_data:
            all_nutrition_data[food_item] = nutrition_data

    with open('nutrition_data.json', 'w') as json_file:
        json.dump(all_nutrition_data, json_file, indent=4)
    print("Nutrition data exported to nutrition_data.json")

    user_weight = float(input("Please enter your weight in pounds: "))
    try:
        with open('nutrition_data.json', 'r') as file:
            nutrition_data = json.load(file)
    except FileNotFoundError:
        print("Nutrition data file not found. Please make sure 'nutrition_data.json' exists.")
        return

    calories_percent, protein_percent, carbs_percent = calculate_intake_percentages(user_weight, nutrition_data)
    print("\nBased on your weight and the food you've eaten:")
    print(f"Calories intake is {calories_percent:.2f}% of your daily needs.")
    print(f"Protein intake is {protein_percent:.2f}% of your daily needs.")
    print(f"Carbs intake is {carbs_percent:.2f}% of your daily needs.")

if __name__ == "__main__":
    main()
