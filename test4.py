import base64

def image_file_to_base64(file_path):
    with open(file_path, "rb") as image_file:
        data = base64.b64encode(image_file.read())

    return data.decode('utf-8')

encoded_data = image_file_to_base64("data/play_movie3.jpg")

with open('play_movie3.png.b64', 'w') as f:
    f.write(bytearray(encoded_data, 'UTF-8').decode())