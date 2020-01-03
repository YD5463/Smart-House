#import speech_recognition as sr
from flask import Flask, flash, redirect, render_template, request, session, abort, make_response
#import RPi.GPIO as GPIO
import time

from DataBaseManager import DataBaseManager

'''
def input_speech():
    # Record Audio
    r = sr.Recognizer()
    with sr.WavFile("test.wav") as source:              # use "test.wav" as the audio source
        audio = r.record(source)
    return audio
def speech_to_text():
    audio = input_speech()
    r = sr.Recognizer()
    # Speech recognition using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        return ("You said: " + r.recognize_google(audio))
    except sr.UnknownValueError:
        return ("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        return ("Could not request results from Google Speech Recognition service; {0}".format(e))
'''
class MenuManager:
    database = DataBaseManager()

    @staticmethod
    def add_device():
        MenuManager.database.add_device(session["email"],request.form['Device_name'],request.form['Device_type'])
        return render_template("Menu.html",result = MenuManager.database.get_devices_by_type(session['email'],"light"))

    @staticmethod
    def remove_device(self):
        MenuManager.database.remove_device(session["email"],request.form["Device_name"])
        return render_template("Menu.html",result = MenuManager.database.get_devices_by_type(session['email'],"light"))

    @staticmethod
    def turn_on_or_off():
        '''
        #for check on raspberry
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(18,GPIO.OUT)
        if('on' in request.form.getlist('on-off')):
            print 'led on'
            GPIO.output(18,GPIO.HIGH)
        else:
            print 'led off'
            GPIO.output(18,GPIO.LOW)
        '''

        #for debug in computer

        status = "off"
        for device_name in request.form.getlist("device_name"):
            if('on' in request.form.getlist(device_name)):
                status = "on"
            else:
                status = "off"
            MenuManager.database.change_status(status,session['email'],device_name)
        return render_template("Menu.html",result = MenuManager.database.get_devices_by_type(session['email'],"light"))
    @staticmethod
    def input_speech_to_text_request():
        '''
        file = request.files['data']
        with open("test.wav",'wb') as save:
            save.write(file.read())
        text_from_user = speech_to_text()
        if "turn on" in text_from_user:
            MenuManager.turn_on_or_off()
        '''



