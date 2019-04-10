# minor-project-backend

Backend for our minor project that uses a trained keras model to classify images as males or females (the images must contain the face of the person).

The backend is hosted on Heroku and is divided into two parts :

## resizer-n-uploader
A flask application that accepts post requests with a field > url that contains the url to the image to be analyzed by the saved model.
