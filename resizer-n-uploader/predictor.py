from flask import Flask, jsonify, request
from PIL import Image
import requests
import face_recognition
import cloudinary
import cloudinary.uploader
import cloudinary.api
from random import randint

app = Flask(__name__)
@app.route('/predictgender', methods=['POST'])
def make_predict():
    IMG_SIZE=100

    #downloading and saving the image
    data=request.get_json(force=True)
    imgurl=data["url"]
    img_data = requests.get(imgurl).content
    file_type=imgurl[imgurl.rfind('.'):]
    img_filename_downloaded = 'downloaded'+file_type
    with open(img_filename_downloaded, 'wb') as handler:
        handler.write(img_data)

    #detecting the face and cropping the face in the shape of a square
    raw_image = face_recognition.load_image_file(img_filename_downloaded)
    face_locations = face_recognition.face_locations(raw_image)
    top, right, bottom, left = face_locations[0]
    top_c, left_c = top, left
    top = top-((bottom-top)*3)//4 if (top-((bottom-top)*3)//4)>0  else 0
    bottom = bottom+(bottom-top_c) if bottom+(bottom-top_c)<raw_image.shape[0] else raw_image.shape[0]
    left = left-((right-left)//2) if (left-((right-left)//2))>0 else 0
    right = right+((right-left_c)//2) if (right+((right-left_c)//2))<raw_image.shape[1] else raw_image.shape[1]

    larger_dimen = 0
    smaller_dimen = 0
    if(bottom-top>right-left):
        larger_dimen = bottom-top
        smaller_dimen = right-left
    else:
        larger_dimen = right-left
        smaller_dimen = bottom-top
    
    selected_dimen = smaller_dimen if(top+larger_dimen>raw_image.shape[0] or left+larger_dimen>raw_image.shape[1]) else larger_dimen
    horizontal_mid = (right+left)//2
    print(top, bottom, left, right, selected_dimen)
    left_limit = horizontal_mid-(selected_dimen//2) if(horizontal_mid-(selected_dimen//2)>=0) else 0
    rigth_limit = left_limit+selected_dimen
    print(top, top+selected_dimen, horizontal_mid-(selected_dimen//2), horizontal_mid+(selected_dimen//2))
    face_image = raw_image[top:top+selected_dimen, left_limit:rigth_limit]
    print(raw_image.shape)
    print(face_image.shape)
    img = Image.fromarray(face_image)
    
    #resizing the image and saving it after appending a random number to its name
    img = img.resize((IMG_SIZE,IMG_SIZE), Image.ANTIALIAS)
    img_filename_resized = 'resized'+str(randint(1, 100000))+file_type
    img.save(img_filename_resized)

    #uploading the image to cloudinary and returing its url
    url = cloudinary.uploader.upload(img_filename_resized)['url']
    return url

@app.before_first_request
def loadthemodel():
    cloudinary.config( 
    cloud_name = "YOUR CLOUDINARY", 
    api_key = "CREDENTIALS", 
    api_secret = "HERE" 
    )

if __name__=="__main__":
    app.run()