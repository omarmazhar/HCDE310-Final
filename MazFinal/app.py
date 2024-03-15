from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

EDAMAM_API_URL = "https://api.edamam.com/api/nutrition-data?app_id=6a2f5f46&app_key=f647292ef28b5d08914370df89454e82"

def get_nutrition_data(food_item):
    """
    Fetches nutrition data for a given food item using the Edamam API.
    """
    params = {"ingr": food_item}
    response = requests.get(EDAMAM_API_URL, params=params)
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

    return {
        "calories_percent": (total_calories / calories_needed) * 100,
        "protein_percent": (total_protein / protein_needed) * 100,
        "carbs_percent": (total_carbs / carbs_needed) * 100
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_weight = float(request.form['weight'])
        food_items = request.form['foods'].split(',')

        all_nutrition_data = {}
        for food_item in food_items:
            nutrition_data = get_nutrition_data(food_item.strip())
            if nutrition_data:
                all_nutrition_data[food_item] = nutrition_data

        with open('nutrition_data.json', 'w') as json_file:
            json.dump(all_nutrition_data, json_file, indent=4)
        
        try:
            with open('nutrition_data.json', 'r') as file:
                nutrition_data = json.load(file)
        except FileNotFoundError:
            return "Nutrition data file not found. Please make sure 'nutrition_data.json' exists."

        results = calculate_intake_percentages(user_weight, nutrition_data)
        return render_template('results.html', results=results)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
