from flask import Flask, render_template, request, send_file #pip install flask
from PIL import Image #pip install pillow
import os #pip install os-sys

app = Flask(__name__)

# Create the 'uploads' directory if it doesn't exist
uploads_dir = os.path.join(app.instance_path, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)

# Replace this with the actual implementation of your compression algorithm
def compress_image(input_image_path, output_image_path, block_size=8):
    # Open the input image
    img = Image.open(input_image_path)
    
    # Get the size of the image
    width, height = img.size
    
    # Create a new image for the compressed result
    compressed_img = Image.new('RGB', (width, height))
    
    # Iterate through the image in block_size x block_size blocks
    for x in range(0, width, block_size):
        for y in range(0, height, block_size):
            # Crop the block from the original image
            block = img.crop((x, y, x + block_size, y + block_size))
            
            # Perform your compression algorithm on the block here
            # Replace this with your actual compression logic
            
            # Paste the compressed block into the result image
            compressed_img.paste(block, (x, y))
    
    # Save the compressed image
    compressed_img.save(output_image_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', error='No selected file')

    if file:
        input_image_path = os.path.join(uploads_dir, 'original.jpg')
        output_image_path = os.path.join(uploads_dir, 'compressed.jpg')

        file.save(input_image_path)

        # Replace this with the actual implementation of your compression algorithm
        compress_image(input_image_path, output_image_path)

        return render_template('index.html', compressed=True)

@app.route('/download')
def download():
    return send_file(os.path.join(uploads_dir, 'compressed.jpg'), as_attachment=True)
   


if __name__ == '__main__':
    app.run(debug=True)
