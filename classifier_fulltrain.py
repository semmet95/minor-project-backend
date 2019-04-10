from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

import keras
from keras.models import Sequential
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dropout
from keras.layers.core import Dense
from keras import backend as K

try:
    from keras.models import load_model
    model = load_model('path to the model checkpoint')
except Exception as err:
    print("\n\ntype error: " + str(err))

    csv1 = pd.read_csv('path to imdb4p5.csv, available online')
    csv1_data = csv1.values
    csv2 = pd.read_csv('path to wiki5.csv, available online')
    csv2_data = csv2.values

    csv1_features = csv1_data[:, 3:]
    csv1_labels = csv1_data[:, 1]
    csv2_features = csv2_data[:, 3:]
    csv2_labels = csv2_data[:, 1]

    all_features = np.concatenate((csv1_features, csv2_features), axis=0)
    all_labels = np.concatenate((csv1_labels, csv2_labels), axis=0)
    
    x_train, x_test, y_train, y_test = train_test_split(all_features, all_labels, test_size=0.2, random_state=2)
    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.25, random_state=3)

    x_train = x_train.reshape(x_train.shape[0], 100, 100, 1)
    x_val = x_val.reshape(x_val.shape[0], 100, 100, 1)

    y_train_one_hot = keras.utils.to_categorical(y_train)
    y_val_one_hot = keras.utils.to_categorical(y_val)

    inputShape = (100,100,1)
    chanDim = -1
    model = Sequential()
    model.add(Conv2D(32, (3,3), padding="same", input_shape= inputShape))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(MaxPooling2D(pool_size=(3,3)))
    model.add(Dropout(0.25))
    model.add(Conv2D(64, (3,3), padding="same"))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(Conv2D(64, (3,3), padding="same"))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25))
    model.add(Conv2D(128, (3,3), padding="same"))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(Conv2D(128, (3,3), padding="same"))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(1024))
    model.add(Activation("relu"))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))        
    model.add(Dense(2))
    model.add(Activation("sigmoid"))
    model.compile(loss='mse', optimizer='adam',metrics=['accuracy'])
    model.fit(x_train,y_train_one_hot,validation_data=(x_val,y_val_one_hot),epochs=10,batch_size=100,verbose=1)

x_test = x_test.reshape(x_test.shape[0], 100, 100,1)
y_test_one_hot = keras.utils.to_categorical(y_test)
score = model.evaluate(x_test, y_test_one_hot, verbose=1)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

model.save('path where you wanna save the model to') # creates a HDF5 file 'my_model.h5' 