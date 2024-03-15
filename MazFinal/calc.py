import json

def calculate_intake_percentages(user_weight, nutrition_data):
    # Calculate daily needs
    calories_needed = user_weight * 15
    protein_needed = user_weight * 0.75
    carbs_needed = (user_weight / 2.2) * 7
    
     

    # Initialize total intake from food
    total_calories = total_protein = total_carbs  = 0

    # Sum up nutrients from each food item
    for item in nutrition_data.values():
        total_calories += item['totalNutrients'].get('ENERC_KCAL', {}).get('quantity', 0)
        total_protein += item['totalNutrients'].get('PROCNT', {}).get('quantity', 0)
        total_carbs += item['totalNutrients'].get('CHOCDF', {}).get('quantity', 0)
        

    # Calculate percentages
    calories_percent = (total_calories / calories_needed) * 100
    protein_percent = (total_protein / protein_needed) * 100
    carbs_percent = (total_carbs / carbs_needed) * 100
    

    return calories_percent, protein_percent, carbs_percent

def main():
    # Ask user for their weight
    user_weight = float(input("Please enter your weight in pounds: "))
    
    # Load nutrition data from JSON file
    try:
        with open('nutrition_data.json', 'r') as file:
            nutrition_data = json.load(file)
    except FileNotFoundError:
        print("Nutrition data file not found. Please make sure 'nutrition_data.json' exists.")
        return
    
    # Calculate intake percentages
    calories_percent, protein_percent, carbs_percent= calculate_intake_percentages(user_weight, nutrition_data)
    
    # Print out the results in a nice manner
    print("\nBased on your weight and the food you've eaten:")
    print(f"Calories intake is {calories_percent:.2f}% of your daily needs.")
    print(f"Protein intake is {protein_percent:.2f}% of your daily needs.")
    print(f"Carbs intake is {carbs_percent:.2f}% of your daily needs.")
    

if __name__ == "__main__":
    main()
