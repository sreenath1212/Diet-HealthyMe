# Meal Planner Setup Guide

## API Configuration

The 7-day meal planner requires Edamam API credentials to function properly. Follow these steps to set up the API:

### 1. Get Edamam API Credentials

1. Go to [Edamam Recipe API](https://developer.edamam.com/edamam-recipe-api)
2. Sign up for a free account
3. Create a new application to get your API credentials
4. Note down your `APP_ID` and `APP_KEY`

### 2. Set Environment Variables

Create a `.env` file in the project root with the following content:

```
EDAMAM_APP_ID=your_app_id_here
EDAMAM_APP_KEY=your_app_key_here
```

Replace `your_app_id_here` and `your_app_key_here` with your actual Edamam API credentials.

### 3. Install Required Dependencies

Make sure you have the `python-dotenv` package installed:

```bash
pip install python-dotenv
```

### 4. Restart the Django Server

After setting up the environment variables, restart your Django development server:

```bash
python manage.py runserver
```

## Troubleshooting

### Common Issues:

1. **"Edamam API credentials are not configured"**
   - Make sure you have created a `.env` file with the correct API credentials
   - Ensure the `.env` file is in the project root directory
   - Restart the Django server after adding the credentials

2. **"No recipes found"**
   - Check your internet connection
   - Verify that your API credentials are correct
   - Try adjusting the meal planner filters (diet, health, cuisine type, etc.)

3. **"Network Error"**
   - Check your internet connection
   - The Edamam API might be temporarily unavailable
   - Try again later

## Features

The meal planner includes:
- Personalized calorie calculation based on height, weight, age, gender, and activity level
- 7-day meal plans with 3 meals per day (breakfast, lunch, dinner)
- Dietary restrictions and health filters
- Cuisine type preferences
- Cooking time limits
- Ingredient exclusions
- Automatic meal plan saving for logged-in users 