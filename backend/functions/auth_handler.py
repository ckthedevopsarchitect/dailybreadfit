"""
User authentication Lambda functions
"""
import json
from typing import Dict, Any
from database import db_client, generate_id, get_timestamp
from auth import get_password_hash, verify_password, create_access_token, create_refresh_token, decode_token
from config import settings
from boto3.dynamodb.conditions import Key


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Main Lambda handler router"""
    
    try:
        path = event.get('path', '')
        http_method = event.get('httpMethod', '')
        
        # CORS headers
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
            'Content-Type': 'application/json'
        }
        
        # Handle OPTIONS for CORS
        if http_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        # Route to appropriate handler
        if path.endswith('/register') and http_method == 'POST':
            return register(event, headers)
        elif path.endswith('/login') and http_method == 'POST':
            return login(event, headers)
        elif path.endswith('/refresh') and http_method == 'POST':
            return refresh_token(event, headers)
        elif path.endswith('/me') and http_method == 'GET':
            return get_current_user(event, headers)
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


def register(event: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
    """Register a new user"""
    try:
        body = json.loads(event.get('body', '{}'))
        
        email = body.get('email')
        password = body.get('password')
        name = body.get('name')
        
        if not email or not password:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'message': 'Email and password required'})
            }
        
        # Check if user already exists
        existing_users = db_client.query(
            settings.USERS_TABLE,
            Key('email').eq(email),
            index_name='EmailIndex'
        )
        
        if existing_users:
            return {
                'statusCode': 409,
                'headers': headers,
                'body': json.dumps({'message': 'User already exists'})
            }
        
        # Create user
        user_id = generate_id()
        user = {
            'user_id': user_id,
            'email': email,
            'password_hash': get_password_hash(password),
            'name': name,
            'created_at': get_timestamp(),
            'is_active': True,
            'role': 'user'
        }
        
        db_client.put_item(settings.USERS_TABLE, user)
        
        # Create user profile
        profile = {
            'user_id': user_id,
            'fitness_goal': body.get('fitness_goal', 'maintenance'),
            'dietary_preferences': body.get('dietary_preferences', []),
            'allergies': body.get('allergies', []),
            'height': body.get('height'),
            'weight': body.get('weight'),
            'age': body.get('age'),
            'gender': body.get('gender'),
            'activity_level': body.get('activity_level', 'moderate'),
            'created_at': get_timestamp()
        }
        
        db_client.put_item(settings.USER_PROFILES_TABLE, profile)
        
        # Generate tokens
        access_token = create_access_token({"sub": user_id})
        refresh_token = create_refresh_token({"sub": user_id})
        
        return {
            'statusCode': 201,
            'headers': headers,
            'body': json.dumps({
                'user_id': user_id,
                'email': email,
                'name': name,
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'bearer'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': 'Registration failed', 'error': str(e)})
        }


def login(event: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
    """Login user"""
    try:
        body = json.loads(event.get('body', '{}'))
        
        email = body.get('email')
        password = body.get('password')
        
        if not email or not password:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'message': 'Email and password required'})
            }
        
        # Find user by email
        users = db_client.query(
            settings.USERS_TABLE,
            Key('email').eq(email),
            index_name='EmailIndex'
        )
        
        if not users:
            return {
                'statusCode': 401,
                'headers': headers,
                'body': json.dumps({'message': 'Invalid credentials'})
            }
        
        user = users[0]
        
        # Verify password
        if not verify_password(password, user['password_hash']):
            return {
                'statusCode': 401,
                'headers': headers,
                'body': json.dumps({'message': 'Invalid credentials'})
            }
        
        if not user.get('is_active', True):
            return {
                'statusCode': 403,
                'headers': headers,
                'body': json.dumps({'message': 'Account is inactive'})
            }
        
        # Generate tokens
        access_token = create_access_token({"sub": user['user_id']})
        refresh_token = create_refresh_token({"sub": user['user_id']})
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'user_id': user['user_id'],
                'email': user['email'],
                'name': user.get('name'),
                'role': user.get('role', 'user'),
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'bearer'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': 'Login failed', 'error': str(e)})
        }


def refresh_token(event: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
    """Refresh access token"""
    try:
        body = json.loads(event.get('body', '{}'))
        refresh_token_str = body.get('refresh_token')
        
        if not refresh_token_str:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'message': 'Refresh token required'})
            }
        
        payload = decode_token(refresh_token_str)
        
        if not payload or payload.get('type') != 'refresh':
            return {
                'statusCode': 401,
                'headers': headers,
                'body': json.dumps({'message': 'Invalid refresh token'})
            }
        
        user_id = payload.get('sub')
        access_token = create_access_token({"sub": user_id})
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'access_token': access_token,
                'token_type': 'bearer'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': 'Token refresh failed', 'error': str(e)})
        }


def get_current_user(event: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
    """Get current user info"""
    try:
        auth_header = event.get('headers', {}).get('Authorization', '')
        
        if not auth_header.startswith('Bearer '):
            return {
                'statusCode': 401,
                'headers': headers,
                'body': json.dumps({'message': 'Missing or invalid authorization header'})
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
        user = db_client.get_item(settings.USERS_TABLE, {'user_id': user_id})
        
        if not user:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'message': 'User not found'})
            }
        
        # Remove sensitive data
        user.pop('password_hash', None)
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(user)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': 'Failed to get user', 'error': str(e)})
        }
