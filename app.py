from flask import Flask, request, send_file
from PIL import Image
import os

app = Flask(__name__)

# Tworzenie katolgu /tmp, jeśli nie istnieje.
if not os.path.exists('/tmp'):
    os.makedirs('/tmp')

# Definiowanie katalogu publicznego, w którym przechowywane są obrazy.
public_directory = 'C:\\Users\\ampou\\OneDrive\\Obrazy'


@app.route('/<image>', methods=['GET'])
def resize_image(image):
    try:
        width = int(request.args.get('w'))
        height = int(request.args.get('h'))

        # Sprawdzenie, czy podano szerokość i wysokość
        if not width or not height:
            return "Width and height parameters are required", 400

        # Sprawdzenie, czy obraz istnieje w katalogu publicznym.
        image_path = os.path.join(public_directory, image)
        if not os.path.exists(image_path):
            return "Image not found", 404

        # Otwieranie pliku obrazu.
        with Image.open(image_path) as img:
            # Konwertowanie obrazu do RGB, jeśli jest w RGBA
            if img.mode == 'RGBA':
                img = img.convert('RGB')

            # Zmiana rozmiaru obrazu
            resized_img = img.resize((width, height))

            # Zapisanie obrazu o zmienionym rozmiarze w pliku tymczasowym
            temp_image_path = '/tmp/resized_image.jpg'
            resized_img.save(temp_image_path)

        # W odpowiedzi wysłanie obrazu o zmienionym rozmiarze.
        return send_file(temp_image_path, mimetype='image/jpeg')

    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    app.run(debug=True)

# http://127.0.0.1:5000/mail.png?w=1430&h=1300