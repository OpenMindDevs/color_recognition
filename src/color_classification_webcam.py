#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------
# --- Author         : Ahmet Ozlu
# --- Mail           : ahmetozlu93@gmail.com
# --- Date           : 31st December 2017 - new year eve :)
#  
# MIT License

# Copyright (c) 2018 Ozlu

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# ----------------------------------------------
# El autor de una parte del codigo implementado fue contactado y se nos dio permiso de tulizarlo siempre y
# cuando dieramos credito
# Paul Silisteanu
# sol-prog on Github
# https://solarianprogrammer.com/2018/04/21/python-opencv-show-video-tkinter-window/
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
import imutils
import requests
from gtts import gTTS
from pygame import mixer

prediction= "n.a"

class App:

    #########FUNCION TRADUCIR################################
    
    def Traduccion(self, source, target, text):
        parametros = {'sl': source, 'tl': target, 'q': text}
        cabeceras = {"Charset":"UTF-8","User-Agent":"AndroidTranslate/5.3.0.RC02.130475354-53000263 5.1 phone TRANSLATE_OPM5_TEST_1"}
        url = "https://translate.google.com/translate_a/single?client=at&dt=t&dt=ld&dt=qca&dt=rm&dt=bd&dj=1&hl=es-ES&ie=UTF-8&oe=UTF-8&inputm=2&otf=2&iid=1dd3b944-fa62-4b55-b330-74909a99969e"
        response = requests.post(url, data=parametros, headers=cabeceras)
        if response.status_code == 200:
            for x in response.json()['sentences']:
                return x['trans']
        else:
            return "Ocurrió un error"
    ##############################################################

    def __init__(self, window, window_title, video_source=0):
        self.training()
        self.window = window
        self.window.title(window_title)

        self.window.rowconfigure(0,  weight=1)
        self.window.columnconfigure(0, weight=1)

        self.video_source = video_source
        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

         # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = 480, bg="red")
        self.canvas.grid(rowspan=9,column=0)
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
        self.nameApp = tkinter.Label(window, text="Color Recognition")
        #botones disposicion
        self.nameApp.grid(row=0, column=1)
        self.btn_snapshot.grid(row=1, column=1, padx=5)
        self.btn_color.grid(row=2, column=1, sticky=S, padx=5)

         
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

    def reproducir(self, texto, language):
        NOMBRE_ARCHIVO = "sound.mp3"
        tts = gTTS(texto, lang=language)
        # Nota: podríamos llamar directamente a save
        with open(NOMBRE_ARCHIVO, "wb") as archivo:
            tts.write_to_fp(archivo)

        #playsound(NOMBRE_ARCHIVO)  
        print("estoy escuchando "+texto) 
        mixer.init()
        mixer.music.load(NOMBRE_ARCHIVO)
        mixer.music.play()    
 
    def color(self):
        print("Estoy viendo el color:" + prediction)
        en=prediction
        es=self.Traduccion("en","es",prediction)
        fr=self.Traduccion("en","fr",prediction)
        ge=self.Traduccion("en","ge",prediction)
        pt=self.Traduccion("en","pt",prediction)
        it=self.Traduccion("en","it",prediction)
        Label(self.window, text="English: "+en).grid(row=3, column=1, sticky=N)
        Label(self.window, text="Spanish: "+es).grid(row=4, column=1, sticky=N)
        Label(self.window, text="French: "+fr).grid(row=5, column=1, sticky=N)
        Label(self.window, text="German: "+ge).grid(row=6, column=1, sticky=N)
        Label(self.window, text="Portuguese: "+pt).grid(row=7, column=1, sticky=N)
        Label(self.window, text="Italian: "+it).grid(row=8, column=1, sticky=N)
        Button(self.window, text="play", width=20 ,command=lambda : self.reproducir(en,"en-us")).grid(row=3, column=2)
        Button(self.window, text="play", width=20 ,command=lambda : self.reproducir(es,"es-us")).grid(row=4, column=2)
        Button(self.window, text="play", width=20 ,command=lambda : self.reproducir(fr,"fr")).grid(row=5, column=2)
        Button(self.window, text="play", width=20 ,command=lambda : self.reproducir(ge,"de")).grid(row=6, column=2)
        Button(self.window, text="play", width=20 ,command=lambda : self.reproducir(pt,"pt")).grid(row=7, column=2)
        Button(self.window, text="play", width=20 ,command=lambda : self.reproducir(it,"it")).grid(row=8, column=2)

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
            frame = imutils.resize(frame, width=480, height=480)
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
