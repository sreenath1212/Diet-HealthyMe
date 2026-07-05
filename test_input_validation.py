import os
import sys
import django
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HealthyMe.settings')
django.setup()

from django.test import RequestFactory
from MyApp.views import plan_meal, calculate_tdee

# Create a mock request
factory = RequestFactory()

def test_tdee_calculation():
    """Test TDEE calculation with known values"""
    print("=== Testing TDEE Calculation ===")
    
    # Test case 1: Male, 30 years, 70kg, 170cm, moderately active
    tdee1 = calculate_tdee(170, 70, 30, 'male', 'moderately_active')
    expected_bmr1 = (10 * 70) + (6.25 * 170) - (5 * 30) + 5  # 700 + 1062.5 - 150 + 5 = 1617.5
    expected_tdee1 = expected_bmr1 * 1.55  # 1617.5 * 1.55 = 2507.125
    print(f"Male, 30y, 70kg, 170cm, moderately active:")
    print(f"  Expected BMR: {expected_bmr1:.1f}")
    print(f"  Expected TDEE: {expected_tdee1:.1f}")
    print(f"  Calculated TDEE: {tdee1:.1f}")
    print(f"  Difference: {abs(tdee1 - expected_tdee1):.1f}")
    print(f"  ✅ Correct" if abs(tdee1 - expected_tdee1) < 1 else f"  ❌ Incorrect")
    
    # Test case 2: Female, 25 years, 60kg, 165cm, sedentary
    tdee2 = calculate_tdee(165, 60, 25, 'female', 'sedentary')
    expected_bmr2 = (10 * 60) + (6.25 * 165) - (5 * 25) - 161  # 600 + 1031.25 - 125 - 161 = 1345.25
    expected_tdee2 = expected_bmr2 * 1.2  # 1345.25 * 1.2 = 1614.3
    print(f"\nFemale, 25y, 60kg, 165cm, sedentary:")
    print(f"  Expected BMR: {expected_bmr2:.1f}")
    print(f"  Expected TDEE: {expected_tdee2:.1f}")
    print(f"  Calculated TDEE: {tdee2:.1f}")
    print(f"  Difference: {abs(tdee2 - expected_tdee2):.1f}")
    print(f"  ✅ Correct" if abs(tdee2 - expected_tdee2) < 1 else f"  ❌ Incorrect")

