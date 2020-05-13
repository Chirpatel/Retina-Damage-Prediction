import os
os.system('pip install --upgrade pip')
os.system('pip install tensorflow==2.2.0rc4')

import random, string
from flask import Flask, render_template, request, jsonify
import base64
import numpy as np
import io
from PIL import Image
from base64 import decodestring
#import tensorflow as tf
from keras import backend as K
from flask import request
from flask import jsonify
from flask import Flask
import keras
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage.io import imread
from skimage.transform import resize
import shutil
import cv2
app = Flask(  # Create a flask app
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)

ok_chars = string.ascii_letters + string.digits


@app.route('/')  # What happens when the user visits the site
def base_page():
	return render_template(
		'predict.html',  # Template file path, starting from the templates folder. 
	)


model=0
def get_model():
    global model
    model = keras.models.load_model("model_3000trained10.model")
    print(" * Model Loded!")

def preprocess_image(image):
    if image.mode !="RGB":
        image=image.convert("RGB")
        image.resize((256,256))
    return image

print(" * Loading Keras Model...")
get_model()

@app.route("/",methods=["POST"])
def predict():
    CATEGORIES=["NORMAL","CNV","DME","DRUSEN"]
    message = request.get_json(force=True)
    #print(message)
    
    encoded = message['image']
    decoded = base64.b64decode(encoded)
    bytesio=io.BytesIO(decoded)
    filename="test.png"
    with open(filename, "wb") as outfile:
        # Copy the BytesIO stream to the output file
        outfile.write(bytesio.getbuffer())
    num=find()
    response = {
        'prediction': str(num[0]),
				'prob': str(num[1])
    }
    return jsonify(response)

def find():

	CATEGORIES=["NORMAL","CNV","DME","DRUSEN"]

	image=imread("test.png")
	img = np.asarray(image,dtype=np.uint8)
	img = cv2.resize(img,(128,128))
	img = img.reshape(1,128,128,1)
	classIndex = int(model.predict_classes(img))
	predictions = model.predict(img)
	probVal= np.amax(predictions)
	print(CATEGORIES[classIndex],probVal)
	return  [CATEGORIES[classIndex],probVal]





if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=5000,  # Randomly select the port the machine hosts on.
		threaded=False
	)