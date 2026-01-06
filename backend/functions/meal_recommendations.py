"""
AI-powered meal recommendation Lambda function
"""
import json
import os
from typing import Dict, Any, List
from database import db_client
from auth import decode_token
from config import settings

# OpenAI for AI recommendations
try:
    from openai import OpenAI
    openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
    OPENAI_AVAILABLE = True
except:
    OPENAI_AVAILABLE = False


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Main Lambda handler for meal recommendations"""
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
        'Content-Type': 'application/json'
    }
    
    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}
    
    try:
        # Extract user from token
        auth_header = event.get('headers', {}).get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return {
                'statusCode': 401,
                'headers': headers,
                'body': json.dumps({'message': 'Unauthorized'})
            }
        
        token = auth_header.split(' ')[1]
        payload = decode_token(token)
        
        if not payload:
            return {
                'statusCode': 401,
                'headers': headers,
                'body': json.dumps({'message': 'Invalid token'})
            }
        
        user_id = payload.get('sub')
        
        # Get user profile
        profile = db_client.get_item(settings.USER_PROFILES_TABLE, {'user_id': user_id})
        
        if not profile:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'message': 'User profile not found'})
            }
        
        # Get request body
        body = json.loads(event.get('body', '{}'))
        meal_type = body.get('meal_type', 'lunch')  # breakfast, lunch, dinner
        
        # Generate recommendations
        recommendations = generate_meal_recommendations(profile, meal_type)
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'meal_type': meal_type,
                'recommendations': recommendations
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': 'Failed to generate recommendations', 'error': str(e)})
        }


def generate_meal_recommendations(profile: Dict[str, Any], meal_type: str) -> List[Dict[str, Any]]:
    """Generate AI-powered meal recommendations based on user profile"""
    
    # Extract user preferences
    fitness_goal = profile.get('fitness_goal', 'maintenance')
    dietary_preferences = profile.get('dietary_preferences', [])
    allergies = profile.get('allergies', [])
    activity_level = profile.get('activity_level', 'moderate')
    
    # Calculate nutritional needs
    calories = calculate_calorie_needs(profile)
    macros = calculate_macros(calories, fitness_goal)
    
    if OPENAI_AVAILABLE and settings.OPENAI_API_KEY:
        # Use OpenAI for intelligent recommendations
        recommendations = get_ai_recommendations(
            fitness_goal, dietary_preferences, allergies, 
            activity_level, meal_type, macros
        )
    else:
        # Fallback to rule-based recommendations
        recommendations = get_rule_based_recommendations(
            fitness_goal, dietary_preferences, allergies, meal_type, macros
        )
    
    return recommendations


def calculate_calorie_needs(profile: Dict[str, Any]) -> int:
    """Calculate daily calorie needs using Mifflin-St Jeor Equation"""
    
    weight = profile.get('weight', 70)  # kg
    height = profile.get('height', 170)  # cm
    age = profile.get('age', 30)
    gender = profile.get('gender', 'other')
    activity_level = profile.get('activity_level', 'moderate')
    fitness_goal = profile.get('fitness_goal', 'maintenance')
    
    # Base Metabolic Rate (BMR)
    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif gender == 'female':
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 78
    
    # Activity multipliers
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    
    tdee = bmr * activity_multipliers.get(activity_level, 1.55)
    
    # Adjust for fitness goal
    if fitness_goal == 'weight_loss':
        calories = tdee - 500
    elif fitness_goal == 'weight_gain':
        calories = tdee + 500
    else:  # maintenance
        calories = tdee
    
    return int(calories)


def calculate_macros(calories: int, fitness_goal: str) -> Dict[str, int]:
    """Calculate macronutrient distribution"""
    
    if fitness_goal == 'weight_loss':
        # Higher protein, moderate fat, lower carbs
        protein_ratio = 0.40
        carb_ratio = 0.30
        fat_ratio = 0.30
    elif fitness_goal == 'weight_gain':
        # Higher carbs and protein, moderate fat
        protein_ratio = 0.30
        carb_ratio = 0.45
        fat_ratio = 0.25
    else:  # maintenance or muscle_gain
        # Balanced
        protein_ratio = 0.30
        carb_ratio = 0.40
        fat_ratio = 0.30
    
    return {
        'protein': int((calories * protein_ratio) / 4),  # 4 cal per gram
        'carbs': int((calories * carb_ratio) / 4),
        'fat': int((calories * fat_ratio) / 9),  # 9 cal per gram
        'calories': calories
    }


def get_ai_recommendations(fitness_goal: str, dietary_preferences: List[str], 
                          allergies: List[str], activity_level: str, 
                          meal_type: str, macros: Dict[str, int]) -> List[Dict[str, Any]]:
    """Get AI-powered meal recommendations using OpenAI"""
    
    prompt = f"""Generate 3 nutritious {meal_type} meal recommendations for someone with the following profile:

Fitness Goal: {fitness_goal}
Dietary Preferences: {', '.join(dietary_preferences) if dietary_preferences else 'None'}
Allergies: {', '.join(allergies) if allergies else 'None'}
Activity Level: {activity_level}

