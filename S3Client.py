import boto3
from decouple import config

class S3Client:
    def __init__(self):
        self.s3 = boto3.resource('s3', aws_access_key_id=config('S3_ACCESS_KEY_ID'), aws_secret_access_key=config('S3_ACCESS_SECRET_KEY'))
        self.s3_bucket = self.s3.Bucket(config('S3_BUCKET_NAME'))
        self.s3_client = boto3.client('s3')
        self.bucket_name = config('S3_BUCKET_NAME')
        
        
    def upload(self, file, filename, folder="raw"):
        self.s3_bucket.put_object(
            Key=f"{folder}/{filename}",
            Body=file
        )
        
    def getAllFilenames(self, folder="raw"):
        audio_files = []
        folder_filter = f"{folder}/"
        for audio in self.s3_bucket.objects.filter(Prefix=folder_filter):
            audio_files.append(audio.key)
            
        return audio_files[1:]
    
    def retrieveAudioFiles(self, folder="raw"):
        audio_files = self.getAllFilenames(folder) 
        raw_files = []

        for file in audio_files:
            obj = self.s3.Object(self.bucket_name, file)
            content = obj.get()['Body'].read() 
            
            raw_files.append((file, content)) 
            
        return raw_files
    
    def getContents(self, key):
        fileObject = self.s3.Object(self.bucket_name, key)
        
        return fileObject.get()['Body']
        
    
  
    
    
     