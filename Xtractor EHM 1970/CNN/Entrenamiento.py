import cv2
import numpy as np
import matplotlib.pyplot as plt
from time import time


from tensorflow.keras import datasets, layers, models
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras import optimizers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense
from tensorflow.keras import backend as K
from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import PIL
from PIL import Image
import os
from sklearn.utils import shuffle


import glob


total = 0

def Normalizar():                    

    global total
    
    for i in range(0,10):
        
        path = 'C:\\Users\\VAIO\\ML\\Dataset Anuarios\\Dataset Testing'
        
        path = path + '\\' + str(i) + '\\'
        
        files = []
        
        for r,d,f in os.walk(path):
            for file in f:
                files.append(os.path.join(r, file))
        
        x = 0
        
        if not os.path.exists('C:\\Users\\VAIO\\ML\\Dataset Anuarios\\Dataset Testing\\' + str(i) + 'r\\'):
            os.mkdir('C:\\Users\\VAIO\\ML\\Dataset Anuarios\\Dataset Testing\\' + str(i) + 'r\\')
        
        total = total + len(files)
        
        for f in files:
            img = cv2.imread(f)
            res = cv2.resize(img,(15,30))
            cv2.imwrite(os.path.join('C:\\Users\\VAIO\\ML\\Dataset Anuarios\\Dataset Testing\\' + str(i) + 'r\\', str(x) + '.png'),res)
            x = x+1                    

def CNN():
    
    global total
    
    cont = 0

    test_img = np.zeros((total,30,15))
    train_label = np.zeros((total,1))
    
    for i in range(0,10):
    
        path = 'C:\\Users\\VAIO\\ML\\Dataset Anuarios\\Dataset Testing'
        
        path = path + '\\' + str(i) + 'r\\'
                
        for filename in os.listdir(path):
            img = load_img(path+filename)
            x = img_to_array(img)
            x = x[:,:,0]
            test_img[cont] = x
            train_label[cont] = str(i)
            cont += 1
    
    test_img, train_label = shuffle(test_img, train_label)
    
    test_img = test_img.reshape((total,30,15,1))
    train_label = to_categorical(train_label)
    test_img = test_img.astype('float32') / 255.
    
    convNN = models.Sequential()
    convNN.add(layers.Conv2D(filters=64, kernel_size=(2, 2), padding='same', activation='relu',input_shape=(30,15,1)))
    convNN.add(layers.MaxPooling2D(pool_size=(2, 2), padding='same'))
    convNN.add(layers.Conv2D(filters=64, kernel_size=(2, 2), padding='same', activation='relu'))
    convNN.add(layers.MaxPooling2D(pool_size=(2, 2), padding='same' ))
    convNN.add(layers.Conv2D(filters=64, kernel_size=(1, 1), padding='same', activation='relu'))
    convNN.add(layers.Flatten())
    convNN.add(layers.Dense(units=32, activation='relu'))
    convNN.add(layers.Dense(units=16, activation='sigmoid'))
    #convNN.add(layers.Dense(units=8, activation='relu'))
    convNN.add(layers.Dense(units=10, activation='softmax'))
    convNN.summary()
    
    convNN.compile(optimizer='rmsprop',loss='categorical_crossentropy',metrics=['accuracy'])
    convNN.fit(x = test_img, y = train_label, epochs=48,batch_size=8,verbose=2)
    
    
    convNN.save('red_final.h5')

Normalizar()
CNN()