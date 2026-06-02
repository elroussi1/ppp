from flask import Flask, render_template, request, send_file
from PIL import Image, ImageFilter
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
EDITED_FOLDER = 'edited'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EDITED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Example edit: grayscale + sharpen
    img = Image.open(filepath)
    edited = img.convert("L").filter(ImageFilter.SHARPEN)

    edited_path = os.path.join(EDITED_FOLDER, "edited_" + file.filename)
    # Save with high quality
    edited.save(edited_path, quality=95, optimize=True)

    return render_template("result.html",
                           original=os.path.basename(filepath),
                           edited=os.path.basename(edited_path))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename))

@app.route('/edited/<filename>')
def edited_file(filename):
    return send_file(os.path.join(EDITED_FOLDER, filename))

@app.route('/download/<filename>')
def download_file(filename):
    path = os.path.join(EDITED_FOLDER, filename)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
