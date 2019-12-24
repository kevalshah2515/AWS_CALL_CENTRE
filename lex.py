import json
import boto3
import datetime
from botocore.vendored import requests
from boto3.dynamodb.conditions import Key, Attr

def dispatch(intent_request):
    
    intent_name = intent_request['currentIntent']['name']
    if intent_name == 'GetCreditsInformation':
        return GetCreditsInformation_intent(intent_request)

def get_slots(intent_request):
    return intent_request['currentIntent']['slots']

def GetCreditsInformation_intent(intent_request): 
    print("inside GetCreditsInformation_intent")
    email = get_slots(intent_request)["email"]
    email = int(email)
    print(email)
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    print("after dynamodb")
    table = dynamodb.Table('CustomerData')
    print("after table")    

    responseData = table.query(KeyConditionExpression=Key('email').eq(email))
    print("printing response data")
    print(responseData['Items'][0]['info']['amount_used'])
    
    response_text = "You have " + str(responseData['Items'][0]['info']['amount_used']) + " credits left"
    return {
        'dialogAction': {
            "type": "ElicitIntent",
            'message': {
                'contentType': 'PlainText', 
                'content': response_text }
        }
    }


def lambda_handler(event, context):
    # TODO implement
    print(event)
    
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello from Lambda!')
    # }
    
    return dispatch(event)
    
    
