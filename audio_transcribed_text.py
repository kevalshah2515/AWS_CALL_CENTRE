import json
import time
import boto3
from datetime import datetime  
import time

def lambda_handler(event, context):
    # TODO implement
    print(event)
    
    time.sleep(7)
    transcribe = boto3.client('transcribe')
    curr_time = datetime.now()
    job_name = "speech_to_text"+str(int(datetime.timestamp(curr_time)))
    print(job_name)
    job_uri = "https://amazon-customer-audio.s3.amazonaws.com/"+event['Records'][0]['s3']['object']['key']
    print(job_uri)
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='wav',
        LanguageCode='en-US',
        OutputBucketName='amazon-transcribed-text'
    )
    
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet...")
        time.sleep(5)
    print(status)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

