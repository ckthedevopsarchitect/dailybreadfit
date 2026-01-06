"""
Database utilities for DynamoDB operations
"""
import boto3
from boto3.dynamodb.conditions import Key, Attr
from typing import Dict, List, Optional, Any
from config import settings
from datetime import datetime
import uuid


class DynamoDBClient:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_REGION)
        
    def get_table(self, table_name: str):
        """Get DynamoDB table resource"""
        return self.dynamodb.Table(table_name)
    
    def put_item(self, table_name: str, item: Dict) -> Dict:
        """Insert or update an item"""
        table = self.get_table(table_name)
        table.put_item(Item=item)
        return item
    
    def get_item(self, table_name: str, key: Dict) -> Optional[Dict]:
        """Get a single item by primary key"""
        table = self.get_table(table_name)
        response = table.get_item(Key=key)
        return response.get('Item')
    
    def query(self, table_name: str, key_condition: Any, 
              index_name: Optional[str] = None) -> List[Dict]:
        """Query items"""
        table = self.get_table(table_name)
        
        kwargs = {'KeyConditionExpression': key_condition}
        if index_name:
            kwargs['IndexName'] = index_name
            
        response = table.query(**kwargs)
        return response.get('Items', [])
    
    def scan(self, table_name: str, filter_expression: Optional[Any] = None) -> List[Dict]:
        """Scan table"""
        table = self.get_table(table_name)
        
        kwargs = {}
        if filter_expression:
            kwargs['FilterExpression'] = filter_expression
            
        response = table.scan(**kwargs)
        return response.get('Items', [])
    
    def update_item(self, table_name: str, key: Dict, 
                   update_expression: str, 
                   expression_values: Dict) -> Dict:
        """Update an item"""
        table = self.get_table(table_name)
        response = table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ReturnValues='ALL_NEW'
        )
        return response.get('Attributes', {})
    
    def delete_item(self, table_name: str, key: Dict) -> bool:
        """Delete an item"""
        table = self.get_table(table_name)
        table.delete_item(Key=key)
        return True


class S3Client:
    def __init__(self):
        self.s3 = boto3.client('s3', region_name=settings.AWS_REGION)
    
    def upload_file(self, file_content: bytes, bucket: str, key: str) -> str:
        """Upload file to S3"""
        self.s3.put_object(Bucket=bucket, Key=key, Body=file_content)
        return f"s3://{bucket}/{key}"
    
    def get_file(self, bucket: str, key: str) -> bytes:
        """Get file from S3"""
        response = self.s3.get_object(Bucket=bucket, Key=key)
        return response['Body'].read()
    
    def delete_file(self, bucket: str, key: str) -> bool:
        """Delete file from S3"""
        self.s3.delete_object(Bucket=bucket, Key=key)
        return True
    
    def generate_presigned_url(self, bucket: str, key: str, expiration: int = 3600) -> str:
        """Generate presigned URL for file access"""
        url = self.s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=expiration
        )
        return url


# Singleton instances
db_client = DynamoDBClient()
s3_client = S3Client()


def generate_id() -> str:
    """Generate unique ID"""
    return str(uuid.uuid4())


def get_timestamp() -> int:
    """Get current timestamp"""
    return int(datetime.utcnow().timestamp())
