import boto3
import json
import pymysql
import sys
import time
from datetime import datetime

REGION = 'us-east-1'


rds_host  = "database-1.cbik5ogwsgag.us-east-1.rds.amazonaws.com"
name = "kas1085"
password = "nandanam13!"
db_name = "cloudproject"





#import pymysql
import sys

def main(event, context):
    # TODO implement
    comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
    #print(event,"eveeeent")
    
    
    json_filename = event['Records'][0]['s3']['object']['key']
    #print(decoded_json)
    


    s3 = boto3.resource('s3')

    content_object = s3.Object('amazon-transcribed-text', json_filename)
    file_content = content_object.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    #print(json_content['results']['transcripts'][0]['transcript'])
    
    
    text = json_content['results']['transcripts'][0]['transcript']
    
    print('Calling DetectSentiment')
    detect_sentiment = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    print("----",detect_sentiment['Sentiment'])
    print('End of DetectSentiment\n')
    
    
    
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    
    now = datetime.now()
    current_timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
   
    print(type(current_timestamp))
    sentiment = detect_sentiment['Sentiment'].lower()
    time_stamp = current_timestamp
    with conn.cursor() as cur:
        cur.execute("""insert into sentiments (time_stamp, sentiment) values( '%s', '%s')""" % (time_stamp, sentiment))
        conn.commit()
        cur.close()
    
    
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }






# event = {
#   "id": 777,
#   "name": "appychip"
# }
# context = ""
# main(event, context)
