import requests
import json

def get_nutrition_data(food_item):
    """
    Fetches nutrition data for a given food item using the Edamam API.
    """
    # Here, the API URL already includes the app_id and app_key
    api_url = "https://api.edamam.com/api/nutrition-data?app_id=6a2f5f46&app_key=f647292ef28b5d08914370df89454e82"
    # Specify the food item in the query parameters
    params = {
        "ingr": food_item
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        return response.json()  # Returns the JSON response if the request was successful
    else:
        print(f"Failed to fetch data for: {food_item}")
        return None

def main():
    all_nutrition_data = {}

    while True:
        food_item = input("Enter a food item (or type 'quit' to exit): ").strip()
        if food_item.lower() == 'quit':
            break
        nutrition_data = get_nutrition_data(food_item)
        if nutrition_data:
            all_nutrition_data[food_item] = nutrition_data

    # Save the collected nutrition data into a JSON file
    with open('nutrition_data.json', 'w') as json_file:
        json.dump(all_nutrition_data, json_file, indent=4)
        print("Nutrition data exported to nutrition_data.json")

if __name__ == "__main__":
    main()
