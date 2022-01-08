import base64

import requests


def to_anime(image_path: str, output_path: str):
    encoded_string = base64.b64encode(open(image_path, "rb").read()).decode('ascii')
    r = requests.post(url='https://hf.space/gradioiframe/akhaliq/AnimeGANv2/api/predict',
                      json={"data": [
                          f"data:image/png;base64,{str(encoded_string)}",
                          "version 1 (\ud83d\udd3a stylization, \ud83d\udd3b robustness)"
                      ]})
    base64_predict_image = r.json()['data'][0]
    base64_predict_image = base64_predict_image.partition(",")[2]
    base64_message = base64_predict_image.encode('utf-8')
    message_bytes = base64.decodebytes(base64_message)
    image_result = open(output_path, 'wb')  # create a writable image and write the decoding result
    image_result.write(message_bytes)


def to_dragness(image_path: str, output_path: str):
    encoded_string = base64.b64encode(open(image_path, "rb").read()).decode('ascii')
    r = requests.post(url='https://hf.space/gradioiframe/Norod78/Dragness/api/predict',
                      json={"data": [
                          f"data:image/png;base64,{str(encoded_string)}"
                      ]})
    base64_predict_image = r.json()['data'][0]
    base64_predict_image = base64_predict_image.partition(",")[2]
    base64_message = base64_predict_image.encode('utf-8')
    message_bytes = base64.decodebytes(base64_message)
    image_result = open(output_path, 'wb')  # create a writable image and write the decoding result
    image_result.write(message_bytes)


def to_jojo(image_path: str, output_path: str, ref_model="JoJo"):
    encoded_string = base64.b64encode(open(image_path, "rb").read()).decode('ascii')
    r = requests.post(url='https://hf.space/gradioiframe/akhaliq/JoJoGAN/api/predict',
                      json={"data": [
                          f"data:image/png;base64,{str(encoded_string)}",
                          ref_model
                      ]})
    base64_predict_image = r.json()['data'][0]
    base64_predict_image = base64_predict_image.partition(",")[2]
    base64_message = base64_predict_image.encode('utf-8')
    message_bytes = base64.decodebytes(base64_message)
    image_result = open(output_path, 'wb')  # create a writable image and write the decoding result
    image_result.write(message_bytes)
