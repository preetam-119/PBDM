import cv2
from pymongo import MongoClient
from pandas import DataFrame
import numpy as np

# Initialize MongoDB connection
client = MongoClient('mongodb://localhost:27017')  #connection string
db = client['mydb']  # database name
collection = db['test']  # collection name

# Retrieve the image from MongoDB
# This function is used to view one random image from db for POC

retrieved_document = collection.find_one()
image_data = retrieved_document['Image']
image_array = np.frombuffer(image_data, np.uint8)
retrieved_image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

# Display the retrieved image
cv2.imshow('Retrieved Image', retrieved_image)


# Display the retrieved image
cv2.waitKey(0)

# Release the video capture and close the MongoDB connection
client.close()
