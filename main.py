from flask import Flask, render_template, request, send_file, after_this_request
from file_conversion import convert_pdf_to_jpeg, convert_pdf_to_png, jpeg_to_png, png_to_jpeg
from file_tools import lock_pdf, unlock_pdf
from image_compressor import reduce_image_size
import os
import zipfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert/pdf-to-jpeg', methods=['POST'])
def convert_pdf_to_jpeg_endpoint():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    pdf_path = 'uploaded_file.pdf'
    file.save(pdf_path)

    jpeg_paths = convert_pdf_to_jpeg(pdf_path)

    # Create a zip file containing all JPEG images
    with zipfile.ZipFile('converted_images.zip', 'w') as zip_file:
        for jpeg_path in jpeg_paths:
            zip_file.write(jpeg_path, os.path.basename(jpeg_path))

    # Delete the PDF file and JPEG images after conversion
    os.remove(pdf_path)
    for jpeg_path in jpeg_paths:
        os.remove(jpeg_path)

    return send_file('converted_images.zip', as_attachment=True)

@app.route('/convert/pdf-to-png', methods=['POST'])
def convert_pdf_to_png_endpoint():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    pdf_path = 'uploaded_file.pdf'
    file.save(pdf_path)

    png_paths = convert_pdf_to_png(pdf_path)

    # Create a zip file containing all PNG images
    with zipfile.ZipFile('converted_images.zip', 'w') as zip_file:
        for png_path in png_paths:
            zip_file.write(png_path, os.path.basename(png_path))

    # Delete the PDF file and PNG images after conversion
    os.remove(pdf_path)
    for png_path in png_paths:
        os.remove(png_path)

    return send_file('converted_images.zip', as_attachment=True)

@app.route('/lock-pdf', methods=['POST'])
def lock_pdf_endpoint():
    if 'file' not in request.files or 'password' not in request.form:
        return "No file part or password"

    file = request.files['file']
    password = request.form['password']
    if file.filename == '':
        return "No selected file"

    input_pdf_path = 'input_file.pdf'
    file.save(input_pdf_path)

    output_pdf_path = 'locked_file.pdf'
    lock_pdf(input_pdf_path, output_pdf_path, password)

    @after_this_request
    def delete_files(response):
        # Function to delete files after the response is sent
        os.remove(input_pdf_path)
        return response

    return send_file(output_pdf_path, as_attachment=True)

@app.route('/unlock-pdf', methods=['POST'])
def unlock_pdf_endpoint():
    if 'file' not in request.files or 'password' not in request.form:
        return "No file part or password"

    file = request.files['file']
    password = request.form['password']
    if file.filename == '':
        return "No selected file"

    input_pdf_path = 'input_file.pdf'
    file.save(input_pdf_path)

    output_pdf_path = 'unlocked_file.pdf'
    unlock_pdf(input_pdf_path, output_pdf_path, password)

    return send_file(output_pdf_path, as_attachment=True)

@app.route('/convert/jpeg-to-png', methods=['POST'])
def jpeg_to_png_endpoint():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    jpeg_path = 'uploaded_file.jpg'
    file.save(jpeg_path)

    output_png_path = 'output_file.png'
    jpeg_to_png(jpeg_path, output_png_path)

    return send_file(output_png_path, as_attachment=True)

@app.route('/convert/png-to-jpeg', methods=['POST'])
def png_to_jpeg_endpoint():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    png_path = 'uploaded_file.png'
    file.save(png_path)

    output_jpeg_path = 'output_file.jpg'
    png_to_jpeg(png_path, output_jpeg_path)

    return send_file(output_jpeg_path, as_attachment=True)

@app.route('/compress-image', methods=['POST'])
def compress_image_endpoint():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    image_path = 'uploaded_image.png'
    file.save(image_path)

    target_size_kb = request.form.get('size', type=int)  # Get target size from form

    output_path = reduce_image_size(image_path, 'compressed_image.jpg', target_size_kb)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
