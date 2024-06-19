import streamlit as st
import json
import requests
import base64
from PIL import Image
import io


#these are main classes our image is trained on
#defined the classes in alphabectical order
PREDICTED_LABELS = ["Adult", "Child"]


def get_prediction(image_data):
  #replace your image classification ai service URL
  url = 'https://askai.aiclub.world/30747a9a-354c-4325-bf79-8c3ea209918c'
  r = requests.post(url, data=image_data)
  response = r.json()['predicted_label']
  score = r.json()['score']
  #print("Predicted_label: {} and confidence_score: {}".format(response,score))
  return response, score


#creating the web app

#setting up the title
st.title("Identifying user age groups")#change according to your project
#setting up the subheader
st.subheader("File Uploader")#change according to your project

#file uploader
image = st.file_uploader(label="Upload an image",accept_multiple_files=False, help="Upload an image to classify them")
if image:
    #converting the image to bytes
    img = Image.open(image)
    buf = io.BytesIO()
    img.save(buf,format = 'JPEG')
    byte_im = buf.getvalue()

    #converting bytes to b64encoding
    payload = base64.b64encode(byte_im)

    #file details
    file_details = {
      "file name": image.name,
      "file type": image.type,
      "file size": image.size
    }

    #write file details
    st.write(file_details)

    #setting up the image
    st.image(img)

    #predictions
    response, scores = get_prediction(payload)

    #if you are using the model deployment in navigator
    #you need to define the labels
    response_label = PREDICTED_LABELS[response]

    col1, col2 = st.columns(2)
    with col1:
      st.metric("Prediction Label",response_label)
    with col2:
      st.metric("Confidence Score", max(scores))



