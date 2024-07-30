from flask import Flask, render_template, request, redirect, url_for
from PIL import Image, ImageEnhance, ImageFilter
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


def convert_to_black_and_white(image):
    return image.convert('L')


def increase_sharpness(image):
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(5.0)  # Increase sharpness intensity


def pixelate(image, pixel_size=15):  # Increase pixelation intensity
    small = image.resize((image.width // pixel_size, image.height // pixel_size), Image.NEAREST)
    return small.resize(image.size, Image.NEAREST)


def depixelate(image):
    return image.filter(ImageFilter.GaussianBlur(2))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            print("No file part")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print("No selected file")
            return redirect(request.url)
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            print(f"File saved to {filepath}")
            try:
                image = Image.open(filepath)

                if request.form.get('action') == 'black_white':
                    image = convert_to_black_and_white(image)
                elif request.form.get('action') == 'sharpen':
                    image = increase_sharpness(image)
                elif request.form.get('action') == 'pixelate':
                    image = pixelate(image)
                elif request.form.get('action') == 'depixelate':
                    image = depixelate(image)

                edited_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'edited_' + file.filename)
                image.save(edited_filepath)
                print(f"Edited file saved to {edited_filepath}")
                return render_template('index.html', uploaded_image=filepath, edited_image=edited_filepath)
            except Exception as e:
                print(f"An error occurred: {e}")
                return redirect(request.url)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
