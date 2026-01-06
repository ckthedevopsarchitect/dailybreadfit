"""
DynamoDB table schemas for Daily Bread application
"""

# Users Table
USERS_TABLE_SCHEMA = {
    "TableName": "dailybread-users",
    "KeySchema": [
        {"AttributeName": "user_id", "KeyType": "HASH"}
    ],
    "AttributeDefinitions": [
        {"AttributeName": "user_id", "AttributeType": "S"},
        {"AttributeName": "email", "AttributeType": "S"}
    ],
    "GlobalSecondaryIndexes": [
        {
            "IndexName": "EmailIndex",
            "KeySchema": [
                {"AttributeName": "email", "KeyType": "HASH"}
            ],
            "Projection": {"ProjectionType": "ALL"}
        }
    ],
    "BillingMode": "PAY_PER_REQUEST"
}

# User Profiles Table
USER_PROFILES_TABLE_SCHEMA = {
    "TableName": "dailybread-user-profiles",
    "KeySchema": [
        {"AttributeName": "user_id", "KeyType": "HASH"}
    ],
    "AttributeDefinitions": [
        {"AttributeName": "user_id", "AttributeType": "S"}
    ],
    "BillingMode": "PAY_PER_REQUEST"
}

# Recipes Table
RECIPES_TABLE_SCHEMA = {
    "TableName": "dailybread-recipes",
    "KeySchema": [
        {"AttributeName": "recipe_id", "KeyType": "HASH"}
    ],
    "AttributeDefinitions": [
        {"AttributeName": "recipe_id", "AttributeType": "S"},
        {"AttributeName": "category", "AttributeType": "S"},
        {"AttributeName": "created_at", "AttributeType": "N"}
    ],
    "GlobalSecondaryIndexes": [
        {
            "IndexName": "CategoryIndex",
            "KeySchema": [
                {"AttributeName": "category", "KeyType": "HASH"},
                {"AttributeName": "created_at", "KeyType": "RANGE"}
            ],
            "Projection": {"ProjectionType": "ALL"}
        }
    ],
    "BillingMode": "PAY_PER_REQUEST"
}

# Daily Tips Table
DAILY_TIPS_TABLE_SCHEMA = {
    "TableName": "dailybread-daily-tips",
    "KeySchema": [
        {"AttributeName": "tip_id", "KeyType": "HASH"}
    ],
    "AttributeDefinitions": [
        {"AttributeName": "tip_id", "AttributeType": "S"},
        {"AttributeName": "created_at", "AttributeType": "N"}
    ],
    "GlobalSecondaryIndexes": [
        {
            "IndexName": "CreatedAtIndex",
            "KeySchema": [
                {"AttributeName": "created_at", "KeyType": "HASH"}
            ],
            "Projection": {"ProjectionType": "ALL"}
        }
    ],
    "BillingMode": "PAY_PER_REQUEST"
}

# User Favorites Table
USER_FAVORITES_TABLE_SCHEMA = {
    "TableName": "dailybread-user-favorites",
    "KeySchema": [
        {"AttributeName": "user_id", "KeyType": "HASH"},
        {"AttributeName": "item_id", "KeyType": "RANGE"}
    ],
    "AttributeDefinitions": [
        {"AttributeName": "user_id", "AttributeType": "S"},
        {"AttributeName": "item_id", "AttributeType": "S"}
    ],
    "BillingMode": "PAY_PER_REQUEST"
}

# Orders Table
ORDERS_TABLE_SCHEMA = {
    "TableName": "dailybread-orders",
    "KeySchema": [
        {"AttributeName": "order_id", "KeyType": "HASH"}
    ],
    "AttributeDefinitions": [
        {"AttributeName": "order_id", "AttributeType": "S"},
        {"AttributeName": "user_id", "AttributeType": "S"},
        {"AttributeName": "created_at", "AttributeType": "N"}
    ],
    "GlobalSecondaryIndexes": [
        {
            "IndexName": "UserOrdersIndex",
            "KeySchema": [
                {"AttributeName": "user_id", "KeyType": "HASH"},
                {"AttributeName": "created_at", "KeyType": "RANGE"}
            ],
            "Projection": {"ProjectionType": "ALL"}
        }
    ],
    "BillingMode": "PAY_PER_REQUEST"
}

# Meal Plans Table
MEAL_PLANS_TABLE_SCHEMA = {
    "TableName": "dailybread-meal-plans",
    "KeySchema": [
        {"AttributeName": "plan_id", "KeyType": "HASH"}
    ],
    "AttributeDefinitions": [
        {"AttributeName": "plan_id", "AttributeType": "S"},
        {"AttributeName": "user_id", "AttributeType": "S"}
    ],
    "GlobalSecondaryIndexes": [
        {
            "IndexName": "UserPlansIndex",
            "KeySchema": [
                {"AttributeName": "user_id", "KeyType": "HASH"}
            ],
            "Projection": {"ProjectionType": "ALL"}
        }
    ],
    "BillingMode": "PAY_PER_REQUEST"
}
