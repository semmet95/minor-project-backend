# minor-project-backend

Backend for our minor project that uses a trained keras model to classify images as males or females (the images must contain the face of the person).

The backend is hosted on Heroku and is divided into two parts because I kept getting memory overflow errors due to the free tier limits (because as of yet I'm a broke student who can't afford to pay Heroku)

## resizer-n-uploader
A flask application that accepts post requests with a field `url` that contains the url to the image to be analyzed by the saved model. The app then uses [this](https://github.com/ageitgey/face_recognition) api to detect the face in the image and resize by cropping keeping the face in the center. Now this image (resized to 100 * 100) is uploaded to cloudinary (I love Cloudinary, their free tier limit is mind blowingly high) and the app returns its url. What are we going to do with the resized image? How are we going to predict the gender? How does all this tie up? All shall be answered in the next episode of... I mean keep reading.

## gender-predictor-69
Really sorry about the title, I was trying to be edgy and ended up being lame (and I'm too lazy to change it). So... last time on minor-project-backend... ok I'll stop.
Now this is another flask app that accepts post requests with a field `url` that contains... yeah, you guessed it right, the url that was returned in the previous ~~episode~~ app. Now this app transforms the image into grayscale and then into a matrix and then feeds it to the saved model to get predictions, and then finally returns predictions as probabilities.

### 👏👏 Bonus Code
## classifier_fulltrain.py
This is the code you can use to train your own model. You're gonna have to download the dataset though. Here I have used both the IMDB and WIKI dataset. You can find them both [here](http://datax.kennesaw.edu/imdb_wiki/)

# USAGE
You can test the model yourself. Here's an example (I'm using `curl` here)

First get the url to the resized image using the url to the original image, so here you use the `resizer-n-uploader` app

`curl -X POST -d '{"url":"https://www.barrheadnews.com/resources/images/8018549.jpg"}' https://resizer-n-uploader.herokuapp.com/predictgender`

This will return a url to the resized image which in my case was
http://res.cloudinary.com/devamit/image/upload/v1554907451/resized8719.jpg

And now you send a post request to the `gender-predictor-69` app using the url you received

`curl -X POST -d '{"url":"http://res.cloudinary.com/devamit/image/upload/v1554907451/resized8719.jpg"}' https://gender-predictor-69.herokuapp.com/predictgender`

And you get your probabilities, which in my case were
`{"Boy Characteristics in percent":0.11391347634882505,"Girl Characteristics in percent":99.8860857319175}`
