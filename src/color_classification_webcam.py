#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------
# --- Author         : Ahmet Ozlu
# --- Mail           : ahmetozlu93@gmail.com
# --- Date           : 31st December 2017 - new year eve :)
# ----------------------------------------------

#Librerias del repo original
from color_recognition_api import color_histogram_feature_extraction
from color_recognition_api import knn_classifier
import os
import os.path
#fin de las librerias
import tkinter
from tkinter import *
import cv2
import PIL.Image
import PIL.ImageTk
import time

prediction= "n.a"

class App:
    def __init__(self, window, window_title, video_source=0):
        self.training()
        self.window = window
        self.window.title(window_title)

        self.window.rowconfigure(0, minsize=800, weight=1)
        self.window.columnconfigure(0, minsize=800, weight=1)

        self.video_source = video_source
        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

         # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.grid(row=0,column=0)
        #self.canvas.pack()

        #creacion de un frame para manejar botones con grid
        frame = Frame(self.window)
        frame.grid(row=0,column=1, sticky="n")

         # Button that lets the user take a snapshot
        self.btn_snapshot=tkinter.Button(window, text="Tomar captura", width=40, command=self.snapshot)
        #self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        #Boton para imprimir color encontrado
        self.btn_color=tkinter.Button(window, text="Captura color", width=40, command=self.color)
        #self.btn_color.pack(anchor=tkinter.CENTER, expand=True)

        #botones disposicion
        self.btn_snapshot.grid(row=0, column=1, sticky=S, padx=5)
        self.btn_color.grid(row=1, column=1, sticky=S, padx=5)

         
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()
 
        self.window.mainloop()
 
    def snapshot(self):
         # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            print("pantalla capturada")
 
    def color(self):
        print("Estoy viendo el color:" + prediction)
        Label(self.window, text="__"+prediction+"__").grid(row=1, sticky=N)

    def update(self):
         # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
 
        self.window.after(self.delay, self.update)

    #Funcion de entrenamiento
    def training(self):
        # checking whether the training data is ready
        self.PATH = './training.data'

        if os.path.isfile(self.PATH) and os.access(self.PATH, os.R_OK):
            print ('training data is ready, classifier is loading...')
        else:
            print ('training data is being created...')
            open('training.data', 'w')
            color_histogram_feature_extraction.training()
            print ('training data is ready, classifier is loading...')
    ##
 
class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
 
         # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
 
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            global prediction
            prediction = knn_classifier.main('training.data', 'test.data')
            if ret:
                #Funcionalidad de aplicar el modelo
                cv2.putText(
                    frame,
                    'Prediction: ' + prediction,
                    (15, 45),
                    cv2.FONT_HERSHEY_PLAIN,
                    3,
                    (81, 229, 255),
                    )
                    #Display the resulting frame
                    #cv2.imshow('color classifier', frame)

                color_histogram_feature_extraction.color_histogram_of_test_image(frame)

                #self.prediction = knn_classifier.main('training.data', 'test.data')
                ###

                 # Return a boolean success flag and the current frame converted to BGR             
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)
 
     # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
 
 # Create a window and pass it to the Application object
App(tkinter.Tk(), "ACA color recogniiton 01-2020")