def test_meal_planner_with_different_inputs():
    """Test meal planner with various user inputs"""
    print("\n=== Testing Meal Planner with Different Inputs ===")
    
    test_cases = [
        {
            'name': 'High Activity Male',
            'data': {
                'height': '180',
                'weight': '80',
                'age': '25',
                'gender': 'male',
                'activity_level': 'very_active',
                'medical_conditions': '',
                'diet': 'Any',
                'health': '',
                'cuisineType': '',
                'time': '',
                'excluded': ''
            }
        },
        {
            'name': 'Sedentary Female',
            'data': {
                'height': '160',
                'weight': '55',
                'age': '35',
                'gender': 'female',
                'activity_level': 'sedentary',
                'medical_conditions': '',
                'diet': 'Any',
                'health': '',
                'cuisineType': '',
                'time': '',
                'excluded': ''
            }
        },
        {
            'name': 'Custom Calorie Target',
            'data': {
                'height': '175',
                'weight': '70',
                'age': '30',
                'gender': 'male',
                'activity_level': 'moderately_active',
                'medical_conditions': '',
                'diet': 'Any',
                'health': '',
                'cuisineType': '',
                'time': '',
                'excluded': '',
                'calories': '2000'  # Custom calorie target
            }
        },
        {
            'name': 'With Dietary Restrictions',
            'data': {
                'height': '170',
                'weight': '65',
                'age': '28',
                'gender': 'female',
                'activity_level': 'lightly_active',
                'medical_conditions': '',
                'diet': 'low-carb',
                'health': 'vegan',
                'cuisineType': 'Italian',
                'time': '30',
                'excluded': 'nuts,shellfish'
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n--- {test_case['name']} ---")
        
        # Create the request
        request = factory.post('/plan_meal/', test_case['data'])
        request.session = {'UID': 'test_user_123'}
        
        try:
            # Call the meal planner function
            response = plan_meal(request)
            
            if response.status_code == 200:
                print(f"  ✅ Success - Status: {response.status_code}")
                
                # Check if the response contains the expected content
                content = response.content.decode('utf-8')
                
                # Verify that user inputs are reflected in the output
                for key, value in test_case['data'].items():
                    if value and key in ['height', 'weight', 'age', 'gender', 'activity_level']:
                        if value in content:
                            print(f"  ✅ {key}: {value} found in output")
                        else:
                            print(f"  ❌ {key}: {value} NOT found in output")
                
                # Check for meal plan structure
                if 'Day 1' in content and 'Day 7' in content:
                    print(f"  ✅ 7-day meal plan structure found")
                else:
                    print(f"  ❌ 7-day meal plan structure missing")
                
                # Check for meal types
                if 'Breakfast' in content and 'Lunch' in content and 'Dinner' in content:
                    print(f"  ✅ All meal types (Breakfast, Lunch, Dinner) found")
                else:
                    print(f"  ❌ Some meal types missing")
                
            else:
                print(f"  ❌ Failed - Status: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")

def test_calorie_distribution():
    """Test that calorie distribution is reasonable"""
    print("\n=== Testing Calorie Distribution ===")
    
    # Test with a known TDEE
    height, weight, age, gender, activity = 170, 70, 30, 'male', 'moderately_active'
    tdee = calculate_tdee(height, weight, age, gender, activity)
    
    print(f"TDEE: {tdee:.1f} calories")
    
    # Calculate expected meal distributions
    breakfast_min = max(tdee * 0.20, 100)
    breakfast_max = max(tdee * 0.30, 200)
    lunch_min = max(tdee * 0.30, 200)
    lunch_max = max(tdee * 0.40, 300)
    dinner_min = max(tdee * 0.35, 250)
    dinner_max = max(tdee * 0.45, 400)
    
    print(f"Breakfast range: {breakfast_min:.0f}-{breakfast_max:.0f} calories")
    print(f"Lunch range: {lunch_min:.0f}-{lunch_max:.0f} calories")
    print(f"Dinner range: {dinner_min:.0f}-{dinner_max:.0f} calories")
    
    total_min = breakfast_min + lunch_min + dinner_min
    total_max = breakfast_max + lunch_max + dinner_max
    
    print(f"Total daily range: {total_min:.0f}-{total_max:.0f} calories")
    print(f"TDEE coverage: {total_min/tdee*100:.1f}%-{total_max/tdee*100:.1f}%")
    
    # Verify the distribution is reasonable
    if total_min <= tdee <= total_max:
        print(f"  ✅ Calorie distribution covers TDEE appropriately")
    else:
        print(f"  ❌ Calorie distribution may not cover TDEE appropriately")

def test_input_validation():
    """Test input validation and error handling"""
    print("\n=== Testing Input Validation ===")
    
    invalid_cases = [
        {
            'name': 'Invalid Height',
            'data': {
                'height': 'invalid',
                'weight': '70',
                'age': '30',
                'gender': 'male',
                'activity_level': 'moderately_active'
            }
        },
        {
            'name': 'Missing Weight',
            'data': {
                'height': '170',
                'weight': '',
                'age': '30',
                'gender': 'male',
                'activity_level': 'moderately_active'
            }
        },
        {
            'name': 'Invalid Age',
            'data': {
                'height': '170',
                'weight': '70',
                'age': 'abc',
                'gender': 'male',
                'activity_level': 'moderately_active'
            }
        }
    ]
    
    for test_case in invalid_cases:
        print(f"\n--- {test_case['name']} ---")
        
        # Create the request
        request = factory.post('/plan_meal/', test_case['data'])
        request.session = {'UID': 'test_user_123'}
        
        try:
            response = plan_meal(request)
            
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                if 'error' in content.lower() or 'invalid' in content.lower():
                    print(f"  ✅ Properly handled invalid input")
                else:
                    print(f"  ❌ Invalid input not properly handled")
            else:
                print(f"  ✅ Proper error response (Status: {response.status_code})")
                
        except Exception as e:
            print(f"  ✅ Exception caught: {type(e).__name__}")

if __name__ == "__main__":
    print("Starting comprehensive meal planner validation tests...")
    
    test_tdee_calculation()
    test_calorie_distribution()
    test_input_validation()
    test_meal_planner_with_different_inputs()
    
    print("\n=== Test Summary ===")
    print("All tests completed. Check the output above for any issues.") 