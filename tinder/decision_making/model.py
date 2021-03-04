import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Convolution2D, MaxPooling2D
from sklearn.model_selection import train_test_split
from tensorflow.keras import optimizers
from keras.utils import np_utils
import cv2
import os


img_size = 640

class Model:
    def __init__(self):
        # self.dataset = dataset_path
        self.images = []
        self.labels = []

    def process_image(self, image_path):
        img = cv2.imread(image_path)
        # gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dim = (img_size, img_size)
        resized_img = cv2.resize(img, dim, interpolation=cv2.INTER_LINEAR)
        return resized_img

    def split_data(self, dataset_path):
        temp_images = []
        temp_labels = []
        liked_folder_path = os.path.join(dataset_path, 'liked')
        disliked_folder_path = os.path.join(dataset_path, 'disliked')

        for file in os.listdir(liked_folder_path):
            image = self.process_image(os.path.join(liked_folder_path, file))
            temp_images.append(image)
            temp_labels.append(1)

        for file in os.listdir(disliked_folder_path):
            image = self.process_image(os.path.join(disliked_folder_path, file))
            temp_images.append(image)
            temp_labels.append(0)

        self.images = np.array(temp_images)
        self.labels = np.array(temp_labels)

        print(self.images.shape)
        print(self.labels.shape)

    def define_model(self):
        X_train, X_test, y_train, y_test = train_test_split(self.images, self.labels, train_size=0.8, random_state=20)

        nb_classes = 2
        y_train = np.array(y_train)
        y_test = np.array(y_test)
        Y_train = np_utils.to_categorical(y_train, nb_classes)
        Y_test = np_utils.to_categorical(y_test, nb_classes)

        X_train = X_train.astype('float32')
        X_test = X_test.astype('float32')

        print("Training matrix shape", X_train.shape)
        print("Testing matrix shape", X_test.shape)

        print("Training label shape", Y_train.shape)
        print("Testing label shape", Y_test.shape)

        model = Sequential()
        model.add(Convolution2D(32, 3, 3, activation='relu', input_shape=(img_size, img_size, 3)))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Convolution2D(32, 3, 3, activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Convolution2D(64, 3, 3, activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(2, activation='softmax'))

        adam = optimizers.SGD(lr=1e-4, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy',
                      optimizer=adam,
                      metrics=['accuracy'])

        model.fit(X_train, Y_train,
                  batch_size=64, epochs=10, verbose=2)
