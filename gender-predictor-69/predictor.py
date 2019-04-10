from flask import Flask, jsonify, request
from keras.models import load_model
import numpy as np
from PIL import Image
import requests

app = Flask(__name__)
@app.route('/predictgender', methods=['POST'])
def make_predict():

    #downloading and saving the image
    data=request.get_json(force=True)
    imgurl=data["url"]
    print("lol not working", imgurl)
    img_data = requests.get(imgurl).content
    file_type=imgurl[imgurl.rfind('.'):]
    img_filename_downloaded = 'downloaded'+file_type
    with open(img_filename_downloaded, 'wb') as handler:
        handler.write(img_data)

    #converting the image into grayscale and extracting pixel matrix
    img_bnw = Image.open(img_filename_downloaded).convert('L')
    gray_matrix=np.asarray(img_bnw.getdata(),dtype=np.float64).reshape((1, 100, 100, 1))

    #making predictions
    girlboyratio=model.predict(gray_matrix)

    return jsonify({"Girl Characteristics in percent":girlboyratio[0][0]*100/(girlboyratio[0][0]+girlboyratio[0][1]),"Boy Characteristics in percent":girlboyratio[0][1]*100/(girlboyratio[0][0]+girlboyratio[0][1])})

@app.before_first_request
def loadthemodel():
    #loading the model here to ensure it's loaded only once
    global model
    model = load_model('path to the saved model')

if __name__=="__main__":
    app.run()