Target Macros per meal:
- Calories: {macros['calories'] // 3} cal
- Protein: {macros['protein'] // 3}g
- Carbs: {macros['carbs'] // 3}g
- Fat: {macros['fat'] // 3}g

For each meal, provide:
1. Meal name
2. Description
3. Ingredients list
4. Estimated nutritional info (calories, protein, carbs, fat)
5. Preparation time
6. Difficulty level

Format as JSON array."""

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional nutritionist and meal planner."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        content = response.choices[0].message.content
        # Parse JSON from response
        recommendations = json.loads(content)
        return recommendations
        
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return get_rule_based_recommendations(fitness_goal, dietary_preferences, allergies, meal_type, macros)


def get_rule_based_recommendations(fitness_goal: str, dietary_preferences: List[str],
                                   allergies: List[str], meal_type: str, 
                                   macros: Dict[str, int]) -> List[Dict[str, Any]]:
    """Fallback rule-based recommendations"""
    
    meal_calories = macros['calories'] // 3
    meal_protein = macros['protein'] // 3
    meal_carbs = macros['carbs'] // 3
    meal_fat = macros['fat'] // 3
    
    recommendations = []
    
    if meal_type == 'breakfast':
        recommendations = [
            {
                "name": "High-Protein Oatmeal Bowl",
                "description": "Creamy oatmeal topped with nuts, seeds, and berries",
                "ingredients": ["Oats", "Protein powder", "Almonds", "Blueberries", "Chia seeds"],
                "nutrition": {
                    "calories": meal_calories,
                    "protein": meal_protein,
                    "carbs": meal_carbs,
                    "fat": meal_fat
                },
                "prep_time": "10 minutes",
                "difficulty": "easy"
            },
            {
                "name": "Veggie Egg White Scramble",
                "description": "Light and nutritious egg whites with colorful vegetables",
                "ingredients": ["Egg whites", "Spinach", "Tomatoes", "Bell peppers", "Whole grain toast"],
                "nutrition": {
                    "calories": meal_calories,
                    "protein": meal_protein,
                    "carbs": meal_carbs,
                    "fat": meal_fat
                },
                "prep_time": "15 minutes",
                "difficulty": "easy"
            },
            {
                "name": "Greek Yogurt Parfait",
                "description": "Layered Greek yogurt with granola and fresh fruit",
                "ingredients": ["Greek yogurt", "Granola", "Mixed berries", "Honey", "Walnuts"],
                "nutrition": {
                    "calories": meal_calories,
                    "protein": meal_protein,
                    "carbs": meal_carbs,
                    "fat": meal_fat
                },
                "prep_time": "5 minutes",
                "difficulty": "easy"
            }
        ]
    elif meal_type == 'lunch':
        recommendations = [
            {
                "name": "Grilled Chicken Salad",
                "description": "Fresh mixed greens with grilled chicken breast",
                "ingredients": ["Chicken breast", "Mixed greens", "Cherry tomatoes", "Cucumber", "Olive oil"],
                "nutrition": {
                    "calories": meal_calories,
                    "protein": meal_protein,
                    "carbs": meal_carbs,
                    "fat": meal_fat
                },
                "prep_time": "20 minutes",
                "difficulty": "medium"
            },
            {
                "name": "Quinoa Buddha Bowl",
                "description": "Colorful bowl with quinoa, roasted vegetables, and tahini",
                "ingredients": ["Quinoa", "Chickpeas", "Sweet potato", "Kale", "Tahini"],
                "nutrition": {
                    "calories": meal_calories,
                    "protein": meal_protein,
                    "carbs": meal_carbs,
                    "fat": meal_fat
                },
                "prep_time": "30 minutes",
                "difficulty": "medium"
            },
            {
                "name": "Turkey and Avocado Wrap",
                "description": "Lean turkey breast with fresh avocado in whole wheat wrap",
                "ingredients": ["Turkey breast", "Avocado", "Whole wheat wrap", "Lettuce", "Tomato"],
                "nutrition": {
                    "calories": meal_calories,
                    "protein": meal_protein,
                    "carbs": meal_carbs,
                    "fat": meal_fat
                },
                "prep_time": "10 minutes",
                "difficulty": "easy"
            }
        ]
    else:  # dinner
        recommendations = [
            {
                "name": "Baked Salmon with Vegetables",
                "description": "Omega-3 rich salmon with roasted seasonal vegetables",
                "ingredients": ["Salmon fillet", "Broccoli", "Carrots", "Lemon", "Herbs"],
                "nutrition": {
                    "calories": meal_calories,
                    "protein": meal_protein,
                    "carbs": meal_carbs,
                    "fat": meal_fat
                },
                "prep_time": "25 minutes",
                "difficulty": "medium"
            },
            {
                "name": "Lean Beef Stir-Fry",
                "description": "Tender beef strips with colorful vegetables",
                "ingredients": ["Lean beef", "Bell peppers", "Snap peas", "Brown rice", "Soy sauce"],
                "nutrition": {
                    "calories": meal_calories,
                    "protein": meal_protein,
                    "carbs": meal_carbs,
                    "fat": meal_fat
                },
                "prep_time": "20 minutes",
                "difficulty": "medium"
            },
            {
                "name": "Vegetarian Lentil Curry",
                "description": "Hearty lentil curry with aromatic spices",
                "ingredients": ["Red lentils", "Coconut milk", "Spinach", "Tomatoes", "Curry spices"],
                "nutrition": {
                    "calories": meal_calories,
                    "protein": meal_protein,
                    "carbs": meal_carbs,
                    "fat": meal_fat
                },
                "prep_time": "35 minutes",
                "difficulty": "medium"
            }
        ]
    
    return recommendations
