"""
Recipes Lambda function handler
Handles CRUD operations for recipes
"""
import json
from typing import Dict, Any
from database import db_client, generate_id, get_timestamp
from auth import decode_token
from config import settings
from boto3.dynamodb.conditions import Key


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Main Lambda handler router for recipes"""
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
        'Content-Type': 'application/json'
    }
    
    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}
    
    try:
        path = event.get('path', '')
        http_method = event.get('httpMethod', '')
        
        # Route to appropriate handler
        if path.endswith('/recipes') and http_method == 'GET':
            return get_recipes(event, headers)
        elif path.endswith('/recipes') and http_method == 'POST':
            return create_recipe(event, headers)
        elif '/recipes/' in path and http_method == 'GET':
            return get_recipe(event, headers)
        elif '/recipes/' in path and http_method == 'PUT':
            return update_recipe(event, headers)
        elif '/recipes/' in path and http_method == 'DELETE':
            return delete_recipe(event, headers)
        elif path.endswith('/search') and http_method == 'GET':
            return search_recipes(event, headers)
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'message': 'Not Found'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': 'Internal Server Error', 'error': str(e)})
        }


def get_recipes(event: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
    """Get all recipes with optional category filter"""
    try:
        params = event.get('queryStringParameters') or {}
        category = params.get('category')
        
        if category:
            recipes = db_client.query(
                settings.RECIPES_TABLE,
                Key('category').eq(category),
                index_name='CategoryIndex'
            )
        else:
            recipes = db_client.scan(settings.RECIPES_TABLE)
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'recipes': recipes})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': 'Failed to get recipes', 'error': str(e)})
        }


def get_recipe(event: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
    """Get a single recipe by ID"""
    try:
        path_params = event.get('pathParameters') or {}
        recipe_id = path_params.get('id')
        
        if not recipe_id:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'message': 'Recipe ID required'})
            }
        
        recipe = db_client.get_item(settings.RECIPES_TABLE, {'recipe_id': recipe_id})
        
        if not recipe:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'message': 'Recipe not found'})
            }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(recipe)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': 'Failed to get recipe', 'error': str(e)})
        }


def create_recipe(event: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
    """Create a new recipe (admin only)"""
    try:
        # TODO: Add admin authorization check
        
        body = json.loads(event.get('body', '{}'))
        
        recipe = {
            'recipe_id': generate_id(),
            'name': body.get('name'),
            'description': body.get('description'),
            'category': body.get('category'),
            'ingredients': body.get('ingredients', []),
            'instructions': body.get('instructions', []),
            'prep_time': body.get('prep_time', 0),
            'cook_time': body.get('cook_time', 0),
            'servings': body.get('servings', 1),
            'nutrition': body.get('nutrition', {}),
            'image_url': body.get('image_url'),
            'difficulty': body.get('difficulty', 'medium'),
            'tags': body.get('tags', []),
            'created_at': get_timestamp(),
            'updated_at': get_timestamp()
        }
        
        db_client.put_item(settings.RECIPES_TABLE, recipe)
        
        return {
            'statusCode': 201,
            'headers': headers,
            'body': json.dumps(recipe)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': 'Failed to create recipe', 'error': str(e)})
        }


def update_recipe(event: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
    """Update a recipe (admin only)"""
    try:
        # TODO: Add admin authorization check
        
        path_params = event.get('pathParameters') or {}
        recipe_id = path_params.get('id')
        
        if not recipe_id:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'message': 'Recipe ID required'})
            }
        
        body = json.loads(event.get('body', '{}'))
        
        # Build update expression dynamically
        update_expr = "SET updated_at = :updated_at"
        expr_values = {':updated_at': get_timestamp()}
        
        for key in ['name', 'description', 'category', 'ingredients', 'instructions', 
                   'prep_time', 'cook_time', 'servings', 'nutrition', 'image_url', 
                   'difficulty', 'tags']:
            if key in body:
                update_expr += f", {key} = :{key}"
                expr_values[f':{key}'] = body[key]
        
        updated_recipe = db_client.update_item(
            settings.RECIPES_TABLE,
            {'recipe_id': recipe_id},
            update_expr,
            expr_values
        )
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(updated_recipe)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': 'Failed to update recipe', 'error': str(e)})
        }


def delete_recipe(event: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
    """Delete a recipe (admin only)"""
    try:
        # TODO: Add admin authorization check
        
        path_params = event.get('pathParameters') or {}
        recipe_id = path_params.get('id')
        
        if not recipe_id:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'message': 'Recipe ID required'})
            }
        
        db_client.delete_item(settings.RECIPES_TABLE, {'recipe_id': recipe_id})
        
        return {
            'statusCode': 204,
            'headers': headers,
            'body': ''
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': 'Failed to delete recipe', 'error': str(e)})
        }


def search_recipes(event: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
    """Search recipes by query string"""
    try:
        params = event.get('queryStringParameters') or {}
        query = params.get('q', '').lower()
        
        if not query:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'message': 'Search query required'})
            }
        
        # Simple search - in production, use Elasticsearch or DynamoDB Search
        all_recipes = db_client.scan(settings.RECIPES_TABLE)
        
        results = [
            recipe for recipe in all_recipes
            if query in recipe.get('name', '').lower() or
               query in recipe.get('description', '').lower() or
               query in str(recipe.get('tags', [])).lower()
        ]
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'recipes': results, 'count': len(results)})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': 'Search failed', 'error': str(e)})
        }
