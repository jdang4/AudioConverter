import boto3
from decouple import config

class S3Client:
    def __init__(self):
        self.s3 = boto3.resource('s3', aws_access_key_id=config('S3_ACCESS_KEY_ID'), aws_secret_access_key=config('S3_ACCESS_SECRET_KEY'))
        self.s3_bucket = self.s3.Bucket(config('S3_BUCKET_NAME'))
        self.s3_client = boto3.client('s3')
        self.bucket_name = config('S3_BUCKET_NAME')
        
        
    def upload(self, file, filename):
        self.s3_bucket.put_object(
            Key=filename,
            Body=file
        )
        
    def __getAllFilenames(self):
        audio_files = []
        for audio in self.s3_bucket.objects.all():
            audio_files.append(audio.key)
            
        return audio_files
    
    def retrieveAudioFiles(self):
        audio_files = self.__getAllFilenames() 
        raw_files = []

        for file in audio_files:
            obj = self.s3.Object(self.bucket_name, file)
            content = obj.get()['Body'].read() 
            
            raw_files.append((file, content)) 
            
        
        '''
	    for audio in audio_files:
		    tmp_path = os.path.join(app.config['UPLOAD_FOLDER'], audio[0])
		    f = open(tmp_path, 'wb')
		    f.write(audio[1])
		    f.close()
	    '''
            
        return raw_files
    
  
    
    
     