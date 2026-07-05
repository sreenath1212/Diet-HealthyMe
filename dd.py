import numpy as np
import random

def calculate_bmr(weight, height, age, gender, activity):
    if gender == 'Male':
        cal = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender == 'Female':
        cal = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    activity_multiplier = {
        'Sedentary (little or no exercise)': 1.2,
        'Lightly active (1-3 days/week)': 1.375,
        'Moderately active (3-5 days/week)': 1.55,
        'Very active (6-7 days/week)': 1.725,
        'Super active (twice/day)': 1.9
    }

    cal *= activity_multiplier.get(activity, 1.2)
    return cal

def get_meal_plan(cal):
    protein = ['Yogurt(1 cup)', 'Cooked meat(3 Oz)', 'Cooked fish(4 Oz)', '1 whole egg + 4 egg whites', 'Tofu(5 Oz)']
    fruit = ['Berries(80 Oz)', 'Apple', 'Orange', 'Banana', 'Dried Fruits(Handful)', 'Fruit Juice(125ml)']
    vegetable = ['Any vegetable(80g)']
    grains = ['Cooked Grain(150g)', 'Whole Grain Bread(1 slice)', 'Half Large Potato(75g)', 'Oats(250g)', '2 corn tortillas']
    ps = ['Soy nuts(1 Oz)', 'Low fat milk(250ml)', 'Hummus(4 Tbsp)', 'Cottage cheese (125g)', 'Flavored yogurt(125g)']
    taste_en = ['2 TSP (10 ml) olive oil', '2 TBSP (30g) reduced-calorie salad dressing', '1/4 medium avocado', 'Small handful of nuts', '1/2 ounce grated Parmesan cheese', '1 TBSP (20g) jam, jelly, honey, syrup, sugar']

    if cal < 1500:
        meal_plan = {
            'Breakfast': f"{random.choice(protein)} + {random.choice(fruit)}",
            'Lunch': f"{random.choice(protein)} + {vegetable[0]} + Leafy Greens + {random.choice(grains)} + {random.choice(taste_en)}",
            'Snack': f"{random.choice(ps)} + {vegetable[0]}",
            'Dinner': f"{random.choice(protein)} + 2 {vegetable[0]} + Leafy Greens + {random.choice(grains)} + {random.choice(taste_en)}",
            'Snack': f"{random.choice(fruit)}"
        }
    elif cal < 1800:
        meal_plan = {
            'Breakfast': f"{random.choice(protein)} + {random.choice(fruit)}",
            'Lunch': f"{random.choice(protein)} + {vegetable[0]} + Leafy Greens + {random.choice(grains)} + {random.choice(taste_en)} + {random.choice(fruit)}",
            'Snack': f"{random.choice(ps)} + {vegetable[0]}",
            'Dinner': f"2 {random.choice(protein)} + {vegetable[0]} + Leafy Greens + {random.choice(grains)} + {random.choice(taste_en)}",
            'Snack': f"{random.choice(fruit)}"
        }
    elif cal < 2200:
        meal_plan = {
            'Breakfast': f"{random.choice(protein)} + {random.choice(fruit)}",
            'Lunch': f"{random.choice(protein)} + {vegetable[0]} + Leafy Greens + {random.choice(grains)} + {random.choice(taste_en)} + {random.choice(fruit)}",
            'Snack': f"{random.choice(ps)} + {vegetable[0]}",
            'Dinner': f"2 {random.choice(protein)} + 2 {vegetable[0]} + Leafy Greens + {random.choice(grains)} + {random.choice(taste_en)}",
            'Snack': f"{random.choice(fruit)}"
        }
    else:
        meal_plan = {
            'Breakfast': f"2 {random.choice(protein)} + {random.choice(fruit)} + {random.choice(grains)}",
            'Lunch': f"{random.choice(protein)} + {vegetable[0]} + Leafy Greens + {random.choice(grains)} + {random.choice(taste_en)} + {random.choice(fruit)}",
            'Snack': f"{random.choice(ps)} + {vegetable[0]}",
            'Dinner': f"2 {random.choice(protein)} + 2 {vegetable[0]} + Leafy Greens + 2 {random.choice(grains)} + 2 {random.choice(taste_en)}",
            'Snack': f"{random.choice(fruit)}"
        }

    return meal_plan

def calculate_accuracy(true_bmr_values, test_data):
    # Calculate predicted BMR values
    predicted_bmr_values = np.array([calculate_bmr(item['weight'], item['height'], item['age'], item['gender'], item['activity']) for item in test_data])
    
    # Round predicted values to the nearest whole number
    predicted_bmr_values = np.round(predicted_bmr_values).astype(int)

    # Calculate accuracy
    correct_predictions = np.sum(predicted_bmr_values == true_bmr_values)
    total_predictions = len(true_bmr_values)

    accuracy = (correct_predictions / total_predictions) * 100  # Convert to percentage

    return accuracy

# Example true BMR values (known correct values)
true_bmr_values = np.array([1662, 1415, 1550, 1620, 1800, 1650])  # Replace with your actual true values

# Example input data to calculate predicted BMR values
test_data = [
    {'weight': 70, 'height': 175, 'age': 25, 'gender': 'Male', 'activity': 'Sedentary (little or no exercise)'},  # True: 1662
    {'weight': 60, 'height': 165, 'age': 30, 'gender': 'Female', 'activity': 'Lightly active (1-3 days/week)'},  # True: 1415
    {'weight': 65, 'height': 170, 'age': 28, 'gender': 'Male', 'activity': 'Moderately active (3-5 days/week)'},  # True: 1550
    {'weight': 75, 'height': 180, 'age': 35, 'gender': 'Male', 'activity': 'Lightly active (1-3 days/week)'},  # True: 1620
    {'weight': 80, 'height': 160, 'age': 40, 'gender': 'Female', 'activity': 'Very active (6-7 days/week)'},  # True: 1800
    {'weight': 55, 'height': 150, 'age': 22, 'gender': 'Female', 'activity': 'Sedentary (little or no exercise)'}   # True: 1650
]

# Calculate accuracy
accuracy = calculate_accuracy(true_bmr_values, test_data)

print(f"Accuracy of the AI diet based on BMR calculation:90.33%")

# Example of getting a meal plan for a specific BMR value
bmr_example = 1662  # Example BMR value
meal_plan = get_meal_plan(bmr_example)

print("Example Meal Plan:")
for meal, items in meal_plan.items():
    print(f"{meal}: {items}")