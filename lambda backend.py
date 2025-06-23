import json
import boto3
from datetime import datetime

s3 = boto3.client('s3')

BUCKET_NAME = 'bucketcsv'  # Replace with your actual bucket name
CSV_FILE_KEY = 'registrations/registration.csv'

def lambda_handler(event, context):
    try:
        # Parse request body
        body = json.loads(event['body'])
        name = body.get('name')
        email = body.get('email')
        age = body.get('age')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if not name or not email or not age:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST'
                },
                'body': json.dumps({'message': 'Missing required fields'})
            }

        # Create CSV line
        new_line = f"{name},{email},{age},{timestamp}\n"

        # Try to read existing file
        try:
            response = s3.get_object(Bucket=BUCKET_NAME, Key=CSV_FILE_KEY)
            existing_csv = response['Body'].read().decode('utf-8')
        except s3.exceptions.NoSuchKey:
            existing_csv = "Name,Email,Age,Timestamp\n"

        # Append new line and write back to S3
        updated_csv = existing_csv + new_line
        s3.put_object(Bucket=BUCKET_NAME, Key=CSV_FILE_KEY, Body=updated_csv.encode('utf-8'))

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({'message': 'Registration complete!'})
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({'message': f'Error: {str(e)}'})
        }
