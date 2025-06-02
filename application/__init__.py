from flask import Flask
from flask_dropzone import Dropzone
import os

app = Flask(__name__)
dropzone = Dropzone(app)

# Set a secret key for session and Flask-WTF
app.secret_key = 'my-dev-secret-key'  # Replace with a secure key in production

# Set upload paths
app.config['UPLOADED_PATH'] = os.path.join(app.root_path, 'static', 'uploaded_files')
app.config['AUDIO_FILE_UPLOAD'] = os.path.join(app.root_path, 'static', 'audio_files')

# Flask-Dropzone config (optional if you are using drag & drop uploads)
app.config['DROPZONE_UPLOAD_MULTIPLE'] = False
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
app.config['DROPZONE_MAX_FILE_SIZE'] = 3

# Import routes at the end to avoid circular import errors
from application import routes
