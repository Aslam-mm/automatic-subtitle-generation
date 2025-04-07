from flask import Flask, request, render_template, send_from_directory
import os 
from videoProcess import VideoProcess
# Allowed video extensions
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'videos'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-subtitle', methods=['POST'])
def generate_subtitle():
    if 'myfile' not in request.files:
        return render_template('index.html', message='No file part')

    video_file = request.files['myfile']

    if video_file.filename == '':
        return render_template('index.html', message='No selected file')

    if not allowed_file(video_file.filename):
        return render_template('index.html', message='Invalid file type. Please upload a video.')

    filename = video_file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    video_file.save(filepath)

    process = VideoProcess(filepath) 
    subtitled_video = os.path.splitext(filename)[0] + '_subtitled.mp4'

    return render_template('index.html', message='Video uploaded and processed successfully.', video_file=subtitled_video)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
