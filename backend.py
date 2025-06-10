from flask import Flask, render_template, request, jsonify
"""
Flask: Web framework for handling HTTP requests.

render_template: Renders HTML templates.

request: Handles incoming HTTP request data (e.g., file uploads).

jsonify: Converts Python dictionaries to JSON responses.
"""
import boto3 #AWS SDK for Python (interacts with S3).
from werkzeug.utils import secure_filename #secure_filename: Sanitizes filenames to prevent security risks.
import os #os: Used to access environment variables.
from dotenv import load_dotenv #dotenv: Loads .env file for AWS credentials.
from datetime import datetime, timedelta # Used for pre-signed URL expiration.

app = Flask(__name__)

@app.route('/')  
def home():
    return render_template('index.html') 

load_dotenv()

#AWS CREDENTIALS FILE

AWS_ACCESS_KEY_ID = str(os.getenv('AWS_ACCESS_KEY_ID')) 
AWS_SECRET_ACCESS_KEY = str(os.getenv('AWS_SECRET_ACCESS_KEY'))

#S3 CONFIGURATION
S3_BUCKET = str(os.getenv('BUCKET_NAME'))
S3_REGION = str(os.getenv('BUCKET_REGION'))

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name = S3_REGION)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error':'No file uploaded'}) , 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error':'No file selected'}) , 400
    
    filename = secure_filename(file.filename) #secure_filename: Removes dangerous characters
    allowed_ext = {'pdf', 'jpg', 'jpeg', 'png', 'txt'}
    if not ('.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_ext):
        return jsonify({"error": "File type not allowed"})
    

    try:
        #upload file to s3 bucket
        s3.upload_fileobj(file, S3_BUCKET, filename) 

        presigned_url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': S3_BUCKET, 'Key': filename},
        ExpiresIn=3600  # 1 hour expiry
        )
        print("DEBUG: Upload successful") 

        return jsonify({
            "success": True,
            "filename": filename,
            "url": presigned_url
        }) , 200
    
    except Exception as e:
        print("DEBUG: Upload failed:", str(e))
        return jsonify({'error':str(e)}) , 500
    
@app.route('/files')
def list_files():
    try:
        # List all objects in the S3 bucket
        response = s3.list_objects_v2(Bucket=S3_BUCKET)
        files = []
        
        if 'Contents' in response:
            for item in response['Contents']:
                # Generate a pre-signed URL for each file
                presigned_url = s3.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': S3_BUCKET, 'Key': item['Key']},
                    ExpiresIn=3600  # 1 hour expiry
                )
                
                files.append({
                    'name': item['Key'],
                    'size': item['Size'],
                    'last_modified': item['LastModified'].isoformat(),
                    'url': presigned_url
                })
        
        return jsonify(files)
    
    except Exception as e:
        return jsonify({'error': str(e)}) , 500

if __name__ == '__main__':
    app.run(debug=True)